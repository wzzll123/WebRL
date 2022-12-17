#coding=utf-8
#oldUrl="https://web.archive.org/web/20190603014315/http://www.twitch.tv/"
#newUrl="https://web.archive.org/web/20200222004844/https://www.twitch.tv/"
#http://web.archive.org/web/20210125014536/https://www.twitch.tv/
#http://web.archive.org/web/20211231000225/https://www.twitch.tv/
#http://web.archive.org/web/20220516083337/https://www.twitch.tv/
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/twitch2019/index.html")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
#home
el=driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/nav/div/div[1]/a[1]/div")
el.click()



























