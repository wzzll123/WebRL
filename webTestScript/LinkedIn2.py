#coding=utf-8
#oldUrl="http://web.archive.org/web/20200818001215/https://www.linkedin.com/"
#newUrl="http://web.archive.org/web/20210809005904/https://www.linkedin.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20200818001215/https://www.linkedin.com/")
# driver.get("http://web.archive.org/web/20210809005904/https://www.linkedin.com/")
# sign in
el=driver.find_element_by_xpath("/html/body/nav/a[3]")
el.click()