#coding=utf-8
#oldUrl="https://web.archive.org/web/20210122023743/https://www.paypal.com/us/home"
#newUrl="https://web.archive.org/web/20220129060505/https://www.paypal.com/us/home"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/paypal2021/index.html")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
el=driver.find_element_by_xpath("//*[@id=\"main-menu\"]/ul[1]/li[2]/a")
#business
el.click()