import time
from selenium import webdriver
driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
driver.get("file:///Users/wzz/Desktop/Research/scriptRepair/WebRL/website/linkedin/old/index.html")
el = driver.find_element_by_link_text("Forgot password?")
el = driver.find_element_by_id("login-email")
el = driver.find_element_by_id("login-submit")
el = driver.find_element_by_id("login-password")
el = driver.find_element_by_xpath("/html[1]/body[1]/div[1]/main[1]/div[1]/div[1]/div[1]/h1[1]/img[1]")
