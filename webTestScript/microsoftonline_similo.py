import time
from selenium import webdriver
driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
driver.get("file:///Users/wzz/Desktop/Research/scriptRepair/WebRL/website/microsoftonline/old/index.html")
el = driver.find_element_by_id("cantAccessAccount")
el = driver.find_element_by_id("ftrPrivacy")
el = driver.find_element_by_id("i0116")
el = driver.find_element_by_id("idSIButton9")
el = driver.find_element_by_id("signup")
el = driver.find_element_by_id("ftrTerms")
