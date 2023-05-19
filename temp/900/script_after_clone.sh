#!/bin/bash
# logstash
echo adding network interface..
virsh attach-interface --domain logstash_cr900_1_1 --type network --source proxyArp --model rtl8139 --mac 52:54:00:10:ff:60 --config --live
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.3.2 "systemctl enable NetworkManager.service;systemctl start NetworkManager.service;route del default dev eth0;ip route add 900.1.1.2 via 900.1.3.3 dev eth0;ip route add 900.1.2.2 via 900.1.3.3 dev eth0;ip route add 900.1.1.3 via 900.1.3.3 dev eth0;ip route add 900.1.1.4 via 900.1.3.3 dev eth0;ip route add 900.1.1.5 via 900.1.3.3 dev eth0;systemctl enable logstash.service; systemctl start logstash.service;su -c 'python3 /home/ubuntu/kafka_consumer.py' - ubuntu &>/dev/null &"
# aiv_robot
virsh reboot aiv_robot_cr900_1_1 &>/dev/null
sleep 60
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.2 "route delete 0.0.0.0 mask 0.0.0.0"
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.2 "route add 0.0.0.0 mask 0.0.0.0 900.1.1.6"
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.2 "C:\CyberRange\psexec -u root -p theroot -d -s -i 1 C:\CyberRange\script1.bat -accepteula" &>/dev/null
sleep 10
sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no winuser@900.1.1.2 "C:\CyberRange\psexec -u winuser -p shadow -d -s -i 1 C:\CyberRange\script2.bat -accepteula" &>/dev/null
# rtu1
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.3 "python3 /home/ubuntu/code_rtu1.py &>/dev/null &"
# rtu2
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.4 "python3 /home/ubuntu/code_rtu2.py &>/dev/null &"
# plc1
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.5 "mv /home/ubuntu/filebeat_plc1.yml /etc/filebeat/filebeat.yml;chown root /etc/filebeat/filebeat.yml;chmod go-w /etc/filebeat/filebeat.yml;service filebeat start;systemctl enable openplc;sleep 5;systemctl start openplc;sleep 5;su -c 'python3 /home/ubuntu/script_selenium_plc1.py' - ubuntu &>/dev/null &"
# mtu-hmi
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.2.2 "mv /home/ubuntu/aiv_robot.png /var/lib/tomcat7/webapps/ScadaBR/uploads/;systemctl enable tomcat7 &>/dev/null;systemctl start tomcat7 &>/dev/null;sleep 10;su -c 'python3 /home/ubuntu/script_selenium.py' - ubuntu &>/dev/null"
# router-gw
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@900.1.1.6 "sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config;echo 'Match Host 900.1.1.1' >> /etc/ssh/sshd_config;echo '    PermitRootLogin yes' >> /etc/ssh/sshd_config;/etc/init.d/ssh restart;iptables-save > /bin/cyberrange/initif/iptables.conf;"
