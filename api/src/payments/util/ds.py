import faker
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from faker import Faker
from kafka.admin import KafkaAdminClient, NewTopic

class DatasourceUtil(object):

    def __init__(self,
                 db_hosts=["localhost"],
                 db_port=9042,
                 keyspace="payments",
                 kafka_brokers=["localhost:9042"]):

        self.keyspace = keyspace
        self.cluster = Cluster(contact_points=db_hosts, port=db_port)
        self.session = self.cluster.connect()
        self.kafka_brokers = kafka_brokers

    def get_session(self):
        return self.session

    def initialize(self, dev_mode=False):

        try:
            self.create_keyspace(self.keyspace)
        except Exception as e:
            # TODO: Circle back
            print(e)

        self.session.set_keyspace(self.keyspace)

        # Create tables
        try:
            self.create_tables()
        except Exception as e:
            # TODO: Circle back
            print(e)

        # Create kafka topics
        try:
            self.create_topics()
        except Exception as e:
            print(e)

        # Create test data
        if dev_mode:
            self.gen_test_data()

    def create_tables(self):
        self.create_accounts_table()
        self.create_failed_transactions_table()

    def create_accounts_table(self, seed=False):
        try:
            self.session.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id TEXT PRIMARY KEY,
                    balance FLOAT
                );
            ''')
        except Exception as e:
            print(e)

    def create_failed_transactions_table(self):
        try:
            self.session.execute("""
                CREATE TABLE IF NOT EXISTS failed_transactions (
                    id TEXT PRIMARY KEY,
                    from_account_id TEXT,
                    to_account_id TEXT,
                    amount FLOAT,
                    reason TEXT
                );
            """)
        except Exception as e:
            print(e)

    def create_keyspace(self, keyspace):
        try:
            self.session.execute("""
                CREATE KEYSPACE IF NOT EXISTS %s
                WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
                AND durable_writes = 'true'
                """ % keyspace)
        except Exception as e:
            print(e)
    def gen_test_data(self):
        for i in range(25):
            f = faker.Faker()
            uuid = f.uuid4()

            batch = """
            INSERT INTO accounts (id, balance)
            VALUES ('{id}', {balance}) IF NOT EXISTS;
            """.format(id=f"{uuid}", balance=f.random_number(4))
            try:
                self.session.execute(batch)
            except Exception as e:
                print(str(e))
                continue

    def create_topics(self):
        admin_client = KafkaAdminClient(
            bootstrap_servers=self.kafka_brokers,
            client_id='dv-mode'
        )
        # TODO: In a REAL cluster the replication factor would at least 3
        admin_client.create_topics([NewTopic("transactions",num_partitions=10, replication_factor=1)])


    def drop_keyspace(self):
        self.session.execute("DROP KEYSPACE IF EXISTS" + self.keyspace)
