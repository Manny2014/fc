import json

from flask_restful import Resource, marshal_with
from flask import request, jsonify, make_response
from uuid import uuid4

from payments.accounts.model import Account
from payments.accounts.service import AccountsService
from payments.transactions.service import TransactionService
from payments.transactions.model import Transaction
from payments.accounts.exceptions import AccountNotFound
from logging import Logger


class TransactionsApi(Resource):

    def __init__(self, logger: Logger, transaction_service: TransactionService, account_svc: AccountsService):
        self.transactions_service = transaction_service
        self.account_svc = account_svc
        self.logger = logger

    def get(self, transaction_id: str):
        pass

    def post(self):
        data = request.get_json()
        if data.get("from_account_id") is None or data.get("to_account_id") is None or data.get("amount") is None:
            make_response(jsonify({'error': 'Missing parameters: from_account_id, to_account_id, or amount'}), 400)

        self.logger.info("from_account_id {} to_account_id {} amount {}".format(data.get("from_account_id"),
                                                                                data.get("to_account_id"),
                                                                                data.get("amount")))

        transaction_id = str(uuid4())
        from_account_id = data.get('from_account_id')
        to_account_id = data.get('to_account_id')
        amount = float(data.get('amount'))

        from_account = None
        to_account = None

        try:
            from_account = self.account_svc.get_account(from_account_id)
            self.logger.info(f"from_account id {from_account.id}")
            to_account = self.account_svc.get_account(to_account_id)
            self.logger.info(f"to_account id {to_account.id}")
        except AccountNotFound as e:
            make_response(jsonify({'error': "InvalidTransaction", "message": str(e)}), 404)

        # Create transaction object
        transaction = Transaction(transaction_id, from_account.id, to_account.id, amount)

        # Check if there's enough fund
        if not from_account.has_money() or not from_account.has_more_than(amount):
            self.logger.info(f"{from_account.id} has no more money --> {from_account.has_money()}")
            self.logger.info(f"{from_account.id} has more than {amount} --> {from_account.has_more_than(amount)}")

            try:
                self.transactions_service.insert_failed_transactions(transaction, "not enough funds")
            except Exception as e:
                return make_response(jsonify({"error": "InsertFailedTransactionError", "message": str(e)}), 400)

        result_metadata = self.transactions_service.send_transaction(transaction)
        make_response(jsonify(result_metadata), 200)

