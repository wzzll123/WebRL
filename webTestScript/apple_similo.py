import time
from selenium import webdriver
driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
driver.get("file:///Users/wzz/Desktop/Research/scriptRepair/WebRL/website/apple/old/web.archive.org/web/20171002003641/https:/www.apple.com/index.html")
el = driver.find_element_by_link_text("Support")
el = driver.find_element_by_link_text("iPad")
el = driver.find_element_by_link_text("TV")
el = driver.find_element_by_xpath("/html[1]/body[1]/nav[1]/div[1]/ul[2]/li[9]")
el = driver.find_element_by_id("ac-gn-firstfocus")
el = driver.find_element_by_link_text("iPhone")
el = driver.find_element_by_link_text("Music")
el = driver.find_element_by_link_text("Mac")
el = driver.find_element_by_link_text("Watch")
el = driver.find_element_by_link_text("Shopping Bag")
