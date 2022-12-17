#coding=utf-8
#oldUrl="http://web.archive.org/web/20190220004822/http://www.ebay.com/"
#newUrl="http://web.archive.org/web/20220224023129/https://www.ebay.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/ebay2019/index.html")
#search input
el=driver.find_element_by_xpath("/html/body/header/table/tbody/tr/td[3]/form/table/tbody/tr/td[1]/div[1]/div/input")
el.send_keys("a")