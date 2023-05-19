import operations
def script_after_clone(vulnerability, vm_target, ip_list, rtu, plc, model, model_os, mtu, hmi, hmi_os, firewall, generic, export, read_topic, topic, source_log, total_vm, dst_script_ubuntu, dst_script_windows, numb_cyber, path_temp_script):
    #creds ubuntu
    ubx = ['root','ubuntu']
    ubx_pss = ['theroot','shadow']
    wx = ['root','winuser']
    wx_pss = ['theroot','shadow']


    # manage security level
    vuln = []
    target = []
    fix = []
    if vulnerability != None:
    #if len(vulnerability) != 0:
        vuln = vulnerability.replace(" ", "").split(";")
        target = vm_target.replace(" ", "").split(";")
        for idx, x in enumerate(vuln):
            if x == 'ssh_root_deny':
                fix.append("sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config;echo 'Match Host {}.1.1.1' >> /etc/ssh/sshd_config;echo '    PermitRootLogin yes' >> /etc/ssh/sshd_config;/etc/init.d/ssh restart".format(numb_cyber))
            elif x == 'altra':
                fix.append('comando fix 2')


    def check_target(insert_target):
        if len(vuln) != 0:
            command = ''
            for idx, x in enumerate(vuln):
                tmp = target[idx].split(",")
                for x in tmp:
                    if insert_target == x:
                        tt = fix[idx] + ";"
                    else:
                        continue
                    command = command + tt
            return command

    ####### AFTER CLONE #######
    with open(r'{}/script_after_clone.sh'.format(path_temp_script), 'w') as f:
        f.write("#!/bin/bash\n")

        #LOGSTASH - UBUNTU
        if export != None:
        #if len(export) != 0:
            f.write("# {}\n".format(export))
            f.write('echo adding network interface..\n')
            f.write('virsh attach-interface --domain {}_cr{}_1_1 --type network --source proxyArp --model rtl8139 --mac 52:54:00:10:ff:60 --config --live\n'.format(export, numb_cyber))
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
            f.write("{}@{} ".format(ubx[0], ip_list[export + '.eth0'][0]))
            f.write('"systemctl enable NetworkManager.service;systemctl start NetworkManager.service;')
            f.write('route del default dev eth0;')
            for x in total_vm:
                f.write('ip route add {} via {} dev eth0;'.format(ip_list[x + '.eth0'][0], ip_list[export + '.eth0'][1]))
            f.write('systemctl enable logstash.service; systemctl start logstash.service')
            if read_topic != None:
                f.write(";su -c 'python3 {}kafka_consumer.py' - ubuntu &>/dev/null &".format(dst_script_ubuntu))
            f.write('"\n')

        # MODEL, CASE WINDOWS - UBUNTU
        if model_os[0] == 'windows.7':
            # f.write("# {}\n".format(model[0]))
            # f.write("sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            # f.write("seven@{} ".format(ip_list[model[0] + '.eth0'][0]))
            # f.write('"')
            # f.write("cd C:\CyberRange && unzip -o {}.zip -d C:\CyberRange\modelica && copy /y diagslave.exe C:\CyberRange\modelica && copy /y opc_modbus.py C:\CyberRange\modelica".format(model[0]))
            # f.write('"\n')
            # f.write("sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            # f.write("seven@{} ".format(ip_list[model[0] + '.eth0'][0]))
            # f.write('"')
            # f.write(
            #     r"C:\CyberRange\psexec \\\\{} -d -i C:\CyberRange\script.bat".format(ip_list[model[0] + '.eth0'][0]))
            # f.write('"\n')
            f.write("# {}\n".format(model[0]))
            f.write('virsh reboot {}_cr{}_1_1 &>/dev/null\n'.format(model[0], numb_cyber))
            f.write('sleep 60\n')
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(wx_pss[0]))
            f.write("{}@{} ".format(wx[0], ip_list[model[0] + '.eth0'][0]))
            f.write('"route delete 0.0.0.0 mask 0.0.0.0"\n')
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(wx_pss[0]))
            f.write("{}@{} ".format(wx[0], ip_list[model[0] + '.eth0'][0]))
            f.write('"route add 0.0.0.0 mask 0.0.0.0 {}"\n'.format(ip_list[model[0] + '.eth0'][1]))
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(wx_pss[0]))
            f.write("{}@{} ".format(wx[0], ip_list[model[0] + '.eth0'][0]))
            f.write('"')
            f.write('C:\CyberRange\psexec -u {} -p {} -d -s -i 1 {}\script1.bat -accepteula'.format(wx[0], wx_pss[0], dst_script_windows))
            f.write('"')
            f.write(' &>/dev/null\n')
            f.write("sleep 10\n")
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(wx_pss[1]))
            f.write("{}@{} ".format(wx[1], ip_list[model[0] + '.eth0'][0]))
            f.write('"')
            f.write('C:\CyberRange\psexec -u {} -p {} -d -s -i 1 {}\script2.bat -accepteula'.format(wx[1], wx_pss[1], dst_script_windows))
            f.write('"')
            f.write(' &>/dev/null\n')

        else:
            f.write("# {}\n".format(model[0]))
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
            f.write("{}@{} ".format(ubx[0], ip_list[model[0] + '.eth0'][0]))
            # f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
            f.write('"')
            if topic != None and operations.control_source_log(model[0], source_log) == True:
                f.write('mv {}filebeat_{}.yml /etc/filebeat/filebeat.yml;'.format(dst_script_ubuntu, model[0]))
                f.write('chown root /etc/filebeat/filebeat.yml;')
                f.write('chmod go-w /etc/filebeat/filebeat.yml;')
                f.write('service filebeat start;')
            ck = check_target(model[0])
            if ck != None: f.write(ck)
            f.write("mkdir /home/ubuntu/{};".format(model[0]))
            f.write("tar -C {}{} -xvf {}{}.tar.gz;".format(dst_script_ubuntu, model[0], dst_script_ubuntu, model[0]))
            f.write('chmod +x /home/ubuntu/script.sh;')
            f.write('/home/ubuntu/script.sh &>/dev/null &')
            f.write('"\n')

        if len(rtu) != 0:
            for y in rtu:
                f.write("# {}\n".format(y))
                f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
                f.write("{}@{} ".format(ubx[0], ip_list[y + '.eth0'][0]))
                # f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
                f.write('"')
                if topic != None and operations.control_source_log(y, source_log) == True:
                    f.write('mv {}filebeat_{}.yml /etc/filebeat/filebeat.yml;'.format(dst_script_ubuntu, y))
                    f.write('chown root /etc/filebeat/filebeat.yml;')
                    f.write('chmod go-w /etc/filebeat/filebeat.yml;')
                    f.write('service filebeat start;')
                ck = check_target(y)
                if ck != None: f.write(ck)
                #f.write("{}diagslave -m tcp".format(dst_script_ubuntu))
                f.write('python3 {}code_{}.py'.format(dst_script_ubuntu,y))
                f.write(" &>/dev/null &")
                f.write('"\n')

        if len(plc) != 0:
            for idx, y in enumerate(plc):
                f.write("# {}\n".format(y))
                f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
                f.write("{}@{} ".format(ubx[0], ip_list[y + '.eth0'][0]))
                f.write('"')
                if topic != None and operations.control_source_log(y, source_log) == True:
                    f.write('mv {}filebeat_{}.yml /etc/filebeat/filebeat.yml;'.format(dst_script_ubuntu, y))
                    f.write('chown root /etc/filebeat/filebeat.yml;')
                    f.write('chmod go-w /etc/filebeat/filebeat.yml;')
                    f.write('service filebeat start;')
                ck = check_target(y)
                if ck != None: f.write(ck)
                #f.write("/bin/cyberrange/OpenPLC_v3/start_openplc.sh;")
                f.write("systemctl enable openplc;sleep 5;systemctl start openplc;sleep 5;")
                f.write("su -c 'python3 /home/ubuntu/script_selenium_plc{}.py' - ubuntu".format(idx + 1))
                f.write(" &>/dev/null &")
                f.write('"\n')


        # MTU, CASE WINDOWS - UBUNTU
        if hmi_os[0] == 'windows.7':
            f.write("# {}\n".format(mtu[0]))
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(wx_pss[1]))
            f.write("seven@{} ".format(ip_list[mtu[0] + '.eth0'][0]))
            f.write("'")
            f.write('move {}\{}.png "C:\Program Files\ScadaBR\webapps\ScadaBR\\uploads"'.format(dst_script_windows, model[0]))
            f.write(' && cd {} && python script_selenium.py'.format(dst_script_windows))
            f.write("'\n")
        else:
            f.write("# {}\n".format(mtu[0]))
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
            f.write("{}@{} ".format(ubx[0], ip_list[mtu[0] + '.eth0'][0]))
            # f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
            f.write('"')
            if topic != None and operations.control_source_log(mtu[0], source_log) == True:
                f.write('mv {}filebeat_{}.yml /etc/filebeat/filebeat.yml;'.format(dst_script_ubuntu, mtu[0]))
                f.write('chown root /etc/filebeat/filebeat.yml;')
                f.write('chmod go-w /etc/filebeat/filebeat.yml;')
                f.write('service filebeat start;')
            ck = check_target(mtu[0])
            if ck != None: f.write(ck)
            if hmi[0] == 'scadabr':
                f.write('mv {}{}.png /var/lib/tomcat7/webapps/ScadaBR/uploads/;'.format(dst_script_ubuntu, model[0]))
                f.write('systemctl enable tomcat7 &>/dev/null;systemctl start tomcat7 &>/dev/null;sleep 10;')
                # f.write('"su -c')
                f.write("su -c 'python3 /home/ubuntu/script_selenium.py' - ubuntu")
                f.write(' &>/dev/null')
            f.write('"\n')


        for y in firewall:
            f.write("# {}\n".format(y))
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
            f.write("{}@{} ".format(ubx[0], ip_list[y + '.eth0'][0]))
            # f.write('"echo 1 > /proc/sys/net/ipv4/ip_forward;')
            # f.write('"iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;iptables -P FORWARD ACCEPT"')
            f.write('"')
            if topic != None and operations.control_source_log(y, source_log) == True:
                f.write('mv {}filebeat_{}.yml /etc/filebeat/filebeat.yml;'.format(dst_script_ubuntu, y))
                f.write('chown root /etc/filebeat/filebeat.yml;')
                f.write('chmod go-w /etc/filebeat/filebeat.yml;')
                f.write('service filebeat start;')
            ck = check_target(y)
            if ck != None: f.write(ck)
            f.write("iptables-save > /bin/cyberrange/initif/iptables.conf;")
            # if sec_lev != 'low':
            #     f.write("sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config;")
            #     f.write("echo 'Match Host 100.1.1.1' >> /etc/ssh/sshd_config;")
            #     f.write("echo '    PermitRootLogin yes' >> /etc/ssh/sshd_config;/etc/init.d/ssh restart")
            f.write('"')
            f.write("\n")
    f.close()

    ####################################################################################################################
    ####### RESTART #######
    with open(r'{}/script_after_clone_restart.sh'.format(path_temp_script), 'w') as f:
        f.write("#!/bin/bash\n")

        #LOGSTASH - UBUNTU
        if export != None:
        #if len(export) != 0:
            f.write("# {}\n".format(export))
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
            f.write("{}@{} ".format(ubx[0], ip_list[export + '.eth0'][0]))
            f.write('"')
            f.write('systemctl start NetworkManager.service;')
            for x in total_vm:
                f.write('ip route add {} via {} dev eth0;'.format(ip_list[x + '.eth0'][0], ip_list[export + '.eth0'][1]))
            f.write('systemctl start logstash.service')
            if read_topic != None:
                f.write(";su -c 'python3 {}kafka_consumer.py' - ubuntu &>/dev/null &".format(dst_script_ubuntu))
            f.write('"\n')

        # MODEL RESTART - WINDOWS,UBUNTU
        if model_os[0] == 'windows.7':
            # f.write("# {}\n".format(model[0]))
            # f.write('sleep 20\n')
            # f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            # f.write("root@{} ".format(ip_list[model[0] + '.eth0'][0]))
            # f.write('"route delete 0.0.0.0 mask 0.0.0.0"\n')
            # f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            # f.write("root@{} ".format(ip_list[model[0] + '.eth0'][0]))
            # f.write('"route add 0.0.0.0 mask 0.0.0.0 {}"\n'.format(ip_list[model[0] + '.eth0'][1]))
            # f.write("sshpass -p shadow ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            # f.write("seven@{} ".format(ip_list[model[0] + '.eth0'][0]))
            # f.write('"')
            # f.write(
            #     r"C:\CyberRange\psexec \\\\{} -d -i C:\CyberRange\script.bat".format(ip_list[model[0] + '.eth0'][0]))
            # f.write('"\n')
            f.write("# {}\n".format(model[0]))
            f.write('sleep 20\n')
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(wx_pss[0]))
            f.write("{}@{} ".format(wx[0], ip_list[model[0] + '.eth0'][0]))
            f.write('"route delete 0.0.0.0 mask 0.0.0.0"\n')
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(wx_pss[0]))
            f.write("{}@{} ".format(wx[0], ip_list[model[0] + '.eth0'][0]))
            f.write('"route add 0.0.0.0 mask 0.0.0.0 {}"\n'.format(ip_list[model[0] + '.eth0'][1]))
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(wx_pss[0]))
            f.write("{}@{} ".format(wx[0], ip_list[model[0] + '.eth0'][0]))
            f.write('"')
            f.write('C:\CyberRange\psexec -u {} -p {} -d -s -i 1 {}\script1.bat -accepteula'.format(wx[0], wx_pss[0], dst_script_windows))
            f.write('"\n')
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(wx_pss[1]))
            f.write("{}@{} ".format(wx[1], ip_list[model[0] + '.eth0'][0]))
            f.write('"')
            f.write('C:\CyberRange\psexec -u {} -p {} -d -s -i 1 {}\script2.bat -accepteula'.format(wx[1], wx_pss[1], dst_script_windows))
            f.write('"\n')
        else: #UBUNTU
            f.write("# {}\n".format(model[0]))
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
            f.write("{}@{} ".format(ubx[0], ip_list[model[0] + '.eth0'][0]))
            f.write('"route add default gw {} eth0;'.format(ip_list[model[0] + '.eth0'][1]))
            # f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
            if topic != None and operations.control_source_log(model[0], source_log) == True:
                f.write('service filebeat start;')
            #f.write('chmod +x /home/ubuntu/script.sh;')
            f.write('/home/ubuntu/script.sh;')
            #f.write('/home/ubuntu/script.sh;nohup python3 /home/ubuntu/opc_modbus.py &>/dev/null &"')
            f.write('"\n')

        if len(rtu) != 0:
            for y in rtu:
                f.write("# {}\n".format(y))
                f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
                f.write("{}@{} ".format(ubx[0] ,ip_list[y + '.eth0'][0]))
                f.write('"route add default gw {} eth0;'.format(ip_list[y + '.eth0'][1]))
                if topic != None and operations.control_source_log(y, source_log) == True:
                    f.write('service filebeat start;')
                # f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;')
                #f.write("{}diagslave -m tcp".format(dst_script_ubuntu))
                f.write('python3 {}code_{}.py'.format(dst_script_ubuntu,y))
                f.write(' &>/dev/null &"\n')

        if len(plc) != 0:
            for y in plc:
                f.write("# {}\n".format(y))
                f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
                f.write("{}@{} ".format(ubx[0], ip_list[y + '.eth0'][0]))
                f.write('"route add default gw {} eth0;'.format(ip_list[y + '.eth0'][1]))
                if topic != None and operations.control_source_log(y, source_log) == True:
                    f.write('service filebeat start;')
                f.write("su -c 'python3 /home/ubuntu/script_selenium_plc{}_restart.py' - ubuntu".format(idx + 1))
                f.write(' &>/dev/null &"\n')


        # MTU RESTART - WINDOWS,UBUNTU
        f.write("# {}\n".format(mtu[0]))
        if hmi_os[0] == 'windows.7':
            f.write('sleep 20\n')
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[mtu[0] + '.eth0'][0]))
            # f.write('"route -p change 0.0.0.0 mask 0.0.0.0 {}'.format(ip_list[mtu[0] + '.eth0'][1]))
            f.write('"route delete 0.0.0.0 mask 0.0.0.0"\n')
            f.write("sshpass -p theroot ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ")
            f.write("root@{} ".format(ip_list[mtu[0] + '.eth0'][0]))
            f.write('"route add 0.0.0.0 mask 0.0.0.0 {}"\n'.format(ip_list[mtu[0] + '.eth0'][1]))
        else:
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
            f.write("{}@{} ".format(ubx[0], ip_list[mtu[0] + '.eth0'][0]))
            f.write('"route add default gw {} eth0'.format(ip_list[mtu[0] + '.eth0'][1]))
            if topic != None and operations.control_source_log(mtu[0], source_log) == True:
                f.write(';service filebeat start;')
            f.write('"\n')

        if len(generic) != 0:
            for y in generic:
                f.write("# {}\n".format(y))
                f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
                f.write("{}@{} ".format(ubx[0], ip_list[y + '.eth0'][0]))
                f.write('"route add default gw {} eth0'.format(ip_list[y + '.eth0'][1]))
                if topic != None and operations.control_source_log(y, source_log) == True:
                    f.write(';service filebeat start;')
                # f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT"')
                f.write('"\n')

        for y in firewall:
            f.write("# {}\n".format(y))
            f.write("sshpass -p {} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ".format(ubx_pss[0]))
            f.write("{}@{} ".format(ubx[0], ip_list[y + '.eth0'][0]))
            f.write('"echo 1 > /proc/sys/net/ipv4/ip_forward')
            if topic != None and operations.control_source_log(y, source_log) == True:
                f.write(';service filebeat start;')
            # f.write('iptables -F;iptables -P INPUT ACCEPT;iptables -P OUTPUT ACCEPT;iptables -P FORWARD ACCEPT"')
            f.write('"\n')
    f.close()
