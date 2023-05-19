from kafka import KafkaProducer
from time import sleep
import json
import os

#initialize a new kafka producer
producer = KafkaProducer(bootstrap_servers=['192.168.1.188:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

#for e in range(1):
#    data = {'model' : 'start'}
#    a = producer.send('testbed', value=data)
#    print('sending message..')
#    sleep(1)

for e in range(1):
    with open('/home/ubuntu/Scrivania/commands.json') as f:
        stread = json.load(f)
    print(stread)
    id = 100
    name = 'plc1'
    action_type = 'update_firmware'
    command = 'enable'
    data = {'{}'.format(id) : {'asset_id': id,'asset_name': name,
                               'actions': [{'action_type': action_type, 'commands': [{'action_name': command}]
                                            }]
                               }}
    #a = producer.send('testbed', value=data)
    print('sending message..')
    sleep(1)
    print(data)


#data = {'plc' : 'start'}
#a = producer.send('numtest', value=data)

