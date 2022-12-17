#coding=utf-8
#oldUrl="http://web.archive.org/web/20200107001908/https://www.yahoo.com/"
#newUrl="http://web.archive.org/web/20220221000940/https://www.yahoo.com/"
from selenium import webdriver
driver=webdriver.Chrome("/Users//Desktop/chromedriver")
driver.get("http://web.archive.org/web/20200107001908/https://www.yahoo.com/")
# search
el=driver.find_element_by_id("header-search-input")
el.send_keys("weather")
el=driver.find_element_by_id("header-desktop-search-button")
el.click()
driver.quit()


