#coding=utf-8
#oldUrl="https://web.archive.org/web/20160104144745/http://www.w3schools.com/"
#newUrl="http://web.archive.org/web/20191031171902/https://www.w3schools.com/"
#http://web.archive.org/web/20171219002530/www.w3schools.com
#http://web.archive.org/web/20201231100001/https://www.w3schools.com/
#http://web.archive.org/web/20220516060313/https://www.w3schools.com/
import time
from selenium import webdriver
driver=webdriver.Chrome("/usr/bin/chromedriver")
driver.get("https://web.archive.org/web/20160104144745/http://www.w3schools.com/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
el=driver.find_element_by_xpath("//*[@id=\"main\"]/div[1]/div[1]/a[1]")
el.click()
# time.sleep(2)
# el=driver.find_element_by_link_text("Next Chapter »")
# el.click()

