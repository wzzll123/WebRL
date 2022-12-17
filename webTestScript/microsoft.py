#coding=utf-8
#oldUrl="http://web.archive.org/web/20200228000228/https://www.microsoft.com/en-us/"
#newUrl="http://web.archive.org/web/20220323004239/https://www.microsoft.com/en-us/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20200228000228/https://www.microsoft.com/en-us/")
# driver.get("http://web.archive.org/web/20220323004239/https://www.microsoft.com/en-us/")
# pause ppt
el=driver.find_element_by_xpath("//*[@id=\"coreui-hero-wbs8bbs\"]/div/div/div[1]/button")
el.click()
driver.quit()