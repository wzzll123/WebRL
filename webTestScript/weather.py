#coding=utf-8
#oldUrl="http://web.archive.org/web/20200101032203/https://weather.com/"
#newUrl="http://web.archive.org/web/20220223004133/https://weather.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20200101032203/https://weather.com/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
# today
el=driver.find_element_by_xpath("//*[@id=\"header-LocalsuiteNav-1577cc50-d1e0-42a2-9596-51ddc72ccdd8\"]/div/div/div/ul/li[1]/a")
el.click()

