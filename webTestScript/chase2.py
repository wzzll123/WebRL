#coding=utf-8
#oldUrl="https://web.archive.org/web/20210101154733/https://www.chase.com/"
#newUrl="https://web.archive.org/web/20220222082957/https://www.chase.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://1.117.174.176/chase2021/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
el=driver.find_element_by_xpath("/html/body/div/div[6]/header/div[4]/div[3]/a")
el.click()
# CV

