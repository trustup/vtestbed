import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(30)
driver.get("http://localhost:8080/login")
element = driver.find_element_by_id("username")
element.send_keys("openplc")
element = driver.find_element_by_id("password")
element.send_keys("openplc")
element.send_keys(Keys.RETURN)
driver.find_element_by_xpath("//a[contains(@href, 'start_plc')]").click()
