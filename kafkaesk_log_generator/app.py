import kafkaesk
import os

kafka_servers = os.environ.get("KAFKA_SERVERS", "localhost:9092").split(",")

app = kafkaesk.Application(kafka_servers=kafka_servers)
