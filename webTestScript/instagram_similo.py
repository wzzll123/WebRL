import time
from selenium import webdriver
driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
driver.get("file:///Users/wzz/Desktop/Research/scriptRepair/WebRL/website/instagram/old/index.html")
el = driver.find_element_by_xpath("/html[1]/body[1]/span[1]/section[1]/main[1]/article[1]/div[2]/div[3]/p[1]")
el = driver.find_element_by_link_text("HASHTAGS")
el = driver.find_element_by_xpath("/html[1]/body[1]/span[1]/section[1]/main[1]/article[1]/div[2]/div[1]/div[1]/form[1]/div[5]/div[1]/div[1]/label[1]")
el = driver.find_element_by_link_text("API")
el = driver.find_element_by_xpath("/html[1]/body[1]/span[1]/section[1]/main[1]/article[1]/div[2]/div[3]/div[1]/a[1]")
el = driver.find_element_by_link_text("ABOUT US")
el = driver.find_element_by_link_text("TERMS")
el = driver.find_element_by_xpath("/html[1]/body[1]/span[1]/section[1]/main[1]/article[1]/div[2]/div[1]/h1[1]")
el = driver.find_element_by_xpath("/html[1]/body[1]/span[1]/section[1]/main[1]/article[1]/div[2]/div[1]/div[1]/form[1]/div[6]/span[1]")
el = driver.find_element_by_link_text("JOBS")
el = driver.find_element_by_xpath("/html[1]/body[1]/span[1]/section[1]/main[1]/article[1]/div[2]/div[3]/div[1]/a[2]")
el = driver.find_element_by_link_text("PRIVACY")
el = driver.find_element_by_xpath("/html[1]/body[1]/span[1]/section[1]/main[1]/article[1]/div[2]/div[1]/div[1]/form[1]/div[2]/div[1]/div[1]/label[1]")
el = driver.find_element_by_link_text("Log in")
el = driver.find_element_by_link_text("BLOG")
el = driver.find_element_by_xpath("/html[1]/body[1]/span[1]/section[1]/main[1]/article[1]/div[2]/div[3]/div[1]/a[1]/img[1]")
el = driver.find_element_by_xpath("/html[1]/body[1]/span[1]/section[1]/main[1]/article[1]/div[2]/div[3]/div[1]/a[2]/img[1]")
