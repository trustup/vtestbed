def filebeat(vm, vm_os, log_type, ip_exp, port_kafka, port_beats, path_temp_script):

    log_type = log_type.split(",")
    type = []
    path = []
    tags = []
    for idx, x in enumerate(log_type):
        if x == 'login':
            if vm_os == 'ubuntu':
                type.append('log')
                path.append('/var/log/auth.log')
                tags.append("login")
        if x == 'tomcat':
            if vm_os == 'ubuntu':
                type.append('log')
                path.append('/var/log/tomcat8/mango.log')
                tags.append("mango")

    with open(r'{}/filebeat_{}.yml'.format(path_temp_script,vm), 'w') as f:
        f.write('filebeat.inputs:\n\n')
        for idx, x in enumerate(type):
            f.write('- type: {}\n'.format(x))
            f.write('  enabled: true\n')
            f.write('  paths:\n')
            f.write('    - {}\n'.format(path[idx]))
            f.write('  tags: ["{}"]'.format(tags[idx]))
            f.write('\n')

        f.write('\nfilebeat.config.modules:\n')
        f.write('  path: ${path.config}/modules.d/*.yml\n')
        f.write('  reload.enables: false\n')

        f.write('\nsetup.template.settings:\n')
        f.write('  index.number_of_shards: 1\n')

        f.write('\nsetup.kibana:\n')

        f.write('\noutput.logstash:\n')
        f.write('  hosts: ["{}:{}"]\n'.format(ip_exp, port_beats))



    f.close()
