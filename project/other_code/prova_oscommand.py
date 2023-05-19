import os
import json
import socket
import sys
import yaml

#print("You can connect via SSH using: ")
#os.system("grep -r 'Login' /home/ubuntu/cyris/cyber_range/123/range_notification-cr123.txt")
#os.system("grep -r 'Password' /home/ubuntu/cyris/cyber_range/123/range_notification-cr123.txt")

#with open("/home/ubuntu/data_min.json") as json_file :
#    data = json.loads(json_file.read())
#    print(data)
import numpy as np

d = 'a,b,c'
a = d.replace(", ",",").split(",")
print(a)

for idx, x in enumerate(a):
    print(idx,x)

# data = []
# data.append(10)
# print(data)

# dtt = []
# dtt.append(1.0)
# dtt.append(2.0)
# dtt.append(3.0)
# print('a',dtt)
# for x in dtt:
#     print(x)

# data2 = []
# for x in range(2):
#     data2.append({'a':'b'})
#     data2.append({'c':'d'})
#
#
# for x in range(4):
#     exec(f'cat_{x} = 2')
# print(cat_0)

word = 'geeks for geeks'
if (word.find('geeks') != -1):
    print ("Contains given substring ")
else:
    print ("Doesn't contains given substring")

prv  = {'id': 1, 'basevm_host': 'host_1',
           'tasks': [{'copy_content': [
               {'src': 2, 'dst': '{}'},
               {'src': '{}/PycharmProjects/temp/opc_{}.py',
                'dst': '{}'}
           ]}]
           }

prv['tasks'][0]['copy_content'].append({'ciao':'ciao'})
print(prv['tasks'][0]['copy_content'])


len = 10

aaa = np.arange(0,len,2)
print(list(aaa))



#with open('/home/ubuntu/PycharmProjects/robot_control.st') as f:
#    stread = f.read()
#st_construct = [{"plcName":"plc1", "name":"robot_control.st","value": '{}'.format(stread)}]

#print(st_construct[0]['value'])


#st = [{"plcName":"plc1","name":"robot_control.st","value":"FUNCTION function1 : BOOL\n  VAR_INPUT\n    LOWWORD : UINT;\n    HIGHWORD : UINT;\n  END_VAR\n  VAR_OUTPUT\n    WORDSTOREAL : REAL;\n  END_VAR\n\n  {{\n  union words_to_real {\n  uint16_t i[2];\n  float f;\n  }w2r;\n  w2r.i[0] = LOWWORD;\n  w2r.i[1] = HIGHWORD;\n  WORDSTOREAL = w2r.f;\n  }}\nEND_FUNCTION\n\nFUNCTION_BLOCK control\n  VAR_INPUT\n    VALORE : REAL;\n    VALORE2 : REAL;\n  END_VAR\n  VAR_OUTPUT\n    controll : REAL;\n  END_VAR\n\n  IF (VALORE = 0.0 and VALORE2 = 0.0) THEN\n    controll := 1.0;\n  ELSIF (VALORE = 0.0 and VALORE2 = 1.0) THEN\n    controll := 0.0;\n  ELSIF (VALORE = 1.0 and VALORE2 = 1.0) THEN\n    controll := 1.0;\n  END_IF; \nEND_FUNCTION_BLOCK\n\nFUNCTION prova : BOOL\n  VAR_INPUT\n    INPP : REAL;\n  END_VAR\n  VAR_OUTPUT\n    LOWW : UINT;\n    HIGG : UINT;\n  END_VAR\n\n  {{\n  union real_to_words {\n  uint16_t i[2];\n  float f;\n  }r2w;\n  r2w.f = INPP;\n  LOWW = r2w.i[0];\n  HIGG = r2w.i[1];\n  }}\nEND_FUNCTION\n\nPROGRAM robot\n  VAR\n    STATE_STATION_w1 AT %IW100 : UINT;\n    STATION_w1 AT %IW102 : UINT;\n    STATION_w2 AT %IW103 : UINT;\n    STATE_STATION_w2 AT %IW101 : UINT;\n    WORD3 AT %MD0 : REAL;\n    WORD6 AT %MD1 : REAL;\n    ROBOT_STATE_w1 AT %QW100 : UINT;\n    ROBOT_STATE_w2 AT %QW101 : UINT;\n  END_VAR\n  VAR\n    control0 : control;\n    function18_OUT : BOOL;\n    function18_WORDSTOREAL : REAL;\n    function116_OUT : BOOL;\n    function116_WORDSTOREAL : REAL;\n    prova9_OUT : BOOL;\n    prova9_LOWW : UINT;\n    prova9_HIGG : UINT;\n  END_VAR\n\n  function18_OUT := function1(LOWWORD := STATE_STATION_w2, HIGHWORD := STATE_STATION_w1, WORDSTOREAL => function18_WORDSTOREAL);\n  WORD3 := function18_WORDSTOREAL;\n  function116_OUT := function1(LOWWORD := STATION_w2, HIGHWORD := STATION_w1, WORDSTOREAL => function116_WORDSTOREAL);\n  control0(VALORE := function18_WORDSTOREAL, VALORE2 := function116_WORDSTOREAL);\n  prova9_OUT := prova(INPP := control0.controll, LOWW => prova9_LOWW, HIGG => prova9_HIGG);\n  ROBOT_STATE_w2 := prova9_LOWW;\n  ROBOT_STATE_w1 := prova9_HIGG;\n  WORD6 := function116_WORDSTOREAL;\nEND_PROGRAM\n\n\nCONFIGURATION Config0\n\n  RESOURCE Res0 ON PLC\n    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);\n    PROGRAM instance0 WITH task0 : robot;\n  END_RESOURCE\nEND_CONFIGURATION\n"}]
#st2 = [{'plcName': 'plc1', 'name': 'robot_control.st', 'value': 'FUNCTION function1 : BOOL\n  VAR_INPUT\n    LOWWORD : UINT;\n    HIGHWORD : UINT;\n  END_VAR\n  VAR_OUTPUT\n    WORDSTOREAL : REAL;\n  END_VAR\n\n  {{\n  union words_to_real {\n  uint16_t i[2];\n  float f;\n  }w2r;\n  w2r.i[0] = LOWWORD;\n  w2r.i[1] = HIGHWORD;\n  WORDSTOREAL = w2r.f;\n  }}\nEND_FUNCTION\n\nFUNCTION_BLOCK control\n  VAR_INPUT\n    VALORE : REAL;\n    VALORE2 : REAL;\n  END_VAR\n  VAR_OUTPUT\n    controll : REAL;\n  END_VAR\n\n  IF (VALORE = 0.0 and VALORE2 = 0.0) THEN\n    controll := 1.0;\n  ELSIF (VALORE = 0.0 and VALORE2 = 1.0) THEN\n    controll := 0.0;\n  ELSIF (VALORE = 1.0 and VALORE2 = 1.0) THEN\n    controll := 1.0;\n  END_IF; \nEND_FUNCTION_BLOCK\n\nFUNCTION prova : BOOL\n  VAR_INPUT\n    INPP : REAL;\n  END_VAR\n  VAR_OUTPUT\n    LOWW : UINT;\n    HIGG : UINT;\n  END_VAR\n\n  {{\n  union real_to_words {\n  uint16_t i[2];\n  float f;\n  }r2w;\n  r2w.f = INPP;\n  LOWW = r2w.i[0];\n  HIGG = r2w.i[1];\n  }}\nEND_FUNCTION\n\nPROGRAM robot\n  VAR\n    STATE_STATION_w1 AT %IW100 : UINT;\n    STATION_w1 AT %IW102 : UINT;\n    STATION_w2 AT %IW103 : UINT;\n    STATE_STATION_w2 AT %IW101 : UINT;\n    WORD3 AT %MD0 : REAL;\n    WORD6 AT %MD1 : REAL;\n    ROBOT_STATE_w1 AT %QW100 : UINT;\n    ROBOT_STATE_w2 AT %QW101 : UINT;\n  END_VAR\n  VAR\n    control0 : control;\n    function18_OUT : BOOL;\n    function18_WORDSTOREAL : REAL;\n    function116_OUT : BOOL;\n    function116_WORDSTOREAL : REAL;\n    prova9_OUT : BOOL;\n    prova9_LOWW : UINT;\n    prova9_HIGG : UINT;\n  END_VAR\n\n  function18_OUT := function1(LOWWORD := STATE_STATION_w2, HIGHWORD := STATE_STATION_w1, WORDSTOREAL => function18_WORDSTOREAL);\n  WORD3 := function18_WORDSTOREAL;\n  function116_OUT := function1(LOWWORD := STATION_w2, HIGHWORD := STATION_w1, WORDSTOREAL => function116_WORDSTOREAL);\n  control0(VALORE := function18_WORDSTOREAL, VALORE2 := function116_WORDSTOREAL);\n  prova9_OUT := prova(INPP := control0.controll, LOWW => prova9_LOWW, HIGG => prova9_HIGG);\n  ROBOT_STATE_w2 := prova9_LOWW;\n  ROBOT_STATE_w1 := prova9_HIGG;\n  WORD6 := function116_WORDSTOREAL;\nEND_PROGRAM\n\n\nCONFIGURATION Config0\n\n  RESOURCE Res0 ON PLC\n    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);\n    PROGRAM instance0 WITH task0 : robot;\n  END_RESOURCE\nEND_CONFIGURATION\n'}]

#print(st2['value'])

diction = {'plc': 'start'}

print(diction['plc'])

com2 = r'\"ciao\"'
com = "sed -i 'ciao={}'".format(com2)
prova = 'sshpass ubuntu@ciao  "{}" '.format(com)
print(prova)



#var = '[{"plcName":"Node_6","name":"double_control.st","value":"FUNCTION function1 : BOOL\\r\\n  VAR_INPUT\\r\\n    LOWWORD : UINT;\\r\\n    HIGHWORD : UINT;\\r\\n  END_VAR\\r\\n  VAR_OUTPUT\\r\\n"}]'
#aeeeee=eval(var)
#if type(var) == str : print('okke')
#for isx, stt in enumerate(aeeeee):
#    print(stt['value'])


with open('/home/ubuntu/Scaricati/comandi.json') as f:
    stread = json.load(f)
print(stread['108'])
for x in range(3):
    try:
        print(stread['108']['actions'][x]['action_type'])
    except:
        continue

#json_rec= {'100': {'asset_id': 100, 'asset_name': 'AIV1_PLC', 'actions': [{'action_type': 'power_management', 'commands': [{'action_name': 'stop'}]}]}}

#print(json_rec['100']['actions'][0]['commands'][0]['action_name'])


#VERIFY FILE EXIST
#image_prova = os.path.isfile('/home/ubuntu/cyris/models/matlab/aiv_robot/aiv_robot2.png')
#if image_prova == False:
#    os.system('cp /home/ubuntu/cyris/models/generic.png /home/ubuntu/cyris/models/matlab/aiv_robot/aiv.png')




hostname = socket.gethostname()
ip_address = socket.gethostbyname_ex(socket.gethostname())[-1]
print(ip_address)


def provaa(*argg):
    if argg:
        print(argg[0])
    else:
        print("no argg")


with open(r'{}'.format(sys.argv[1])) as f:
    data = yaml.safe_load(f)

print(data)