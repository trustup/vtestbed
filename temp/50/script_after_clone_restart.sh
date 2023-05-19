#!/bin/bash
# logstash
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.3.2 "systemctl start NetworkManager.service;ip route add 50.1.1.2 via 50.1.3.3 dev eth0;ip route add 50.1.2.2 via 50.1.3.3 dev eth0;ip route add 50.1.1.3 via 50.1.3.3 dev eth0;systemctl start logstash.service;su -c 'python3 /home/ubuntu/kafka_consumer.py' - ubuntu &>/dev/null &"
# tankmodel_2
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.1.2 "route add default gw 50.1.1.4 eth0;/home/ubuntu/script.sh;"
# plc1
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.1.3 "route add default gw 50.1.1.4 eth0;service filebeat start;su -c 'python3 /home/ubuntu/script_selenium_plc1_restart.py' - ubuntu &>/dev/null &"
# mtu-hmi
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.2.2 "route add default gw 50.1.2.3 eth0;service filebeat start;"
# router-gw
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.1.4 "echo 1 > /proc/sys/net/ipv4/ip_forward"
