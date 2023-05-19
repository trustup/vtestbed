def plc_mbconfig(path_temp_script, number_plc, sensors_input, actuators_input, actuators_output, variables, ip_model):


    #CONFIGURATION FILE FOR MODBUS TCP SLAVE
    number_devices = len(sensors_input)+len(actuators_input)
    registers = sensors_input + actuators_input  #registers for reading values
    with open(r'{}/PLC/{}/mbconfig.cfg'.format(path_temp_script, number_plc), 'w') as f:

        f.write('Num_Devices="{}"\n'.format(number_devices))
        f.write('Polling_Period = "100"\n')
        f.write('Timeout = "1000"\n')

        for x in range(number_devices):
            f.write('# ------------\n')
            f.write('   DEVICE {}\n'.format(x))
            f.write('# ------------\n')
            f.write('device{}.name = "{}"\n'.format(x, variables[x]))
            f.write('device{}.slave_id = "1"\n'.format(x))
            f.write('device{}.protocol = "TCP"\n'.format(x))
            f.write('device{}.address = "{}"\n'.format(x, ip_model))
            f.write('device{}.IP_Port = "502"\n'.format(x))
            f.write('device{}.RTU_Baud_Rate = "115200"\n'.format(x))
            f.write('device{}.RTU_Parity = "None"\n'.format(x))
            f.write('device{}.RTU_Data_Bits = "8"\n'.format(x))
            f.write('device{}.RTU_Stop_Bits = "1"\n\n'.format(x))

            f.write('device{}.Discrete_Inputs_Start = "0"\n'.format(x))
            f.write('device{}.Discrete_Inputs_Size = "0"\n'.format(x))
            f.write('device{}.Coils_Start = "0"\n'.format(x))
            f.write('device{}.Coils_Size = "0"\n'.format(x))
            f.write('device{}.Input_Registers_Start = "0"\n'.format(x))
            f.write('device{}.Input_Registers_Size = "0"\n'.format(x))
            f.write('device{}.Holding_Registers_Read_Start = "{}"\n'.format(x, registers[x]))
            f.write('device{}.Holding_Registers_Read_Size = "2"\n'.format(x))
            try:
                f.write('device{}.Holding_Registers_Start = "{}"\n'.format(x, actuators_output[x]))
                f.write('device{}.Holding_Registers_Size = "2"\n\n'.format(x))
            except:
                f.write('device{}.Holding_Registers_Start = "0"\n'.format(x))
                f.write('device{}.Holding_Registers_Size = "0"\n\n'.format(x))














    f.close()