#coding=utf-8
#oldUrl="http://web.archive.org/web/20180525002632/https://www.amazon.com/"
#newUrl="http://web.archive.org/web/20200721002358/https://www.amazon.com/"
#http://web.archive.org/web/20190526084424/https://www.amazon.com/
#http://web.archive.org/web/20220518233749/https://www.amazon.com/
#http://web.archive.org/web/20210705180013/http://www.amazon.com/
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/amazon2018/index.html")
#cart
el=driver.find_element_by_xpath("/html/body/div[1]/header/div/div[2]/div[2]/div/a[5]")
el.click()