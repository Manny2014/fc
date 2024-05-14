from cassandra.cluster import Session

from payments.accounts.exceptions import AccountNotFound,AccountAlreadyExists
from payments.accounts.model import Account
from logging import Logger

class AccountsService():

    def __init__(self, logger: Logger, db_session: Session):
        self.db_session = db_session

        self.logger = logger
        # Create prepared statement
        self.account_lookup_statement = None
        self.account_insert_statement = None

    def create_account(self, account_id, balance) :
        statement = self.get_account_insert_statement()
        result = self.db_session.execute(statement, [account_id, float(balance)])
        if not result.was_applied:
            raise AccountAlreadyExists("Account already exists {account_id}")
        return result

    def get_account(self, account_id) -> Account:
        self.logger.info(f"retrieving account for id {account_id}")

        query = self.get_account_lookup_statement()
        results = self.db_session.execute(query, [account_id]).one()

        self.logger.info(f"results {results}")

        if results is None:
            raise AccountNotFound(f"Account {account_id} not found")
        else:
            account = Account(results[0], results[1])

            self.logger.info(f"retrieved account {account.id} with balance {account.balance}")

            return account

    """
    get_account_lookup_statement: Lazy creation of prepare statement to improve future queries.
    """

    def get_account_lookup_statement(self) -> str:
        if self.account_lookup_statement is None:
            self.account_lookup_statement = self.db_session.prepare('SELECT id, balance FROM accounts WHERE id=?')

        return self.account_lookup_statement

    """
    get_account_insert_statement: Lazy creation of prepare statement to improve future queries.
    """
    def get_account_insert_statement(self) -> str:
        if self.account_insert_statement is None:
            self.account_insert_statement = self.db_session.prepare('INSERT INTO accounts (id, balance) VALUES (?, ?) IF NOT EXISTS')
        return self.account_insert_statement