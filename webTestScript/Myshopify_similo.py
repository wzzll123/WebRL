import time
from selenium import webdriver
driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
driver.get("file:///Users/wzz/Desktop/Research/scriptRepair/WebRL/website/Myshopify/old/index.html")
el = driver.find_element_by_link_text("Home")
el = driver.find_element_by_id("MainNavSignupButton")
