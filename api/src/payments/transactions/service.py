import json

from cassandra.cluster import Session
from kafka import KafkaProducer
from payments.util.serializers import json_serializer
from payments.transactions.model import Transaction
import json
from logging import Logger

from payments.accounts.service import AccountsService


class TransactionService():

    def __init__(self, logger: Logger, account_svc: AccountsService, db_session: Session, brokers=['localhost:9092']):
        self.db_session = db_session
        self.producer = KafkaProducer(bootstrap_servers=brokers, key_serializer=str.encode,
                                      value_serializer=json_serializer)
        self.logger = logger
        self.account_svc = account_svc

        self.insert_failed_transactions_statement = None

    def send_transaction(self, transaction: Transaction):
        self.logger.info(transaction.toJSON())
        # Hard coding to partition 0 so ensure ALL transactions are ordered.
        ## TODO: Would be better if we could do it by account. But which one from_ or to_?
        ## --> Thinking from_account: key=data['from_account_id']
        future = self.producer.send("transactions", key=transaction.from_account_id, value=transaction.toJSON(),
                                    partition=0)
        self.producer.flush(timeout=10)
        record_metadata = future.get(timeout=10)
        return record_metadata

    def process_transaction(self, transaction: Transaction):

        from_account = self.account_svc.get_account(transaction.from_account_id)
        to_account = self.account_svc.get_account(transaction.to_account_id)

        # Atomic operation
        batch = """
        BEGIN BATCH
            UPDATE accounts SET balance = {from_balance} - {amount} WHERE id = '{from_id}';
            UPDATE accounts SET balance = {to_balance} + {amount} WHERE id = '{to_id}';
        APPLY BATCH;
        """.format(amount=transaction.amount, from_id=transaction.from_account_id, to_id=transaction.to_account_id,
                   tran_id=transaction.id, from_balance=from_account.balance, to_balance=to_account.balance)

        result = self.db_session.execute(batch)

        # Check if the transaction was applied
        if not result.was_applied:
            self.insert_failed_transactions_statement(transaction, "Insufficient funds")
            return False

        self.logger.info(
            f"Transaction {transaction.id} processed: {transaction.amount} from {transaction.from_account_id} to {transaction.to_account_id}")

    def get_transaction(self, transaction_id: str):
        pass

    def insert_failed_transactions(self, transaction: Transaction, reason: str):
        self.logger.debug(f"inserting failed transaction {transaction.toJSON()} with reason: {reason}")
        statement = self.get_insert_failed_transactions()

        result = self.db_session.execute(statement,
                                         [transaction.id, transaction.from_account_id, transaction.to_account_id,
                                          transaction.amount, reason])

        if not result.was_applied:
            raise Exception("Failed transaction insert failed...")

    def get_insert_failed_transactions(self):
        if self.insert_failed_transactions_statement is None:
            self.insert_failed_transactions_statement = self.db_session.prepare(
                'INSERT INTO failed_transactions (id, from_account_id,to_account_id, amount, reason) VALUES (?, ?, ?, ?, ?) IF NOT EXISTS')

        return self.insert_failed_transactions_statement
