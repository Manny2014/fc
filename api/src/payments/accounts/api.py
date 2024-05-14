from flask_restful import Resource, marshal_with, fields
from cassandra.cluster import Session
from flask import request, jsonify, make_response
from uuid import uuid4
from payments.accounts.exceptions import AccountNotFound
from payments.accounts.service import AccountsService, AccountAlreadyExists
from payments.accounts.model import Account
from logging import Logger

class AccountsApi(Resource):

    def __init__(self, logger: Logger, accounts_svc: AccountsService):
        self.accounts_svc = accounts_svc
        self.logger = logger

    def get(self, account_id):
        try:
            account = self.accounts_svc.get_account(account_id)
            self.logger.info(f"retrieved account {account.toJSON()}")
            return make_response(jsonify({"id": account.id, "balance": account.balance}), 200)
        except AccountNotFound as e:
            return make_response(jsonify({"error": "AccountNotFound", "message": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"error": "UnknownError", "message": str(e)}), 400)

    # Create Account
    # Improvements: Handles accounts that already exists, uses prepared statements for better performance;
    def post(self):
        data = request.get_json()
        account_id = data.get("id", str(uuid4()))
        balance = data.get("balance", 0)
        account = Account(account_id, balance)

        try:
            self.accounts_svc.create_account(account.id, account.balance)
            return make_response(jsonify({'id': account.id, 'balance': account.balance}), 200)
        except AccountAlreadyExists as e:
            return make_response(jsonify({"error": "AccountAlreadyExists", "message": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"error": "UnknownError", "message": str(e)}), 400)

    # Delete account
    # TODO: Not implementing
    def delete(self, account_id):
        return make_response(jsonify({'id': account_id, 'method': 'accounts_delete'}), 200)

    # Update account
    # TODO: Not implementing
    def put(self):
        pass
