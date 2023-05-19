from kafka import KafkaProducer
from time import sleep
import json
import sys

#initialize a new kafka producer
producer = KafkaProducer(bootstrap_servers=['192.168.1.188:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))


for e in range(1):
    with open('{}'.format(sys.argv[1])) as f:
        data = json.load(f)
    a = producer.send('{}'.format(sys.argv[2]), value=data)
    print('sending message..')
    sleep(1)