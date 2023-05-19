#!/bin/bash
# logstash
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.3.2 "systemctl start NetworkManager.service;ip route add 900.1.1.2 via 900.1.3.3 dev eth0;ip route add 900.1.2.2 via 900.1.3.3 dev eth0;ip route add 900.1.1.3 via 900.1.3.3 dev eth0;ip route add 900.1.1.4 via 900.1.3.3 dev eth0;ip route add 900.1.1.5 via 900.1.3.3 dev eth0;systemctl start logstash.service;su -c 'python3 /home/ubuntu/kafka_consumer.py' - ubuntu &>/dev/null &"
# aiv_robot
sleep 20
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.2 "route delete 0.0.0.0 mask 0.0.0.0"
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.2 "route add 0.0.0.0 mask 0.0.0.0 900.1.1.6"
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.2 "C:\CyberRange\psexec -u root -p theroot -d -s -i 1 C:\CyberRange\script1.bat -accepteula"
sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no winuser@900.1.1.2 "C:\CyberRange\psexec -u winuser -p shadow -d -s -i 1 C:\CyberRange\script2.bat -accepteula"
# rtu1
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.3 "route add default gw 900.1.1.6 eth0;python3 /home/ubuntu/code_rtu1.py &>/dev/null &"
# rtu2
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.4 "route add default gw 900.1.1.6 eth0;python3 /home/ubuntu/code_rtu2.py &>/dev/null &"
# plc1
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.5 "route add default gw 900.1.1.6 eth0;su -c 'python3 /home/ubuntu/script_selenium_plc1_restart.py' - ubuntu;service filebeat start; &>/dev/null &"
# mtu-hmi
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.2.2 "route add default gw 900.1.2.3 eth0"
# router-gw
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.6 "echo 1 > /proc/sys/net/ipv4/ip_forward"
