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
driver.find_element_by_xpath("//a[contains(@href, 'programs')]").click()
element = driver.find_element_by_id("file")
element.send_keys("/home/ubuntu/robot_control.st")
element = driver.find_element_by_name("submit").click()
element = driver.find_element_by_id("prog_name")
element.send_keys("robot_control.st")
element = driver.find_element_by_css_selector("input[type='submit']").click()
finished = False
while not finished:
    try:
        element = driver.find_element_by_id("dashboard_button").click()
        finished = True
    except:
        time.sleep(1)
driver.find_element_by_xpath("//a[contains(@href, 'start_plc')]").click()
