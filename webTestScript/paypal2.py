#coding=utf-8
#oldUrl="https://web.archive.org/web/20210122023743/https://www.paypal.com/us/home"
#newUrl="https://web.archive.org/web/20220129060505/https://www.paypal.com/us/home"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("https://web.archive.org/web/20210122023743/https://www.paypal.com/us/home")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
el=driver.find_element_by_xpath("//*[@id=\"editorial-send-money\"]/div/div/div[2]/p/a")
#send money now
el.click()