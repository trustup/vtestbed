#!/bin/bash
# logstash
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@901.1.3.2 "systemctl start NetworkManager.service;ip route add 901.1.1.2 via 901.1.3.3 dev eth0;ip route add 901.1.2.2 via 901.1.3.3 dev eth0;ip route add 901.1.1.3 via 901.1.3.3 dev eth0;systemctl start logstash.service;su -c 'python3 /home/ubuntu/kafka_consumer.py' - ubuntu &>/dev/null &"
# aiv_robot
sleep 20
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@901.1.1.2 "route delete 0.0.0.0 mask 0.0.0.0"
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@901.1.1.2 "route add 0.0.0.0 mask 0.0.0.0 901.1.1.4"
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@901.1.1.2 "C:\CyberRange\psexec -u root -p theroot -d -s -i 1 C:\CyberRange\script1.bat -accepteula"
sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no winuser@901.1.1.2 "C:\CyberRange\psexec -u winuser -p shadow -d -s -i 1 C:\CyberRange\script2.bat -accepteula"
# plc1
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@901.1.1.3 "route add default gw 901.1.1.4 eth0;service filebeat start;su -c 'python3 /home/ubuntu/script_selenium_plc1_restart.py' - ubuntu &>/dev/null &"
# mtu-hmi
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@901.1.2.2 "route add default gw 901.1.2.3 eth0;service filebeat start;"
# router-gw
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@901.1.1.4 "echo 1 > /proc/sys/net/ipv4/ip_forward"
