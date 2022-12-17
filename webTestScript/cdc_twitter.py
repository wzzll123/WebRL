#coding=utf-8
#oldUrl="http://web.archive.org/web/20180717163511/https://www.cdc.gov/"
#newUrl="http://web.archive.org/web/20220209003800/https://www.cdc.gov/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20180101034926/https://www.cdc.gov/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
#more topic
el=driver.find_element_by_xpath("//*[@id=\"footer\"]/div[1]/div/nav[1]/ul/li[3]/a/span[1]")
el.click()

