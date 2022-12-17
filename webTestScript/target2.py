#coding=utf-8
#oldUrl="http://web.archive.org/web/20190617075414/https://www.target.com/"
#newUrl="https://web.archive.org/web/20220308054936/https://www.target.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("https://web.archive.org/web/20210108043803/https://www.target.com/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
el=driver.find_element_by_xpath("/html/body/div[3]/div/div[3]/div[2]/nav/a[7]")
#help
el.click()


