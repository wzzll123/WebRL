import time
from selenium import webdriver
driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
driver.get("file:///Users/wzz/Desktop/Research/scriptRepair/WebRL/website/zillow/old/index.html")
el = driver.find_element_by_link_text("Sell")
el = driver.find_element_by_id("login_opener")
el = driver.find_element_by_xpath("/html[1]/body[1]/div[1]/header[1]/nav[1]/div[1]/div[1]/section[1]/div[1]/a[1]")
el = driver.find_element_by_link_text("Buy")
el = driver.find_element_by_link_text("Agent finder")
el = driver.find_element_by_link_text("Rent")
el = driver.find_element_by_link_text("Advertise")
