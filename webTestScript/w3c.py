#coding=utf-8
#oldUrl="https://web.archive.org/web/20160104144745/http://www.w3schools.com/"
#newUrl="http://web.archive.org/web/20191031171902/https://www.w3schools.com/"
import time
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("file:///Users//Desktop/webProject/w3schools2016/index.html")
#driver.get("https://web.archive.org/web/20191101060559/https://www.w3schools.com/")
# click learn html
el=driver.find_element_by_xpath("//*[@id=\"main\"]/div[1]/div[1]/a[1]")
# learn sql
el=driver.find_element_by_xpath("//*[@id=\"main\"]/div[4]/div[1]/div/a")
# click the botton earth
el=driver.find_element_by_xpath("/html/body/div[2]/div/a[5]")
# click try it yourself
el=driver.find_element_by_link_text("Try it Yourself")
# click learn bootstrap
el=driver.find_element_by_xpath("/html/body/div[4]/div[5]/div[3]/a")
# click search
el=driver.find_element_by_xpath("/html/body/div[2]/div/a[4]")
# click colorpicker
el=driver.find_element_by_xpath("//*[@id=\"main\"]/div[5]/div[2]/a/img")
# certification
el=driver.find_element_by_link_text("WEB CERTIFICATES")
# like
el=driver.find_element_by_xpath("//*[@id=\"main\"]/footer/a[2]")
# tutorial
el=driver.find_element_by_xpath("/html/body/div[2]/div/a[1]")






