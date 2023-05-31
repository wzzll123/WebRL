import time
from selenium import webdriver
driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
driver.get("file:///Users/wzz/Desktop/Research/scriptRepair/WebRL/website/adobe/old/index.html")
el = driver.find_element_by_link_text("Individuals")
el = driver.find_element_by_link_text("Business")
