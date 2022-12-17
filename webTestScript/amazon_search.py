#coding=utf-8
#oldUrl="http://web.archive.org/web/20180525002632/https://www.amazon.com/"
#newUrl="http://web.archive.org/web/20200721002358/https://www.amazon.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/amazon2018/index.html")
#searh button
el=driver.find_element_by_xpath("/html/body/div[1]/header/div/div[1]/div[3]/div/form/div[2]/div/input")
el.click()