#!/bin/bash
cd /home/ubuntu/tankmodel_2/
/home/ubuntu/tankmodel_2/tankmodel_2 -embeddedServer=opc-ua -rt=1 &>/dev/null &
python3 /home/ubuntu/modbus.py &>/dev/null &
su -c 'python3 /home/ubuntu/opc_modbus.py' - ubuntu &>/dev/null &
