#coding=utf-8
#oldUrl="http://web.archive.org/web/20200726022959/https://www.fandom.com/"
#newUrl="http://web.archive.org/web/20220227022323/https://www.fandom.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20200726022959/https://www.fandom.com/")
# file:///Users//Desktop/webProject/msn2021/index.html
# movies
el=driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/a[2]")
el.click()
driver.quit()


