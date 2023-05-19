import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "toor",
    database = "testbed"
)

cursor = mydb.cursor()

def get_models():
    cursor.execute("SELECT name FROM models")

    result = cursor.fetchall()
    res = []

    for idx,x in enumerate(result):
        res.append(x[0])

    return res

def get_models2(modeler):
    sql = 'SELECT models.name FROM models JOIN modeler ON modeler.ID = models.modeler_ID WHERE modeler.name = %s'
    addr = ("{}".format(modeler),)

    cursor.execute(sql,addr)
    result = cursor.fetchall()
    res = []
    for idx, x in enumerate(result):
        res.append(x[0])
    return res


#def get_sensors2(model):
#    cursor.execute("SELECT sensors.name FROM sensors JOIN models ON models.ID = model_id WHERE models.name = '{}'".format(model))
#    result = cursor.fetchall()
#    res = []
#    for idx, x in enumerate(result):
#        res.append(x[0])
#    return res

def get_sensors(model):
    sql = 'SELECT sensors.name FROM sensors JOIN models ON models.ID = model_id WHERE models.name = %s'
    addr = ("{}".format(model),)

    cursor.execute(sql,addr)
    result = cursor.fetchall()
    res = []
    for idx, x in enumerate(result):
        res.append(x[0])
    return res


def get_actuators(model):
    sql = 'SELECT actuators.name, actuators.value FROM actuators JOIN models ON models.ID = model_id WHERE models.name = %s'
    addr = ("{}".format(model),)


    cursor.execute(sql, addr)
    result = cursor.fetchall()

    return result

# def get_os(vm):
#      sql = 'SELECT vms_os.name FROM vms_os JOIN vms ON vms.ID = vms_os.vms_ID WHERE vms.name = %s'
#      addr = ("{}".format(vm),)
#
#      cursor.execute(sql,addr)
#      result = cursor.fetchall()
#      res = []
#      for idx, x in enumerate(result):
#          res.append(x[0])
#      return res

def get_os(vm):
    sql = 'SELECT os.name FROM os JOIN os_vms ON os.ID = os_vms.os_ID JOIN vms ON os_vms.vm_ID = vms.ID WHERE vms.name = %s'
    addr = ("{}".format(vm),)

    cursor.execute(sql, addr)
    result = cursor.fetchall()
    res = []
    for idx, x in enumerate(result):
        res.append(x[0])
    return res


def get_modeler():
    sql = 'SELECT name FROM modeler'
    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    for idx, x in enumerate(result):
        res.append(x[0])
    return res

def get_interfaces():
    sql = 'SELECT name FROM interfaces'
    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    for idx, x in enumerate(result):
        res.append(x[0])
    return res

def get_hmi():
    sql = 'SELECT name FROM hmi'
    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    for idx, x in enumerate(result):
        res.append(x[0])
    return res


def get_fix(vm,os):
    sql = 'select fix.name from fix join fix_vms_os on fix.ID = fix_vms_os.fix_ID join os on os.ID = fix_vms_os.vms_os_ID join vms on vms.ID = fix_vms_os.vms_ID where vms.name = %s and os.name = %s'
    addr = ("{}".format(vm),"{}".format(os))

    cursor.execute(sql, addr)
    result = cursor.fetchall()
    res = []
    for idx, x in enumerate(result):
        res.append(x[0])
    return res

def get_alert(hmi):
    sql = "SELECT hmi_alert.name, hmi_alert.input FROM hmi_alert JOIN hmi ON hmi.ID = hmi_alert.hmi_ID where hmi.name = %s"
    addr = ("{}".format(hmi),)

    result = []
    try:
        cursor.execute(sql, addr)
        result = cursor.fetchall()
        return result
    except:
        return result
    #res = []

    #for idx, x in enumerate(result):
    #    res.append(x[0])


def get_log_type(vm,os):
    sql = 'SELECT log_type.name FROM log_type JOIN log_vms_os ON log_type.ID = log_vms_os.log_ID JOIN os ON os.ID = log_vms_os.os_ID JOIN vms ON vms.ID = log_vms_os.vms_ID WHERE vms.name = %s AND os.name = %s'
    addr = ("{}".format(vm),"{}".format(os))

    cursor.execute(sql, addr)
    result = cursor.fetchall()
    res = []
    for idx, x in enumerate(result):
        res.append(x[0])
    return res


def get_os_modeler(vm):
    sql = 'SELECT os.name FROM os JOIN modeler_os ON os.ID = modeler_os.os_ID JOIN modeler ON modeler_os.modeler_ID = modeler.ID WHERE modeler.name = %s'
    addr = ("{}".format(vm),)

    cursor.execute(sql, addr)
    result = cursor.fetchall()
    res = []
    for idx, x in enumerate(result):
        res.append(x[0])
    return res


def save_scenario_layout(cyber_range_number):
    sql = 'INSERT INTO scenarios (cr_number) VALUES (%s)'
    addr = ("{}".format(cyber_range_number),)
    cursor.execute(sql, addr)
    mydb.commit()

def delete_scenario_layout(cyber_range_number):
    sql = 'DELETE FROM scenarios WHERE cr_number=%s'
    addr = ("{}".format(cyber_range_number),)
    cursor.execute(sql, addr)
    mydb.commit()


def get_scenario_saved():
    sql = 'SELECT cr_number FROM scenarios'
    cursor.execute(sql)
    result = cursor.fetchall()
    res = []
    for idx, x in enumerate(result):
        res.append(x[0])
    return res

get_scenario_saved()