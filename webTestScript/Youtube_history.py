#coding=utf-8
#oldUrl="http://web.archive.org/web/20180510001701/https://www.youtube.com/"
#newUrl="http://web.archive.org/web/20200609000027/https://www.youtube.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/Youtube2018/index.html")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
# history
el=driver.find_element_by_xpath("//*[@id=\"history-guide-item\"]/a")
el.click()
driver.quit()

#注意要将webarchive上面的东西关掉





