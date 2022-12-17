#coding=utf-8
#oldUrl="http://web.archive.org/web/20200101032203/https://weather.com/"
#newUrl="http://web.archive.org/web/20220223004133/https://weather.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20200101032203/https://weather.com/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
# hourly
el=driver.find_element_by_link_text("Hourly")
el.click()
