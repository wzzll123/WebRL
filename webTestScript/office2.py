#coding=utf-8
#oldUrl="http://web.archive.org/web/20180518005533/https://office.com/"
#newUrl="http://web.archive.org/web/20200522054136/https://www.office.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20180518005533/https://office.com/")
# driver.get("http://web.archive.org/web/20200522054136/https://www.office.com/")
# sign in
el=driver.find_element_by_xpath("//*[@id=\"hero-section\"]/div/ul/li[2]")
el.click()
driver.quit()


