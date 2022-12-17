#coding=utf-8
#oldUrl="https://web.archive.org/web/20180112090617/https://www.booking.com/"
#newUrl="https://web.archive.org/web/20200108020102/https://www.booking.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("https://web.archive.org/web/20180112090617/https://www.booking.com/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
# city
el=driver.find_element_by_xpath("//*[@id=\"b2indexPage\"]/div[4]/div[3]/ul[1]/li[2]")
el.click()










