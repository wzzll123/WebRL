#coding=utf-8
#oldUrl="http://web.archive.org/web/20180510001701/https://www.youtube.com/"
#newUrl="http://web.archive.org/web/20200609000027/https://www.youtube.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20180510001701/https://www.youtube.com/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
# click search
el=driver.find_element_by_id("search-btn")
el.click()
driver.quit()





