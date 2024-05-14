from kafka import KafkaConsumer
from payments.util.serializers import json_deserializer
from kafka import TopicPartition
from payments.transactions.model import Transaction
from payments.transactions.service import TransactionService
from payments.accounts.service import AccountsService
import json, os, logging
from payments.util.ds import DatasourceUtil


class TransactionProcessor:

    def __init__(self, transaction_svc: TransactionService, kafka_brokers: ['localhost:9092'], consumer_group="t_0_processor", topic="transactions", partition=0):
        self.consumer = KafkaConsumer(group_id=consumer_group, bootstrap_servers=kafka_brokers, value_deserializer=json_deserializer)
        self.consumer.assign([TopicPartition(topic, partition)])
        self.transaction_svc = transaction_svc


    def consume(self):
        print("starting consumer...")
        # At-least-once (Default) => May re-process a record.
        # At-most-once => May loose a transaction
        for msg in self.consumer:
            print("received message: {}".format(msg))
            j_data = json.loads(msg.value)
            transaction = Transaction(**j_data)

            try:
                self.transaction_svc.process_transaction(transaction)
            except Exception as e:
                self.transaction_svc.insert_failed_transactions(transaction, str(e))

def main():
    c_host = os.environ.get('CASSANDRA_HOST', 'localhost')
    kafka_brokers = os.environ.get('KAFKA_BROKERS', 'localhost:9092').join(',')

    # TODO: RETRY TO CONNECT IF FAILED
    retry = True
    db = None
    while retry: #TODO: Dirty AF
        try:
            db = DatasourceUtil(db_hosts=[c_host], kafka_brokers=kafka_brokers)
            retry = False
        except Exception as e:
            pass

    session = db.get_session()
    session.set_keyspace("payments")
    account_svc = AccountsService(logging.getLogger("TransactionProcessor"), db.session)
    transactions_svc = TransactionService(logging.getLogger("TransactionProcessor"), account_svc, db.session, kafka_brokers)

    consumer = TransactionProcessor(transactions_svc, kafka_brokers)

    consumer.consume()