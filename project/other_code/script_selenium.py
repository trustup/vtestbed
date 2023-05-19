import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.maximize_window()

driver.get("https://github.com/")
element = driver.find_element_by_id("user[login]")
element.send_keys("prova")
element.send_keys(Keys.RETURN)
element.close()