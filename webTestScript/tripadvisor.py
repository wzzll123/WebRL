#coding=utf-8
#oldUrl="https://web.archive.org/web/20210109061650/https://www.tripadvisor.com/"
#newUrl="https://web.archive.org/web/20220106012021/https://www.tripadvisor.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("https://web.archive.org/web/20210109061650/https://www.tripadvisor.com/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
# review
el=driver.find_element_by_xpath("//*[@id=\"lithium-root\"]/main/div[1]/div[1]/div/div/div[5]/a")
el.click()


