import json
import numpy as np
def json_generator(ip_list, sensors, actuators, model, rtu, tp_alert, variable, path_temp_script):

    sensors2 = sensors
    ln = (len(sensors2) + len(actuators)) * 2
    ar = np.arange(0, ln, 2)
    register_modbus = ar.tolist()
    # register_modbus2 = [0, 2, 4, 6, 8, 10, 12]

    dataSource_id = 'DS_074735'
    if len(rtu) != 0:
        host = ip_list[rtu[0] + '.eth0'][0]
    else:
        host = ip_list[model[0] + '.eth0'][0]

    # manage alert:
    eventDetector = []
    variable_alert = []
    type_alert = []
    # values_alert = []
    if len(tp_alert) != 0:
        tp = tp_alert.upper()
        #type_alert.append(tp)
        type_alert = tp.replace(" ","").split(",")
        variable = variable.replace(" ","").split(";")
        for idx, y in enumerate(type_alert):
            vrr = variable[idx].replace(" ","").split(",")
            for idz, z in enumerate(vrr):
                if y == 'HIGH_LIMIT':
                    vr = z.replace(" ", "").split(">")
                    variable_alert.append(vr[0])
                    eventDetector.append({'xid': 'PED_{}'.format(980000 + idx),
                                          'type': y,
                                          'alarmLevel': 'URGENT',
                                          'limit': float(vr[1]),
                                          "durationType": "SECONDS",
                                          "duration": 2,
                                          "alias": "high_level_{}".format(vr[0])})
                if y == 'LOW_LIMIT':
                    vr = z.replace(" ", "").split("<")
                    variable_alert.append(vr[0])
                    eventDetector.append({'xid': 'PED_{}'.format(980000 + idx),
                                          'type': y,
                                          'alarmLevel': 'URGENT',
                                          'limit': float(vr[1]),
                                          "durationType": "SECONDS",
                                          "duration": 2,
                                          "alias": "low_level_{}".format(vr[0])})
                if y == 'CHANGE':
                    vr = z.replace(" ", "")
                    variable_alert.append(vr)
                    eventDetector.append({'xid': 'PED_{}'.format(980000 + idx),
                                          'type': "POINT_CHANGE",
                                          'alarmLevel': 'URGENT',
                                          "alias": "change_{}".format(vr)})
                if y == 'NO_CHANGE':
                    vr = z.replace(" ", "")
                    variable_alert.append(vr)
                    eventDetector.append({'xid': 'PED_{}'.format(980000 + idx),
                                          'type': "NO_CHANGE",
                                          'alarmLevel': 'URGENT',
                                          "durationType": "SECONDS",
                                          "duration": 2,
                                          "alias": "no_change_{}".format(vr)})


    # ------------------------------------data sources----------------------------------
    data = {}
    data['dataSources'] = []
    data['dataSources'].append({
        'xid': dataSource_id,
        'type': 'MODBUS_IP',
        'alarmLevels': {'POINT_WRITE_EXCEPTION': 'NONE', 'DATA_SOURCE_EXCEPTION': 'NONE',
                        'POINT_READ_EXCEPTION': 'NONE'},
        'updatePeriodType': 'MILLISECONDS',
        'transportType': 'TCP',
        'contiguousBatches': False,
        'createSlaveMonitorPoints': False,
        'enabled': True,
        'encapsulated': False,
        'host': host,
        'maxReadBitCount': 2000,
        'maxReadRegisterCount': 125,
        'maxWriteRegisterCount': 120,
        'name': model[0],
        'port': 502,
        'quantize': False,
        'retries': 2,
        'timeout': 500,
        'updatePeriods': 500
    })
    # -----------------------------data points-------------------------------------

    data['dataPoints'] = []
    for idx, x in enumerate(sensors2):
        event = []
        for idxx, xx in enumerate(variable_alert):
            if x == xx:
                event.append(eventDetector[idxx])
                break
        data['dataPoints'].append({
            'xid': 'DP_{}'.format(967000 + idx),
            'loggingType': 'ON_CHANGE',
            'intervalLoggingPeriodType': 'MINUTES',
            'intervalLoggingType': 'INSTANT',
            'purgeType': 'YEARS',
            'pointLocator': {
                'range': 'HOLDING_REGISTER',
                'modbusDataType': 'FOUR_BYTE_FLOAT',
                'additive': 0.0,
                'bit': 0,
                'charset': 'ASCII',
                'multiplier': 1.0,
                'offset': register_modbus[idx],
                'registerCount': 0,
                'settableOverride': False,
                'slaveId': 1,
                'slaveMonitor': False
            },
            'eventDetectors': event,
            'engineeringUnits': '',
            'chartColour': None,
            'chartRenderer': None,
            'dataSourceXid': dataSource_id,
            'defaultCacheSize': 1,
            'deviceName': model[0],
            'discardExtremeValues': False,
            'discardHighLimit': 1.7976931348623157E308,
            'discardLowLimit': -1.7976931348623157E308,
            'enabled': True,
            'intervalLoggingPeriod': 15,
            'name': x,
            'purgePeriod': 1,
            'textRenderer': {'type': 'PLAIN', 'suffix': ''},
            'tolerance': 0.0
        })
    if len(actuators) != 0:
        for idx, x in enumerate(actuators):
            data['dataPoints'].append({
                'xid': 'DP_{}'.format(967000 + idx + len(sensors2)),
                'loggingType': 'ON_CHANGE',
                'intervalLoggingPeriodType': 'MINUTES',
                'intervalLoggingType': 'INSTANT',
                'purgeType': 'YEARS',
                'pointLocator': {
                    'range': 'HOLDING_REGISTER',
                    'modbusDataType': 'FOUR_BYTE_FLOAT',
                    'additive': 0.0,
                    'bit': 0,
                    'charset': 'ASCII',
                    'multiplier': 1.0,
                    'offset': register_modbus[idx + len(sensors2)],
                    'registerCount': 0,
                    'settableOverride': True,
                    'slaveId': 1,
                    'slaveMonitor': False
                },
                'eventDetectors': [],
                'engineeringUnits': '',
                'chartColour': None,
                'chartRenderer': None,
                'dataSourceXid': dataSource_id,
                'defaultCacheSize': 1,
                'deviceName': model[0],
                'discardExtremeValues': False,
                'discardHighLimit': 1.7976931348623157E308,
                'discardLowLimit': -1.7976931348623157E308,
                'enabled': True,
                'intervalLoggingPeriod': 15,
                'name': x[0],
                'purgePeriod': 1,
                'textRenderer': {'type': 'PLAIN', 'suffix': ''},
                'tolerance': 0.0
            })

    # ----------------------------------graphical views-----------------------------------
    graphical_pages = []
    #graphical_pages = sensors2  ###NOTA: viene aggiornato anche sensors non solo graphical_pages
    for idx,z in enumerate(sensors):
        graphical_pages.append(z)
    if len(actuators) != 0:
        for idx, x in enumerate(actuators):
            graphical_pages.append(x[0])

    viewComponents = []  # for main page
    for idx, y in enumerate(graphical_pages):
        viewComponents.append({
            "type": "HTML",
            "content": "<a href=\"http://localhost:8080/ScadaBR/views.shtm?viewId={}\"><IMG SRC=\"uploads\/btn.png\" BORDER=\"0\"></a></img></A>".format(
                2 + idx),
            "x": 30 + (100 * idx),
            "y": 15
        })
        viewComponents.append({
            "type": "LINK",
            "content": "<a href='http://localhost:8080/ScadaBR/views.shtm?viewId={}'>{}</a>".format(2 + idx, y),
            "link": "http://localhost:8080/ScadaBR/views.shtm?viewId={}".format(2 + idx),
            "text": "{}".format(y),
            "x": 30 + (100 * idx),
            "y": 55
        })

    data['graphicalViews'] = []
    data['graphicalViews'].append({  # MAIN PAGE
        'user': 'admin',
        'anonymousAccess': 'NONE',
        'viewComponents': viewComponents,
        'sharingUsers': [{"user": "user", "accessType": "READ"}],
        'backgroundFilename': "uploads\\/{}.png".format(model[0]),
        'name': "{}".format(model[0]),
        'xid': "GV_360000"
    })
    for idx, y in enumerate(graphical_pages):
        data['graphicalViews'].append({  # SENSORS AND ACTUATORS PAGE
            'user': 'admin',
            'anonymousAccess': 'NONE',
            'viewComponents': [{
                "type": "IMAGE_CHART",
                "children": {"point1": "DP_{}".format(967000+idx)},
                "durationType": "HOURS",
                "durationPeriods": 1,
                "height": 300,
                "name": "{}".format(y),
                "width": 500,
                "x": 100,
                "y": 40
            }, {
                "type": "SIMPLE",
                "dataPointXid": "DP_{}".format(967000+idx),
                "bkgdColorOverride": "",
                "displayControls": False,
                "displayPointName": True,
                "nameOverride": "",
                "settableOverride": False,
                "styleAttribute": "",
                "x": 290,
                "y": 350
            }, {
                "type": "HTML",
                "content": "<a href=\"http://localhost:8080/ScadaBR/views.shtm?viewId=1\"><IMG SRC=\"uploads\\/btn.png\" BORDER=\"0\"></a></img></A>",
                "x": 350,
                "y": 386
            }, {
                "type": "LINK",
                "content": "<a href='http://localhost:8080/ScadaBR/views.shtm?viewId=1'>Go To Model</a>",
                "link": "http://localhost:8080/ScadaBR/views.shtm?viewId=1",
                "text": "Go To Model",
                "x": 341,
                "y": 428
            }
            ],
            'sharingUsers': [{"user": "user", "accessType": "READ"}],
            'backgroundFilename': None,
            'name': y,
            'xid': "GV_36000{}".format(idx + 1)
        })

    # --------------------------watch lists---------------------------------------------
    data['watchLists'] = []
    data['watchLists'].append({
        'xid': 'WL_558981',
        'user': 'admin',
        'name': '(unnamed)'
    })

    # ------------------------------users-----------------------------------------------
    # bisognerebbe fare un for per sensors e uno per actuators, ma nelle righe precedenti l'ho gia fatto per graphical_pages, uso quello
    # nota: sensors anche è cambiato assieme a graphical pages
    dataPointPermissions = []
    for idx, x in enumerate(graphical_pages):
        dataPointPermissions.append({
            "dataPointXid": "DP_{}".format(967000 + idx),
            "permission": "READ"
        })

    data['users'] = []
    data['users'].append({
        "admin": True,
        "disabled": False,
        "email": "admin@yourMangoDomain.com",
        "homeUrl": "",
        "password": "wUt32hShc6WTwurKth9wRWKq9Gs=",
        "phone": "",
        "receiveOwnAuditEvents": False,
        "username": "admin"
    })
    data['users'].append({
        "dataSourcePermissions": [],
        "dataPointPermissions": dataPointPermissions,
        "admin": False,
        "disabled": False,
        "email": "u@u.com",
        "homeUrl": "",
        "password": "8ibT1VOTbHjV4OlGfg622j2yJBg=",
        "phone": "0000000",
        "receiveOwnAuditEvents": False,
        "username": "user"
    })

    with open('{}/data.json'.format(path_temp_script), 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=3)


###-------------------------------------------------------------------------------------------------------------------------------------------
###-------------------------------------------------------------------------------------------------------------------------------------------
###-------------------------------------------------------------------------------------------------------------------------------------------
def json_generator_multiple(ip_list, sensors, actuators, model, rtu,input_rtu,tp_alert, variable, path_temp_script):

    #rtu = ['rtu1', 'rtu2']
    #rtu_input = ['mainTank.V,secondaryTank.V','velocityTank2.V,input1']
    #sensors2 = sensors


    #ln = (len(sensors2) + len(actuators)) * 2
    #ar = np.arange(0, ln, 2)
    #register_modbus = ar.tolist()
    # register_modbus2 = [0, 2, 4, 6, 8, 10, 12]

    dataSource_id = 'DS_074735'
    # if len(rtu) != 0:
    #     host = ip_list[rtu[0] + '.eth0'][0]
    # else:
    #     host = ip_list[model[0] + '.eth0'][0]

    # manage alert:
    eventDetector = []
    variable_alert = []
    type_alert = []
    # values_alert = []
    if len(tp_alert) != 0:
        tp = tp_alert.upper()
        # type_alert.append(tp)
        type_alert = tp.replace(" ", "").split(",")
        variable = variable.replace(" ", "").split(";")
        for idx, y in enumerate(type_alert):
            vrr = variable[idx].replace(" ", "").split(",")
            for idz, z in enumerate(vrr):
                if y == 'HIGH_LIMIT':
                    vr = z.replace(" ", "").split(">")
                    variable_alert.append(vr[0])
                    eventDetector.append({'xid': 'PED_{}'.format(980000 + idx),
                                          'type': y,
                                          'alarmLevel': 'URGENT',
                                          'limit': float(vr[1]),
                                          "durationType": "SECONDS",
                                          "duration": 2,
                                          "alias": "high_level_{}".format(vr[0])})
                if y == 'LOW_LIMIT':
                    vr = z.replace(" ", "").split("<")
                    variable_alert.append(vr[0])
                    eventDetector.append({'xid': 'PED_{}'.format(980000 + idx),
                                          'type': y,
                                          'alarmLevel': 'URGENT',
                                          'limit': float(vr[1]),
                                          "durationType": "SECONDS",
                                          "duration": 2,
                                          "alias": "low_level_{}".format(vr[0])})
                if y == 'CHANGE':
                    vr = z.replace(" ", "")
                    variable_alert.append(vr)
                    eventDetector.append({'xid': 'PED_{}'.format(980000 + idx),
                                          'type': "POINT_CHANGE",
                                          'alarmLevel': 'URGENT',
                                          "alias": "change_{}".format(vr)})
                if y == 'NO_CHANGE':
                    vr = z.replace(" ", "")
                    variable_alert.append(vr)
                    eventDetector.append({'xid': 'PED_{}'.format(980000 + idx),
                                          'type': "NO_CHANGE",
                                          'alarmLevel': 'URGENT',
                                          "durationType": "SECONDS",
                                          "duration": 2,
                                          "alias": "no_change_{}".format(vr)})

    # ------------------------------------data sources----------------------------------

    data = {}
    data['dataSources'] = []
    for idx, x in enumerate(rtu):
        host = ip_list['{}'.format(x + '.eth0')][0]
        data['dataSources'].append({
            'xid': 'DS_{}'.format(974000 + idx),
            'type': 'MODBUS_IP',
            'alarmLevels': {'POINT_WRITE_EXCEPTION': 'NONE', 'DATA_SOURCE_EXCEPTION': 'NONE',
                            'POINT_READ_EXCEPTION': 'NONE'},
            'updatePeriodType': 'MILLISECONDS',
            'transportType': 'TCP',
            'contiguousBatches': False,
            'createSlaveMonitorPoints': False,
            'enabled': True,
            'encapsulated': False,
            'host': host,
            'maxReadBitCount': 2000,
            'maxReadRegisterCount': 125,
            'maxWriteRegisterCount': 120,
            'name': x,
            'port': 502,
            'quantize': False,
            'retries': 2,
            'timeout': 500,
            'updatePeriods': 500
        })

    # -----------------------------data points-------------------------------------

    data['dataPoints'] = []
    lstart = 0
    for idz, z in enumerate(rtu):
        a = input_rtu[idz].split(",")
        rtu_s = []
        rtu_a = []
        for idy, y in enumerate(a):
            if y in sensors:
                rtu_s.append(y)
            elif y in actuators:
                rtu_a.append(y)

        for idx, x in enumerate(rtu_s):
            event = []
            for idxx, xx in enumerate(variable_alert):
                if x == xx:
                    event.append(eventDetector[idxx])
                    break
            data['dataPoints'].append({
                'xid': 'DP_{}'.format(967000 + idx + lstart),
                'loggingType': 'ON_CHANGE',
                'intervalLoggingPeriodType': 'MINUTES',
                'intervalLoggingType': 'INSTANT',
                'purgeType': 'YEARS',
                'pointLocator': {
                    'range': 'HOLDING_REGISTER',
                    'modbusDataType': 'FOUR_BYTE_FLOAT',
                    'additive': 0.0,
                    'bit': 0,
                    'charset': 'ASCII',
                    'multiplier': 1.0,
                    'offset': idx * 2,
                    'registerCount': 0,
                    'settableOverride': False,
                    'slaveId': 1,
                    'slaveMonitor': False
                },
                'eventDetectors': event,
                'engineeringUnits': '',
                'chartColour': None,
                'chartRenderer': None,
                'dataSourceXid': 'DS_{}'.format(974000 + idz),
                'defaultCacheSize': 1,
                'deviceName': z,
                'discardExtremeValues': False,
                'discardHighLimit': 1.7976931348623157E308,
                'discardLowLimit': -1.7976931348623157E308,
                'enabled': True,
                'intervalLoggingPeriod': 15,
                'name': x,
                'purgePeriod': 1,
                'textRenderer': {'type': 'PLAIN', 'suffix': ''},
                'tolerance': 0.0
            })
        if len(rtu_a) != 0:
            for idx, x in enumerate(rtu_a):
                data['dataPoints'].append({
                    'xid': 'DP_{}'.format(967000 + idx + len(rtu_s) + lstart),
                    'loggingType': 'ON_CHANGE',
                    'intervalLoggingPeriodType': 'MINUTES',
                    'intervalLoggingType': 'INSTANT',
                    'purgeType': 'YEARS',
                    'pointLocator': {
                        'range': 'HOLDING_REGISTER',
                        'modbusDataType': 'FOUR_BYTE_FLOAT',
                        'additive': 0.0,
                        'bit': 0,
                        'charset': 'ASCII',
                        'multiplier': 1.0,
                        'offset': len(rtu_s)*2+(idx*2),
                        'registerCount': 0,
                        'settableOverride': True,
                        'slaveId': 1,
                        'slaveMonitor': False
                    },
                    'eventDetectors': [],
                    'engineeringUnits': '',
                    'chartColour': None,
                    'chartRenderer': None,
                    'dataSourceXid': 'DS_{}'.format(974000 + idz),
                    'defaultCacheSize': 1,
                    'deviceName': z,
                    'discardExtremeValues': False,
                    'discardHighLimit': 1.7976931348623157E308,
                    'discardLowLimit': -1.7976931348623157E308,
                    'enabled': True,
                    'intervalLoggingPeriod': 15,
                    'name': x,
                    'purgePeriod': 1,
                    'textRenderer': {'type': 'PLAIN', 'suffix': ''},
                    'tolerance': 0.0
                })
        lstart = len(rtu_s)+len(rtu_a)

    #----------------------------------graphical pages---------------------------------------------------------

    graphical_pages = []
    for x in range(len(input_rtu)) :
        tmp = input_rtu[x].split(",")
        for y in tmp:
            graphical_pages.append(y)

    # for idx, z in enumerate(sensors):
    #     graphical_pages.append(z)
    # if len(actuators) != 0:
    #     for idx, x in enumerate(actuators):
    #         graphical_pages.append(x[0])

    viewComponents = []  # for main page
    for idx, y in enumerate(graphical_pages):
        viewComponents.append({
            "type": "HTML",
            "content": "<a href=\"http://localhost:8080/ScadaBR/views.shtm?viewId={}\"><IMG SRC=\"uploads\/btn.png\" BORDER=\"0\"></a></img></A>".format(
                2 + idx),
            "x": 30 + (100 * idx),
            "y": 15
        })
        viewComponents.append({
            "type": "LINK",
            "content": "<a href='http://localhost:8080/ScadaBR/views.shtm?viewId={}'>{}</a>".format(2 + idx, y),
            "link": "http://localhost:8080/ScadaBR/views.shtm?viewId={}".format(2 + idx),
            "text": "{}".format(y),
            "x": 30 + (100 * idx),
            "y": 55
        })

    data['graphicalViews'] = []
    data['graphicalViews'].append({  # MAIN PAGE
        'user': 'admin',
        'anonymousAccess': 'NONE',
        'viewComponents': viewComponents,
        'sharingUsers': [{"user": "user", "accessType": "READ"}],
        'backgroundFilename': "uploads\\/{}.png".format(model[0]),
        'name': "{}".format(model[0]),
        'xid': "GV_360000"
    })
    for idx, y in enumerate(graphical_pages):
        data['graphicalViews'].append({  # SENSORS AND ACTUATORS PAGE
            'user': 'admin',
            'anonymousAccess': 'NONE',
            'viewComponents': [{
                "type": "IMAGE_CHART",
                "children": {"point1": "DP_{}".format(967000+idx)},
                "durationType": "HOURS",
                "durationPeriods": 1,
                "height": 300,
                "name": "{}".format(y),
                "width": 500,
                "x": 100,
                "y": 40
            }, {
                "type": "SIMPLE",
                "dataPointXid": "DP_{}".format(967000+idx),
                "bkgdColorOverride": "",
                "displayControls": False,
                "displayPointName": True,
                "nameOverride": "",
                "settableOverride": False,
                "styleAttribute": "",
                "x": 290,
                "y": 350
            }, {
                "type": "HTML",
                "content": "<a href=\"http://localhost:8080/ScadaBR/views.shtm?viewId=1\"><IMG SRC=\"uploads\\/btn.png\" BORDER=\"0\"></a></img></A>",
                "x": 350,
                "y": 386
            }, {
                "type": "LINK",
                "content": "<a href='http://localhost:8080/ScadaBR/views.shtm?viewId=1'>Go To Model</a>",
                "link": "http://localhost:8080/ScadaBR/views.shtm?viewId=1",
                "text": "Go To Model",
                "x": 341,
                "y": 428
            }
            ],
            'sharingUsers': [{"user": "user", "accessType": "READ"}],
            'backgroundFilename': None,
            'name': y,
            'xid': "GV_36000{}".format(idx + 1)
        })

    # --------------------------watch lists---------------------------------------------
    data['watchLists'] = []
    data['watchLists'].append({
        'xid': 'WL_558981',
        'user': 'admin',
        'name': '(unnamed)'
    })

    # ------------------------------users-----------------------------------------------
    dataPointPermissions = []
    for idx, x in enumerate(graphical_pages):
        dataPointPermissions.append({
            "dataPointXid": "DP_{}".format(967000 + idx),
            "permission": "READ"
        })

    data['users'] = []
    data['users'].append({
        "admin": True,
        "disabled": False,
        "email": "admin@yourMangoDomain.com",
        "homeUrl": "",
        "password": "wUt32hShc6WTwurKth9wRWKq9Gs=",
        "phone": "",
        "receiveOwnAuditEvents": False,
        "username": "admin"
    })
    data['users'].append({
        "dataSourcePermissions": [],
        "dataPointPermissions": dataPointPermissions,
        "admin": False,
        "disabled": False,
        "email": "u@u.com",
        "homeUrl": "",
        "password": "8ibT1VOTbHjV4OlGfg622j2yJBg=",
        "phone": "0000000",
        "receiveOwnAuditEvents": False,
        "username": "user"
    })

    with open('{}/data.json'.format(path_temp_script), 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=3)