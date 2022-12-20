import time
from selenium import webdriver
driver = webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20220221000940/https://www.yahoo.com/")
el = driver.find_element_by_id("ybar-sbq")
el.send_keys("weather")

el = driver.find_element_by_id("ybar-search")
el.click()

driver.quit()
