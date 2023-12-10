import time
from selenium import webdriver
driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
driver.get("file:///Users/wzz/Desktop/webProject/yahoo2022/Yahoo.html")
el = driver.find_element_by_id("ybar-sbq")
el.send_keys("weather")

el = driver.find_element_by_id("ybar-search")
el.click()

driver.quit()
