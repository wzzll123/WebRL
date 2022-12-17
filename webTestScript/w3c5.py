#coding=utf-8
#oldUrl="https://web.archive.org/web/20160104144745/http://www.w3schools.com/"
#newUrl="http://web.archive.org/web/20191031171902/https://www.w3schools.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/w3schools2016/index.html")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
# click learn bootstrap
el=driver.find_element_by_xpath("/html/body/div[4]/div[5]/div[3]/a")
el.click()




