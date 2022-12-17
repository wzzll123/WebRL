#oldUrl="https://web.archive.org/web/20180608001442/https://www.walmart.com/"
#newUrl="https://web.archive.org/web/20200909013626/https://www.walmart.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/walmart2018/index.html")
#searh button
el=driver.find_element_by_xpath("//*[@id=\"global-search-form\"]/div/div[3]/div/button")
el.click()