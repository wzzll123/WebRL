#coding=utf-8
#oldUrl="https://web.archive.org/web/20190115022528/https://www.allrecipes.com/"
#newUrl="https://web.archive.org/web/20220215010622/https://www.allrecipes.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("https://web.archive.org/web/20190115022528/https://www.allrecipes.com/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
el=driver.find_element_by_xpath("//*[@id=\"searchText\"]")
#search
el.send_keys("ab")


