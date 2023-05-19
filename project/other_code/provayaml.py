import sys
import yaml
import json
import time
import sys

#with open(r'/home/ubuntu/PycharmProjects/esempio1.yaml') as f:
#    data = yaml.safe_load(f)

#print(data)


data2 = {'MODEL': {'modeler': 'openmodelica', 'name': 'tankmodel', 'os': 'ubuntu', 'interface': 'modbus', 'opc_parameters': {'actuators': 'input1=0, input2=0, PLC=0', 'sensors': 'mainTank.V, secondTank.V, massOverFlow, pressure1'}}, 'MTU': {'name': 'mtu-hmi', 'os': 'ubuntu', 'hmi': 'scadabr', 'set_alert': {'type': None, 'variable': None}}, 'RTU': {'name': None, 'os': None, 'input': None}, 'PLC': {'name': None, 'os': None, 'input': None, 'output_slave': None, 'plc_code': ''}, 'GENERIC': {'name': None, 'os': None}, 'ROUTER_FIREWALL': {'name': 'router-gw', 'os': 'ubuntu', 'forwarding': [{'rules': [{'rule': 'src=internal_2 dst=internal_1'}, {'rule': 'src=internal_1 dst=internal_2'}]}]}, 'NETWORKS': {'name': 'internal_1; internal_2', 'members': 'mtu-hmi; tankmodel', 'gateway': 'router-gw; router-gw'}, 'CONFIG': {'entry_point': 'mtu-hmi', 'cyber_range_id': 150, 'path': '/home/ubuntu'}, 'SECURITY': {'vulnerability': None, 'target': None}, 'EXPORT_DATA': {'name': None, 'ip_server': None, 'source_data': None, 'log_type': None}}
#with open(r'/home/ubuntu/PycharmProjects/provaaaaaaaa.yml', 'w') as file:
#    data_out = yaml.dump(data2, file, sort_keys=False)

#print(data['MODEL']['opc_parameters']['sensors'])

#print(data['ROUTER_FIREWALL'])

#import subprocess
from subprocess import Popen

#try:
#    subprocess.run("virsh start tankmodel_cr150_1_1", shell=True)
#except subprocess.CalledProcessError as e:
#    print("ciao")

#res = subprocess.Popen("virsh start tankmodel2_cr150_1_1",stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8" ,shell=True)
#if res.wait() != 0:
#    output, error = res.communicate()
#    print("ciao",error)


#LEGGERE FILE
# with open(r'/home/ubuntu/PycharmProjects/temp/35/prova.st', newline='\r') as f:
#     data = f.read()
#
# with open(r'/home/ubuntu/cyris/PLC/1/double_control.st') as f:
#     data2 = f.read()

#print(data2)


#-----------------------------------------------------------------------------------------

# stringa = "'FUNCTION function1 : 'BOOL\r\n  VAR_INPUT\r\n    LOWWORD : UINT;\r\n    HIGHWORD: UINT;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    WORDSTOREAL : REAL;\r\n  END_VAR\r\n\r\n'"
# stringa=stringa.replace("'","",1)
# stringa=stringa[:-1]
#
# print(stringa)
#
# with open('/home/ubuntu/cyris/PLC/1/provaaa.st','w') as f:
#     f.write(stringa)
#
# a = 1.0
# if type(1) == int:
#     a = float(a)
#
# print(a)

#----------------------------------------------------------------------------------------------

filke = [{"plcName":"Node_1","name":"double_control (copy).st","value":"FUNCTION function1 : BOOL\r\n  VAR_INPUT\r\n    LOWWORD : UINT;\r\n    HIGHWORD : UINT;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    WORDSTOREAL : REAL;\r\n  END_VAR\r\n"},{"plcName":"Node_2","name":"double_control.st","value":"FUNCTION function1 : BOOL\r\n  VAR_INPUT\r\n    LOWWORD : UINT;\r\n    HIGHWORD : UINT;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    WORDSTOREAL : REAL;\r\n  END_VAR\r\n\r\n  {{\r\n  union words_to_real {\r\n  uint16_t i[2];\r\n  float f;\r\n  }w2r;\r\n  w2r.i[0] = LOWWORD;\r\n  w2r.i[1] = HIGHWORD;\r\n  WORDSTOREAL = w2r.f;\r\n  }}\r\nEND_FUNCTION\r\n\r\nFUNCTION_BLOCK control\r\n  VAR_INPUT\r\n    VALORE : REAL;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    controll : REAL;\r\n  END_VAR\r\n\r\n  IF (VALORE<1.015) THEN\r\n    controll := 0.0;\r\n  ELSIF (controll = 0.0 and VALORE<2.4) THEN\r\n    controll := 0.0;\r\n  ELSIF (controll = 0.0 and VALORE>2.4) THEN\r\n    controll := 1.0;\r\n  ELSIF (controll =1.0 and VALORE<2.4) THEN\r\n    controll := 1.0;\r\n  END_IF; \r\nEND_FUNCTION_BLOCK\r\n\r\nFUNCTION prova : BOOL\r\n  VAR_INPUT\r\n    INPP : REAL;\r\n  END_VAR\r\n  VAR_OUTPUT\r\n    LOWW : UINT;\r\n    HIGG : UINT;\r\n  END_VAR\r\n\r\n  {{\r\n  union real_to_words {\r\n  uint16_t i[2];\r\n  float f;\r\n  }r2w;\r\n  r2w.f = INPP;\r\n  LOWW = r2w.i[0];\r\n  HIGG = r2w.i[1];\r\n  }}\r\nEND_FUNCTION\r\n\r\nPROGRAM pressure\r\n  VAR\r\n    WORD1 AT %IW100 : UINT;\r\n    WORD2 AT %IW101 : UINT;\r\n    WORD3 AT %MD0 : REAL;\r\n    prova1 AT %QW100 : UINT;\r\n    prova2 AT %QW101 : UINT;\r\n  END_VAR\r\n  VAR\r\n    control0 : control;\r\n    function18_OUT : BOOL;\r\n    function18_WORDSTOREAL : REAL;\r\n    prova9_OUT : BOOL;\r\n    prova9_LOWW : UINT;\r\n    prova9_HIGG : UINT;\r\n  END_VAR\r\n\r\n  function18_OUT := function1(LOWWORD := WORD2, HIGHWORD := WORD1, WORDSTOREAL => function18_WORDSTOREAL);\r\n  WORD3 := function18_WORDSTOREAL;\r\n  control0(VALORE := function18_WORDSTOREAL);\r\n  prova9_OUT := prova(INPP := control0.controll, LOWW => prova9_LOWW, HIGG => prova9_HIGG);\r\n  prova2 := prova9_LOWW;\r\n  prova1 := prova9_HIGG;\r\nEND_PROGRAM\r\n\r\n\r\nCONFIGURATION Config0\r\n\r\n  RESOURCE Res0 ON PLC\r\n    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);\r\n    PROGRAM instance0 WITH task0 : pressure;\r\n  END_RESOURCE\r\nEND_CONFIGURATION\r\n"}]

print(len(filke))
print(filke[0]['plcName'])

for x in filke:
    if x['plcName'] == 'Node_1':
        print('ciaaooo')


file_json = {"id":"9e92d5b0-f0be-46ec-afd1-62895b058cde","offsetX":0,"offsetY":0,"zoom":100,"gridSize":0,"layers":[{"id":"596a7de2-27a6-424c-a275-98bb286bc54f","type":"diagram-links","isSvg":True,"transformed":True,"models":{"a0a9e3f1-acaa-4672-b740-9aec94fa6169":{"id":"a0a9e3f1-acaa-4672-b740-9aec94fa6169","type":"default","selected":False,"source":"611b1abd-9d2b-4339-819b-e85a02108be6","sourcePort":"ea0347ac-f4ac-41ed-8d98-2f9c63bae2ce","target":"b550b544-ca2a-4743-a338-8283fa3521ab","targetPort":"250bdaa7-9a31-4889-b224-fef5ff240ab8","points":[{"id":"14403a27-be14-47d9-8c0f-c7a20600bfeb","type":"point","x":235.54998779296875,"y":173.5},{"id":"10a17ca0-c7ea-4621-8568-a25350d86405","type":"point","x":411.5,"y":159.5}],"labels":[],"width":3,"color":"gray","curvyness":50,"selectedColor":"rgb(0,192,255)"}}},{"id":"a04bdda3-45a6-4c39-b2bf-d72cc4b7448b","type":"diagram-nodes","isSvg":False,"transformed":True,"models":{"611b1abd-9d2b-4339-819b-e85a02108be6":{"id":"611b1abd-9d2b-4339-819b-e85a02108be6","type":"custom-node","x":95,"y":136,"ports":[{"id":"ea0347ac-f4ac-41ed-8d98-2f9c63bae2ce","type":"default","x":228.04998779296875,"y":166,"name":"to_Net","alignment":"right","parentNode":"611b1abd-9d2b-4339-819b-e85a02108be6","links":["a0a9e3f1-acaa-4672-b740-9aec94fa6169"],"in":False,"label":"to_Net"},{"id":"2f3442da-4361-4c40-bb21-2e5034f473a6","type":"default","x":97,"y":166,"name":"Input S/A","alignment":"left","parentNode":"611b1abd-9d2b-4339-819b-e85a02108be6","links":[],"in":True,"label":"Input S/A"}],"name":"Node_1","color":"rgb(0,192,255)","portsInOrder":["2f3442da-4361-4c40-bb21-2e5034f473a6"],"portsOutOrder":["ea0347ac-f4ac-41ed-8d98-2f9c63bae2ce"],"modeler":"Select_Modeler","interface":"Select_Interface","actuators":"None","sensors":"None","nodeType":"RTU","OSystem":"Select_OS","hmi":"Select_HMI","alert":"Select_Alert","PLCCode":"Select_PLCCode","rulesList":[{"src":"","dst":""}],"rulesInfo":{"NetSRC":["SRC Network"],"NetDST":["DST Network"],"HostSRC":["SRC Host"],"HostDST":["DST host"]},"fixList":[],"alertList":[],"arrayOfAlert":[],"exportLog":False,"arrayOfLog":[]},"b550b544-ca2a-4743-a338-8283fa3521ab":{"id":"b550b544-ca2a-4743-a338-8283fa3521ab","type":"custom-node","x":402,"y":122,"ports":[{"id":"250bdaa7-9a31-4889-b224-fef5ff240ab8","type":"default","x":404,"y":152,"name":"net1","alignment":"left","parentNode":"b550b544-ca2a-4743-a338-8283fa3521ab","links":["a0a9e3f1-acaa-4672-b740-9aec94fa6169"],"in":True,"label":"net1"},{"id":"157bdd78-6770-4a22-a756-cbe88fb8c58b","type":"default","x":404,"y":168,"name":"net0","alignment":"left","parentNode":"b550b544-ca2a-4743-a338-8283fa3521ab","links":[],"in":True,"label":"net0"}],"name":"Node_2","color":"rgb(143,0,255)","portsInOrder":["250bdaa7-9a31-4889-b224-fef5ff240ab8","157bdd78-6770-4a22-a756-cbe88fb8c58b"],"portsOutOrder":[],"modeler":"Select_Modeler","interface":"Select_Interface","actuators":"None","sensors":"None","nodeType":"ROUTER","OSystem":"Select_OS","hmi":"Select_HMI","alert":"Select_Alert","PLCCode":"Select_PLCCode","rulesList":[{"src":"","dst":""}],"rulesInfo":{"NetSRC":["SRC Network"],"NetDST":["DST Network"],"HostSRC":["SRC Host"],"HostDST":["DST host"]},"fixList":[],"alertList":[],"arrayOfAlert":[],"exportLog":False,"arrayOfLog":[]}}},{"cyberRangeID":None}]}


jjjj = {'id': '9e92d5b0-f0be-46ec-afd1-62895b058cde', 'offsetX': 32, 'offsetY': -7, 'zoom': 100, 'gridSize': 0, 'layers': [{'id': '596a7de2-27a6-424c-a275-98bb286bc54f', 'type': 'diagram-links', 'isSvg': True, 'transformed': True, 'models': {'a0a9e3f1-acaa-4672-b740-9aec94fa6169': {'id': 'a0a9e3f1-acaa-4672-b740-9aec94fa6169', 'type': 'default', 'selected': False, 'source': '611b1abd-9d2b-4339-819b-e85a02108be6', 'sourcePort': 'ea0347ac-f4ac-41ed-8d98-2f9c63bae2ce', 'target': 'b550b544-ca2a-4743-a338-8283fa3521ab', 'targetPort': '250bdaa7-9a31-4889-b224-fef5ff240ab8', 'points': [{'id': '14403a27-be14-47d9-8c0f-c7a20600bfeb', 'type': 'point', 'x': 235.54998779296875, 'y': 173.5}, {'id': '10a17ca0-c7ea-4621-8568-a25350d86405', 'type': 'point', 'x': 411.5, 'y': 159.5}], 'labels': [], 'width': 3, 'color': 'gray', 'curvyness': 50, 'selectedColor': 'rgb(0,192,255)'}}}, {'id': 'a04bdda3-45a6-4c39-b2bf-d72cc4b7448b', 'type': 'diagram-nodes', 'isSvg': False, 'transformed': True, 'models': {'611b1abd-9d2b-4339-819b-e85a02108be6': {'id': '611b1abd-9d2b-4339-819b-e85a02108be6', 'type': 'custom-node', 'x': 95, 'y': 136, 'ports': [{'id': 'ea0347ac-f4ac-41ed-8d98-2f9c63bae2ce', 'type': 'default', 'x': 228.04998779296875, 'y': 166, 'name': 'to_Net', 'alignment': 'right', 'parentNode': '611b1abd-9d2b-4339-819b-e85a02108be6', 'links': ['a0a9e3f1-acaa-4672-b740-9aec94fa6169'], 'in': False, 'label': 'to_Net'}, {'id': '2f3442da-4361-4c40-bb21-2e5034f473a6', 'type': 'default', 'x': 97, 'y': 166, 'name': 'Input S/A', 'alignment': 'left', 'parentNode': '611b1abd-9d2b-4339-819b-e85a02108be6', 'links': [], 'in': True, 'label': 'Input S/A'}], 'name': 'Node_1', 'color': 'rgb(0,192,255)', 'portsInOrder': ['2f3442da-4361-4c40-bb21-2e5034f473a6'], 'portsOutOrder': ['ea0347ac-f4ac-41ed-8d98-2f9c63bae2ce'], 'modeler': 'Select_Modeler', 'interface': 'Select_Interface', 'actuators': 'None', 'sensors': 'None', 'nodeType': 'RTU', 'OSystem': 'Select_OS', 'hmi': 'Select_HMI', 'alert': 'Select_Alert', 'PLCCode': 'Select_PLCCode', 'rulesList': [{'src': '', 'dst': ''}], 'rulesInfo': {'NetSRC': ['SRC Network'], 'NetDST': ['DST Network'], 'HostSRC': ['SRC Host'], 'HostDST': ['DST host']}, 'fixList': [], 'alertList': [], 'arrayOfAlert': [], 'exportLog': False, 'arrayOfLog': []}, 'b550b544-ca2a-4743-a338-8283fa3521ab': {'id': 'b550b544-ca2a-4743-a338-8283fa3521ab', 'type': 'custom-node', 'x': 402, 'y': 122, 'ports': [{'id': '250bdaa7-9a31-4889-b224-fef5ff240ab8', 'type': 'default', 'x': 404, 'y': 152, 'name': 'net1', 'alignment': 'left', 'parentNode': 'b550b544-ca2a-4743-a338-8283fa3521ab', 'links': ['a0a9e3f1-acaa-4672-b740-9aec94fa6169'], 'in': True, 'label': 'net1'}, {'id': '157bdd78-6770-4a22-a756-cbe88fb8c58b', 'type': 'default', 'x': 404, 'y': 168, 'name': 'net0', 'alignment': 'left', 'parentNode': 'b550b544-ca2a-4743-a338-8283fa3521ab', 'links': [], 'in': True, 'label': 'net0'}], 'name': 'Node_2', 'color': 'rgb(143,0,255)', 'portsInOrder': ['250bdaa7-9a31-4889-b224-fef5ff240ab8', '157bdd78-6770-4a22-a756-cbe88fb8c58b'], 'portsOutOrder': [], 'modeler': 'Select_Modeler', 'interface': 'Select_Interface', 'actuators': 'None', 'sensors': 'None', 'nodeType': 'ROUTER', 'OSystem': 'Select_OS', 'hmi': 'Select_HMI', 'alert': 'Select_Alert', 'PLCCode': 'Select_PLCCode', 'rulesList': [{'src': '', 'dst': ''}], 'rulesInfo': {'NetSRC': ['SRC Network'], 'NetDST': ['DST Network'], 'HostSRC': ['SRC Host'], 'HostDST': ['DST host']}, 'fixList': [], 'alertList': [], 'arrayOfAlert': [], 'exportLog': False, 'arrayOfLog': []}}}, {'cyberRangeID': '20'}]}

print(file_json['layers'][2]['cyberRangeID'])

#formattare come yaml
#with open(r'/home/ubuntu/PycharmProjects/temp/80/values.yml', newline='\r') as f:
#     data = yaml.safe_load(f)
#print(data[4])

print(sys.argv[1])

