from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('testbed',
                         bootstrap_servers=['192.168.1.188:9092'],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         auto_commit_interval_ms=1000,
                         group_id = 'my-groyp',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8'))
                         )

#for message in consumer:
#    if list(message[6])[0] == 'plc':
#        if message[6]['plc'] == 'stop':
#            print('stoppo il plc')

for message in consumer:
    if list(message[6])['85']['asset_name'] == 'aiv_robot':
        print('cioa')