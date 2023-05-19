#!/bin/bash
# logstash
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@300.1.3.2 "systemctl start NetworkManager.service;ip route add 300.1.1.2 via 300.1.3.3 dev eth0;ip route add 300.1.2.2 via 300.1.3.3 dev eth0;ip route add 300.1.1.3 via 300.1.3.3 dev eth0;systemctl start logstash.service;su -c 'python3 /home/ubuntu/kafka_consumer.py' - ubuntu &>/dev/null &"
# aiv_robot
sleep 20
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@300.1.1.2 "route delete 0.0.0.0 mask 0.0.0.0"
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@300.1.1.2 "route add 0.0.0.0 mask 0.0.0.0 300.1.1.4"
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@300.1.1.2 "C:\CyberRange\psexec -u root -p theroot -d -s -i 1 C:\CyberRange\script1.bat -accepteula"
sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no winuser@300.1.1.2 "C:\CyberRange\psexec -u winuser -p shadow -d -s -i 1 C:\CyberRange\script2.bat -accepteula"
# plc1
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@300.1.1.3 "route add default gw 300.1.1.4 eth0;su -c 'python3 /home/ubuntu/script_selenium_plc1_restart.py' - ubuntu;service filebeat start; &>/dev/null &"
# mtu-hmi
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@300.1.2.2 "route add default gw 300.1.2.3 eth0"
# router-gw
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@300.1.1.4 "echo 1 > /proc/sys/net/ipv4/ip_forward"
