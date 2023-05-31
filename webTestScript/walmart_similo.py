import time
from selenium import webdriver
driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
driver.get("file:///Users/wzz/Desktop/Research/scriptRepair/WebRL/website/walmart/old/index.html")
el = driver.find_element_by_id("global-search-input")
el = driver.find_element_by_id("header-Cart")
el = driver.find_element_by_id("header-Logo")
el = driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/header[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/form[1]/div[1]/div[3]/button[1]")
el = driver.find_element_by_id("header-GlobalEyebrowNav-link-5")
el = driver.find_element_by_id("listboxActive")
el = driver.find_element_by_id("header-GlobalAccountFlyout-flyout-link")
