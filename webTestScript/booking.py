#coding=utf-8
#oldUrl="https://web.archive.org/web/20180112090617/https://www.booking.com/"
#newUrl="https://web.archive.org/web/20200108020102/https://www.booking.com/"
#http://web.archive.org/web/20190617191720/https://www.booking.com/
#http://web.archive.org/web/20210615004711/https://www.booking.com/
#http://web.archive.org/web/20220509035925/https://www.booking.com/
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("https://web.archive.org/web/20180112090617/https://www.booking.com/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
# check-in date
el=driver.find_element_by_xpath("//*[@id=\"frm\"]/div[3]/div/div[1]/div[1]/div/div/div[1]/div/div[2]")
el.click()







