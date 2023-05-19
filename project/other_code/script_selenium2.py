import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

driver = webdriver.Firefox()
driver.implicitly_wait(30)
#driver.maximize_window()

driver.get("http://localhost:8080/ScadaBR/login.htm")
element = driver.find_element_by_id("username")
element.send_keys("admin")
element = driver.find_element_by_id("password")
element.send_keys("admin")
element.send_keys(Keys.RETURN)

driver.find_element_by_xpath("//a[contains(@href,'emport.shtm')]").click()
data = driver.find_element_by_id("emportData")
# data.send_keys("admin")
# driver.find_element_by_id("importJsonBtn").click()

with open("/home/ubuntu/data.json") as json_file:
    data_to_write = json.loads(json_file.read())

data.send_keys("{}".format(json.dumps(data_to_write)))
driver.find_element_by_id("importJsonBtn").click()

driver.find_element_by_xpath("//a[contains(@href,'watch_list.shtm')]").click()