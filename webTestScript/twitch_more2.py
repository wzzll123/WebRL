#coding=utf-8
#oldUrl="https://web.archive.org/web/20190603014315/http://www.twitch.tv/"
#newUrl="https://web.archive.org/web/20200222004844/https://www.twitch.tv/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/twitch2019/index.html")
#more2
el=driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/nav/div/div[1]/div/div/div[1]/div/button/div")
el.click()