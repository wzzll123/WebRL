import time
from selenium import webdriver
driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
driver.get("file:///Users/wzz/Desktop/Research/scriptRepair/WebRL/website/twitch/old/index.html")
el = driver.find_element_by_id("header_signup")
el = driver.find_element_by_id("query")
el = driver.find_element_by_id("header_browse")
el = driver.find_element_by_id("header_login")
el = driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[1]/a[1]/*[local-name() = 'svg'][1]")
