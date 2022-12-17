#coding=utf-8
#oldUrl="http://web.archive.org/web/20200221010206/https://www.msn.com/"
#newUrl="http://web.archive.org/web/20211007005032/https://www.msn.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/msn2020/index.html")
# file:///Users//Desktop/webProject/msn2021/index.html
# search
el=driver.find_element_by_id("sb_form_go")
el.click()
driver.quit()

