#coding=utf-8
#oldUrl="https://web.archive.org/web/20190603014315/http://www.twitch.tv/"
#newUrl="https://web.archive.org/web/20200222004844/https://www.twitch.tv/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/twitch2019/index.html")
#sign in
el=driver.find_element_by_xpath("//*[@id=\"root\"]/div/div[2]/nav/div/div[3]/div[3]/div/div[1]/div[2]/button")
el.click()