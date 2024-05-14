import os

from flask import Flask, jsonify, make_response
from payments.accounts.api import AccountsApi
from payments.accounts.service import AccountsService
from payments.transactions.api import TransactionsApi
from payments.transactions.api import TransactionService
from flask_restful import Api
from logging.config import dictConfig

# TODO: Delete
from payments.util.ds import DatasourceUtil

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


# Will be called by gunicorn
def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Setup cassandra
    c_host = os.environ.get('CASSANDRA_HOST', 'localhost')
    kafka_brokers = os.environ.get('KAFKA_BROKERS', 'localhost:9092').join(',')

    # TODO: RETRY TO CONNECT IF FAILED
    retry = True
    db = None
    app.logger.info("waiting for db to be ready...")
    while retry:     #TODO: Dirty AF
        try:
            db = DatasourceUtil(db_hosts=[c_host], kafka_brokers=kafka_brokers)
            retry = False
        except Exception as e:
            pass

    db.initialize(dev_mode=True)

    # Setup services
    account_svc = AccountsService(app.logger, db.session)
    transactions_svc = TransactionService(app.logger, account_svc, db.session, kafka_brokers)

    api.add_resource(TransactionsApi, '/transactions', '/transactions/<transaction_id>',
                     resource_class_args=[app.logger, transactions_svc, account_svc])
    api.add_resource(AccountsApi, '/accounts', '/accounts/<account_id>', resource_class_args=[app.logger, account_svc])

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    return app


def main():
    app = create_app()
    app.run(host="0.0.0.0", port=8080)


if __name__ == '__main__':
    main()
