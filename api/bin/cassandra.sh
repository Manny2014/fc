
# Get all keyspaces
1. SELECT * FROM system_schema.keyspaces;
2. desc keyspaces

# Set keyspace
user payments;

# Create keyspace
#CREATE KEYSPACE fc_payments WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = 'true'

