import time
from selenium import webdriver
driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
driver.get("file:///Users/wzz/Desktop/Research/scriptRepair/WebRL/website/cnn/old/index.html")
el = driver.find_element_by_id("search-button")
el = driver.find_element_by_id("menu")
