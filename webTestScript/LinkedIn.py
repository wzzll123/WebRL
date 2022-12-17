#coding=utf-8
#oldUrl="http://web.archive.org/web/20200818001215/https://www.linkedin.com/"
#newUrl="http://web.archive.org/web/20210809005904/https://www.linkedin.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20200818001215/https://www.linkedin.com/")
# driver.get("http://web.archive.org/web/20210809005904/https://www.linkedin.com/")
# choose a topic to learning about
el=driver.find_element_by_xpath("/html/body/main/section[2]/div/div/div/div/div/label[1]/span")
el.click()