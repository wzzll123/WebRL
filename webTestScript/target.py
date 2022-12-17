#coding=utf-8
#oldUrl="http://web.archive.org/web/20190617075414/https://www.target.com/"
#newUrl="https://web.archive.org/web/20220308054936/https://www.target.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("https://web.archive.org/web/20210108043803/https://www.target.com/")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
el=driver.find_element_by_xpath("//*[@id=\"select-7\"]/button")
#help
el.click()
el=driver.find_element_by_link_text("Size Charts")
el.click()
# CV
