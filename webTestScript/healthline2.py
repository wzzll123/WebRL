#coding=utf-8
#oldUrl="http://web.archive.org/web/20210101075534/https://www.healthline.com/"
#newUrl="http://web.archive.org/web/20220222105353/https://www.healthline.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20210101075534/https://www.healthline.com/")
# driver.get("http://web.archive.org/web/20210809005904/https://www.linkedin.com/")
#search
el=driver.find_element_by_xpath("//*[@id=\"site-header\"]/div[2]/form/button")
el.click()
driver.quit()

