#coding=utf-8
#oldUrl="http://web.archive.org/web/20200228000228/https://www.microsoft.com/en-us/"
#newUrl="http://web.archive.org/web/20220323004239/https://www.microsoft.com/en-us/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
# driver.get("http://web.archive.org/web/20200228000228/https://www.microsoft.com/en-us/")
driver.get("file:///Users//Desktop/webProject/microsoft2020/index.html")
# shop windows 10
el=driver.find_element_by_xpath("/html/body/div[1]/div/div/header/div/div/div[2]/form/button")
el.click()
driver.quit()

