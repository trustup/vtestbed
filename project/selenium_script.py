def selenium_script(hmi, hmi_os, plc, plc_code, dst_script_ubuntu, path_temp_script):

    #FOR HMI SCADABR (ubuntu and windows)
    if hmi[0] == 'scadabr':
        login_user = 'admin'
        login_pass = '$admin$'
        with open(r'{}/script_selenium.py'.format(path_temp_script), 'w') as f:
            f.write(
                "import selenium\nfrom selenium import webdriver\nfrom selenium.webdriver.common.keys import Keys\nimport json\n")
            f.write("from selenium.webdriver.firefox.options import Options\n")
            f.write("options = Options()\noptions.headless = True\n")
            if hmi_os[0] != 'windows.7':
                f.write("driver = webdriver.Firefox(options=options)\ndriver.implicitly_wait(30)\n")
            else:
                f.write(
                    "driver = webdriver.Firefox(options=options, executable_path=r'C:\CyberRange\geckodriver.exe')\ndriver.implicitly_wait(30)\n")
            f.write('driver.get("http://localhost:8080/ScadaBR/login.htm")\n')
            f.write('element = driver.find_element_by_id("username")\nelement.send_keys("{}")\n'.format(login_user))
            f.write('element = driver.find_element_by_id("password")\nelement.send_keys("{}")\n'.format(login_pass))
            f.write('element.send_keys(Keys.RETURN)\n')
            a = "'emport.shtm'"
            # b = "'watch_list.shtm'"
            b = "'data_sources.shtm'"
            f.write('driver.find_element_by_xpath("//a[contains(@href, {})]").click()\n'.format(a))
            f.write('data = driver.find_element_by_id("emportData")\n')
            if hmi_os[0] != 'windows.7':
                f.write('with open("/home/ubuntu/data.json") as json_file:\n')
            else:
                f.write("with open(r'C:\CyberRange\data.json') as json_file:\n")
            f.write('    data_to_write = json.loads(json_file.read())\n')
            f.write('data.send_keys("{}".format(json.dumps(data_to_write)))\n')
            f.write('driver.find_element_by_id("importJsonBtn").click()\n')
        f.close()


    ####################################################################################################################
    #FOR OPENPLC (ubuntu)
    if len(plc) != 0:
        for idx, x in enumerate(plc):
            login_user = 'openplc'
            login_pass = 'openplc'
            with open(r'{}/script_selenium_plc{}.py'.format(path_temp_script,idx + 1), 'w') as f:
                f.write(
                    "import selenium\nfrom selenium import webdriver\nfrom selenium.webdriver.common.keys import Keys\nimport json\nimport time\n")
                f.write("from selenium.webdriver.firefox.options import Options\n")
                f.write("options = Options()\noptions.headless = True\n")
                f.write("driver = webdriver.Firefox(options=options)\ndriver.implicitly_wait(30)\n")
                f.write('driver.get("http://localhost:8080/login")\n')
                f.write('element = driver.find_element_by_id("username")\nelement.send_keys("{}")\n'.format(login_user))
                f.write('element = driver.find_element_by_id("password")\nelement.send_keys("{}")\n'.format(login_pass))
                f.write('element.send_keys(Keys.RETURN)\n')
                a = "'programs'"
                f.write('driver.find_element_by_xpath("//a[contains(@href, {})]").click()\n'.format(a))
                f.write('element = driver.find_element_by_id("file")\n')
                f.write('element.send_keys("{}{}")\n'.format(dst_script_ubuntu, plc_code[idx]))
                f.write('element = driver.find_element_by_name("submit").click()\n')
                f.write('element = driver.find_element_by_id("prog_name")\n')
                f.write('element.send_keys("{}")\n'.format(plc_code[idx]))
                a = "'submit'"
                f.write('element = driver.find_element_by_css_selector("input[type={}]").click()\n'.format(a))
                f.write("finished = False\n")
                f.write("while not finished:\n")
                f.write("    try:\n")
                f.write('        element = driver.find_element_by_id("dashboard_button").click()\n')
                f.write("        finished = True\n")
                f.write("    except:\n")
                f.write("        time.sleep(1)\n")
                a = "'start_plc'"
                f.write('driver.find_element_by_xpath("//a[contains(@href, {})]").click()\n'.format(a))
                #a = "'settings'"
                #f.write('driver.find_element_by_xpath("//a[contains(@href, {})]").click()\n'.format(a))
                #f.write('element = driver.find_element_by_id("auto_run").click()\n')
                #a = "'submit'"
                #f.write('element = driver.find_element_by_css_selector("input[type={}]").click()\n'.format(a))

    if len(plc) != 0:
        for idx, x in enumerate(plc):
            login_user = 'openplc'
            login_pass = 'openplc'
            with open(r'{}/script_selenium_plc{}_restart.py'.format(path_temp_script,idx + 1), 'w') as f:
                f.write(
                    "import selenium\nfrom selenium import webdriver\nfrom selenium.webdriver.common.keys import Keys\nimport json\nimport time\n")
                f.write("from selenium.webdriver.firefox.options import Options\n")
                f.write("options = Options()\noptions.headless = True\n")
                f.write("driver = webdriver.Firefox(options=options)\ndriver.implicitly_wait(30)\n")
                f.write('driver.get("http://localhost:8080/login")\n')
                f.write('element = driver.find_element_by_id("username")\nelement.send_keys("{}")\n'.format(login_user))
                f.write('element = driver.find_element_by_id("password")\nelement.send_keys("{}")\n'.format(login_pass))
                f.write('element.send_keys(Keys.RETURN)\n')
                a = "'start_plc'"
                f.write('driver.find_element_by_xpath("//a[contains(@href, {})]").click()\n'.format(a))