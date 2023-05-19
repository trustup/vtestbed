import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(30)
driver.get("http://localhost:8080/ScadaBR/login.htm")
element = driver.find_element_by_id("username")
element.send_keys("admin")
element = driver.find_element_by_id("password")
element.send_keys("$admin$")
element.send_keys(Keys.RETURN)
driver.find_element_by_xpath("//a[contains(@href, 'emport.shtm')]").click()
data = driver.find_element_by_id("emportData")
with open("/home/ubuntu/data.json") as json_file:
    data_to_write = json.loads(json_file.read())
data.send_keys("{}".format(json.dumps(data_to_write)))
driver.find_element_by_id("importJsonBtn").click()
