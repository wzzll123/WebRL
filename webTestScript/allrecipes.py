#coding=utf-8
#oldUrl="https://web.archive.org/web/20190115022528/https://www.allrecipes.com/"
#newUrl="https://web.archive.org/web/20220215010622/https://www.allrecipes.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/allrecipes2019/index.html")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")

# el = driver.find_element_by_xpath("/html/body/header/nav/div/div/button")
# # menu
# el.click()



# el=driver.find_element_by_xpath("/html/body/div[1]/div[2]/header/section[2]/ul/li[9]")
#menu
# el.click()



# CV

el=driver.find_element_by_xpath("/html/body/div[1]/div[2]/header/section[2]/ul/li[9]")
el.click()
el=driver.find_element_by_link_text("Allrecipes Magazine")
el.click()
