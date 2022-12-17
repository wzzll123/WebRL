#coding=utf-8
#oldUrl="http://web.archive.org/web/20180510001701/https://www.youtube.com/"
#newUrl="http://web.archive.org/web/20200609000027/https://www.youtube.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/Youtube2018/index.html")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
#search
el=driver.find_element_by_id("search-btn")
#guide
el=driver.find_element_by_id("appbar-guide-button")
#sign in
el=driver.find_element_by_xpath("//*[@id=\"yt-masthead-signin\"]/div/button")
# history
el=driver.find_element_by_xpath("//*[@id=\"guide_builder-guide-item\"]/a/span")
#browse
el=driver.find_element_by_xpath("//*[@id=\"guide_builder-guide-item\"]")
#browse2
el=driver.find_element_by_xpath("//*[@id=\"guide_builder-guide-item\"]/a/span")
#help
el=driver.find_element_by_xpath("//*[@id=\"google-help\"]")
#help2
el=driver.find_element_by_xpath("//*[@id=\"google-help\"]/span[1]")
# history
el=driver.find_element_by_xpath("//*[@id=\"history-guide-item\"]/a")
# history 2
el=driver.find_element_by_xpath("//*[@id=\"history-guide-item\"]/a/span")
#search input
el=driver.find_element_by_xpath("//*[@id=\"masthead-search-term\"]")
driver.quit()



