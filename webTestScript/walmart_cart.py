#coding=utf-8
#oldUrl="https://web.archive.org/web/20180608001442/https://www.walmart.com/"
#newUrl="https://web.archive.org/web/20200909013626/https://www.walmart.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/walmart2018/index.html")
#cart
el=driver.find_element_by_xpath("/html/body/div[3]/div/div/div/header/div/div[3]/div/div/div[3]/div/a/div/span[1]")
el.click()