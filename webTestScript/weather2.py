#coding=utf-8
#oldUrl="http://web.archive.org/web/20200101032203/https://weather.com/"
#newUrl="http://web.archive.org/web/20220223004133/https://weather.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20200101032203/https://weather.com/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
# menu
el=driver.find_element_by_xpath("//*[@id=\"header-TwcHeader-10c7c60c-aebb-4e78-b655-512b2460d9f4\"]/div/div/div/div[3]/div[2]/button")
el.click()



