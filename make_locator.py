# encoding=utf-8
from selenium import webdriver
import experiment_constant
from selenium.common.exceptions import WebDriverException


def check_interactive(element):
    # check send_keys
    try:
        element.send_keys("a")
        element.clear()
        return True
    except WebDriverException:
        pass

    # check clickable
    return body.is_enabled() and body.is_displayed()


# for web in experiment_constant.WEB2URL.keys():
for web in ['amazon']:
    interactive_elements = []
    driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver")
    url = experiment_constant.WEB2URL[web]["oldurl"]
    driver.get(url)
    body = driver.find_element_by_xpath("/html/body")
    all_children_by_xpath = body.find_elements_by_xpath(".//*")
    print("the length of elements list is " + str(len(all_children_by_xpath)))
    for child in all_children_by_xpath:
        if check_interactive(child):
            interactive_elements.append(child)
    print("the length of interactive elements list is " + str(len(interactive_elements)))
