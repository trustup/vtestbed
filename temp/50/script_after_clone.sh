#!/bin/bash
# logstash
echo adding network interface..
virsh attach-interface --domain logstash_cr50_1_1 --type network --source proxyArp --model rtl8139 --mac 52:54:00:10:ff:60 --config --live
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.3.2 "systemctl enable NetworkManager.service;systemctl start NetworkManager.service;route del default dev eth0;ip route add 50.1.1.2 via 50.1.3.3 dev eth0;ip route add 50.1.2.2 via 50.1.3.3 dev eth0;ip route add 50.1.1.3 via 50.1.3.3 dev eth0;systemctl enable logstash.service; systemctl start logstash.service;su -c 'python3 /home/ubuntu/kafka_consumer.py' - ubuntu &>/dev/null &"
# tankmodel_2
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.1.2 "mkdir /home/ubuntu/tankmodel_2;tar -C /home/ubuntu/tankmodel_2 -xvf /home/ubuntu/tankmodel_2.tar.gz;chmod +x /home/ubuntu/script.sh;/home/ubuntu/script.sh &>/dev/null &"
# plc1
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.1.3 "mv /home/ubuntu/filebeat_plc1.yml /etc/filebeat/filebeat.yml;chown root /etc/filebeat/filebeat.yml;chmod go-w /etc/filebeat/filebeat.yml;service filebeat start;systemctl enable openplc;sleep 5;systemctl start openplc;sleep 5;su -c 'python3 /home/ubuntu/script_selenium_plc1.py' - ubuntu &>/dev/null &"
# mtu-hmi
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.2.2 "mv /home/ubuntu/filebeat_mtu-hmi.yml /etc/filebeat/filebeat.yml;chown root /etc/filebeat/filebeat.yml;chmod go-w /etc/filebeat/filebeat.yml;service filebeat start;mv /home/ubuntu/tankmodel_2.png /var/lib/tomcat7/webapps/ScadaBR/uploads/;systemctl enable tomcat7 &>/dev/null;systemctl start tomcat7 &>/dev/null;sleep 10;su -c 'python3 /home/ubuntu/script_selenium.py' - ubuntu &>/dev/null"
# router-gw
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@50.1.1.4 "sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config;echo 'Match Host 50.1.1.1' >> /etc/ssh/sshd_config;echo '    PermitRootLogin yes' >> /etc/ssh/sshd_config;/etc/init.d/ssh restart;iptables-save > /bin/cyberrange/initif/iptables.conf;"
