#coding=utf-8
#oldUrl="http://web.archive.org/web/20200726022959/https://www.fandom.com/"
#newUrl="http://web.archive.org/web/20220227022323/https://www.fandom.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/fandom2020/index.html")
# file:///Users//Desktop/webProject/msn2021/index.html

el=driver.find_element_by_xpath("/html/body/div[2]/div/div/form/div/label/svg")
el.click()
driver.quit()

