#!/bin/bash
# robot
echo 'preparing scenario..'
virsh reboot robot_cr123_1_1
sleep 60
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@123.1.1.2 "C:\CyberRange\psexec -u root -p theroot -d -s -i 1 C:\CyberRange\script1.bat -accepteula"
sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no winuser@123.1.1.2 "C:\CyberRange\psexec -u winuser -p shadow -d -s -i 1 C:\CyberRange\script2.bat -accepteula"
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@123.1.1.2 "route delete 0.0.0.0 mask 0.0.0.0"
sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@123.1.1.2 "route add 0.0.0.0 mask 0.0.0.0 123.1.1.3"
echo 'completed'
