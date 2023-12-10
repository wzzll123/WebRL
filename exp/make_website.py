import json
import os
from os import path
import subprocess
from selenium import webdriver
import pickle
import json
import csv
import re
from selenium.common.exceptions import NoSuchElementException

from constant import web2url

from selenium.webdriver.chrome.options import Options


def gen_xpath_locator(element, xpath):
    # for svg element that will cause syntax error
    xpath_with_single_quotes = xpath.replace('"', "'")
    return 'el = driver.find_element_by_xpath(\"' + xpath_with_single_quotes + '\")'


def gen_id_locator(element):
    element_id = element.get_attribute('id')
    return 'el = driver.find_element_by_id(\"' + element_id + '\")'


def gen_name_locator(element):
    element_name = element.get_attribute('name')
    return 'el = driver.find_element_by_name(\"' + element_name + '\")'


def gen_link_text_locator(element):
    link_text = element.text
    return 'el = driver.find_element_by_link_text(\"' + link_text + '\")'


def make_website_dir(web, web_dir, old_dir, new_dir):
    if not path.exists(web_dir):
        print("command: " + 'mkdir ' + web_dir)
        os.system('mkdir ' + web_dir)
    if not path.exists(old_dir):
        print("command: " + 'mkdir ' + old_dir)
        os.system('mkdir ' + old_dir)
    if not path.exists(new_dir):
        os.system('mkdir ' + new_dir)
def covert_xpath_locator(xpath: str):
    return xpath.replace('svg', '*[local-name() = "svg"]')


def convert_absolute_xpath(absolute_xpath: str):
    # covert /html/body to /html[1]/body[1]
    # Split the absolute XPath into individual elements
    elements = absolute_xpath.split('/')[1:]
    normalized_xpath = ""

    for i, element in enumerate(elements):
        # Extract the element name and index (if present)
        match = re.match(r"([a-zA-Z0-9\-]+)(?:\[(\d+)\])?", element)

        if match:
            tag_name = match.group(1)
            index = match.group(2)
            # Build the normalized XPath
            normalized_xpath += f"/{tag_name}[{index or 1}]"
        elif 'local-name' in element:
            normalized_xpath = normalized_xpath + '/' + element + '[1]'
        else:

            raise ValueError("Invalid absolute XPath format")
    # print(absolute_xpath, normalized_xpath)
    return normalized_xpath
def read_manual_csv(manual_path, web2result: dict):
    with open(manual_path, 'r') as file:
        csv_reader = csv.reader(file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                web = row[0]
                old_xpath = row[1]
                new_xpath = row[2]
                if old_xpath == '' or new_xpath == '':
                    continue
                old_xpath = convert_absolute_xpath(covert_xpath_locator(old_xpath))

                new_xpath = convert_absolute_xpath(covert_xpath_locator(new_xpath))
                if web not in web2result:
                    web2result[web] = {}
                    web2result[web]['xpath_pair'] = {}
                    web2result[web]['num_locator'] = 0
                web2result[web]['xpath_pair'][old_xpath] = new_xpath
                web2result[web]['num_locator'] += 1

                line_count += 1
    return web2result


def read_similo(similo_path):
    web2result = {}
    exclude_web = ['youtube', 'cnn']
    for web in web2url:
        if web in exclude_web:
            continue
        # get property
        property_dir = similo_path + '/' + web.capitalize()
        property_files = [name for name in os.listdir(property_dir)
                          if name.endswith('properties')]
        web2result[web] = {}
        web2result[web]['property_list'] = property_files
        web2result[web]['xpath_pair'] = {}
        for property_file in property_files:
            with open(property_dir + '/' + property_file) as f:
                line = f.readline()
                old_xpath = line.split('=', 1)[1][:-1]
                line = f.readline()
                new_xpath = line.split('=', 1)[1][:-1]
                web2result[web]['xpath_pair'][old_xpath] = new_xpath
        web2result[web]['num_locator'] = len(property_files)
    return web2result


def read_pre(similo_path, manual_path):
    web2result = read_similo(similo_path)
    web2result = read_manual_csv(manual_path, web2result)
    return web2result

if __name__ == '__main__':

    web2url_exp = {}
    cmd_wget = 'wget -P {} --page-requisites --convert-links {}'
    with open('config.json','r') as f:
        config = json.load(f)
    root_dir = config['root_dir']

    similo_path = config['similo_path']
    manual_path = os.path.join(root_dir,'exp','manual_.csv')
    # web2result = read_similo(similo_path)
    web2result = read_pre(similo_path, manual_path)
    # web2result = read_manual_csv(manual_path, {})
    # print(web2url.keys())
    for web in web2result:
        # if web != "youtube":
        #     continue
        # print("web: {}".format(web))
        print('\'' + web + '\'', end=',')
        web_dir = root_dir + 'website' + '/' + web
        old_dir = web_dir + '/' + 'old'
        new_dir = web_dir + '/' + 'new'

        make_website_dir(web, web_dir, old_dir, new_dir)

        # if len(os.listdir(old_dir)) == 0:
        #     # print("command: " + cmd_wget.format(old_dir, web2url[web]['old_url']))
        #     os.system(cmd_wget.format(old_dir, web2url[web]['old_url']))
        # if len(os.listdir(new_dir)) == 0:
        #     os.system(cmd_wget.format(new_dir, web2url[web]['new_url']))

        old_url = subprocess.check_output("find {} -name index.html | head -1".format(old_dir), shell=True)
        old_url = old_url.decode('utf-8')[:-1]
        new_url = subprocess.check_output("find {} -name index.html | head -1".format(new_dir), shell=True)
        new_url = new_url.decode('utf-8')[:-1]
        web2url_exp[web] = {}
        if old_url != '':
            web2url_exp[web]['old_url'] = 'file://' + old_url
        else:
            web2url_exp[web]['old_url'] = web2url[web]['old_url']

        if new_url != '':
            web2url_exp[web]['new_url'] = 'file://' + new_url
        else:
            web2url_exp[web]['new_url'] = web2url[web]['new_url']
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome("/Users/wzz/Desktop/chromedriver", chrome_options=chrome_options)
        driver_new = webdriver.Chrome("/Users/wzz/Desktop/chromedriver", chrome_options=chrome_options)
        driver.get(web2url_exp[web]['old_url'])
        driver_new.get(web2url_exp[web]['new_url'])
        script_dir = root_dir + 'webTestScript'
        chrome_str = "driver = webdriver.Chrome(\"{}\")\ndriver.get(\"{}\")\n"
        with open(script_dir + '/' + web + '_similo' + '.py', 'w') as script:
            script.write("import time\nfrom selenium import webdriver\n")
            script.write(chrome_str.format("/Users/wzz/Desktop/chromedriver", web2url_exp[web]['old_url']))
            # for property_file in property_files:
            #     with open(property_dir+'/'+property_file) as f:
            #         line = f.readline()
            #         old_xpath = line.split('=', 1)[1][:-1]
            #         line = f.readline()
            #         new_xpath = line.split('=', 1)[1][:-1]
            i = 0
            for old_xpath, new_xpath in web2result[web]['xpath_pair'].items():
                i += 1
                try:
                    element = driver_new.find_element_by_xpath(new_xpath)
                except Exception as e:
                    print("new: {} get exception in {}\n{}".format(web, old_xpath, e))
                    continue

                try:
                    element = driver.find_element_by_xpath(old_xpath)
                except Exception as e:
                    print("old: {} get exception in {}\n{}".format(web, old_xpath, e))
                    continue

                if element.get_attribute("id") is not None and element.get_attribute("id") != '':
                    element_id = element.get_attribute("id")
                    try:
                        element_by_attr = driver.find_element_by_id(element_id)
                        if element_by_attr == element:
                            script.write(gen_id_locator(element) + '\n')
                        else:
                            script.write(gen_xpath_locator(element, old_xpath) + '\n')

                    except NoSuchElementException:
                        script.write(gen_xpath_locator(element, old_xpath) + '\n')

                elif element.get_attribute("name") is not None and element.get_attribute("name") != '':
                    element_name = element.get_attribute("name")
                    try:
                        element_by_attr = driver.find_element_by_name(element_name)
                        if element_by_attr == element:
                            script.write(gen_name_locator(element) + '\n')
                        else:
                            script.write(gen_xpath_locator(element, old_xpath) + '\n')
                    except NoSuchElementException:
                        script.write(gen_xpath_locator(element, old_xpath) + '\n')

                elif element.tag_name == 'a':
                    link_text = element.text
                    if link_text == '' or '\n' in link_text:
                        script.write(gen_xpath_locator(element, old_xpath) + '\n')
                        continue
                    try:
                        element_by_attr = driver.find_element_by_link_text(link_text)
                        if element_by_attr == element:
                            script.write(gen_link_text_locator(element) + '\n')
                        else:
                            script.write(gen_xpath_locator(element, old_xpath) + '\n')
                    except NoSuchElementException:
                        script.write(gen_xpath_locator(element, old_xpath) + '\n')

                else:
                    script.write(gen_xpath_locator(element, old_xpath) + '\n')

        driver.quit()
        driver_new.quit()
    with open('web2url_exp.pkl', 'wb') as f:
        pickle.dump(web2url_exp, f)
        # print(json.dumps(web2url_exp,indent=4))

    # data = []
    # for web in web2url:
    #     tmp = [web]
    #     for i in range(5):
    #         data.append(tmp)
    # write_to_csv(data, "manual.csv")
