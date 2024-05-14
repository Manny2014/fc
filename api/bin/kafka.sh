

docker exec -it broker1 bash -c 'kafka-topics.sh --create --bootstrap-server localhost:9092 --topic transactions --partitions 1'
