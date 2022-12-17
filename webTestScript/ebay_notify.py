#coding=utf-8
#oldUrl="http://web.archive.org/web/20190220004822/http://www.ebay.com/"
#newUrl="http://web.archive.org/web/20220224023129/https://www.ebay.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/ebay2019/index.html")
# driver.get("http://web.archive.org/web/20200522054136/https://www.office.com/")
#notification
el=driver.find_element_by_xpath("/html/body/header/div[1]/ul[2]/li[3]/div/button")
driver.quit()







