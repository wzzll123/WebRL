#coding=utf-8
#oldUrl="http://web.archive.org/web/20180518005533/https://office.com/"
#newUrl="http://web.archive.org/web/20200522054136/https://www.office.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/office2018/index.html")
# driver.get("http://web.archive.org/web/20200522054136/https://www.office.com/")
# xiang xia
el=driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/button")
el.click()
el=driver.find_element_by_xpath("//*[@id=\"social-media-twitter\"]")
el.click()
driver.quit()

