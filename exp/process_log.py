import re

from constant import web2url
import os
import csv


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


def process_log(log_path, similo_path, manual_path, mode="normal"):
    if mode == "normal":
        web2result = read_pre(similo_path, manual_path)
    elif mode == "manual":
        web2result = read_manual_csv(manual_path, {})
    elif mode == "similo":
        web2result = read_similo(similo_path)

    # print(web2result)
    with open(log_path, 'r') as log:
        num_broken = 0
        web = None
        old_xpath = None
        step_num = -1
        lines = log.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if 'script name is:' in line:
                web = line.split(': ')[1].split('_')[0]
                web2result[web]['num_broken'] = 0
                web2result[web]['num_correct'] = 0
                web2result[web]['detail'] = {}
                web2result[web]['for_vista'] = {}
            elif 'xpath of test step' in line:
                old_xpath = line.split(': ')[1][:-1]
                step_num = int(line.split(': ')[0].split(' ')[-1])
                web2result[web]['detail'][old_xpath] = 'not broken'

            elif 'trace time' in line:
                trace_time_pattern = r"trace time: (\d+(?:\.\d+)?)"
                trace_time_match = re.search(trace_time_pattern, line)
                trace_time = float(trace_time_match.group(1))
                web2result[web]['trace_time'] = trace_time
            elif 'chrome initial time' in line:
                initial_time_pattern = r"chrome initial time: (\d+(?:\.\d+)?)"
                initial_time_match = re.search(initial_time_pattern, line)
                initial_time = float(initial_time_match.group(1))
                web2result[web]['initial_time'] = initial_time
            elif 'all time:' in line:
                all_time_pattern = r"all time: (\d+(?:\.\d+)?)"
                all_time_match = re.search(all_time_pattern, line)
                all_time = float(all_time_match.group(1))
                web2result[web]['all_time'] = all_time

            elif 'encounter a broken test step' in line:
                web2result[web]['num_broken'] += 1
                web2result[web]['detail'][old_xpath] = 'false'
            elif 'xpath of candidate is:' in line:
                new_xpath = lines[i + 1][:-1]
                pre_old_xpath = old_xpath
                if 'svg' in old_xpath or 'svg' in new_xpath:
                    old_xpath = covert_xpath_locator(old_xpath)
                    new_xpath = covert_xpath_locator(new_xpath)
                # if web2result[web]['xpath_pair'][old_xpath] == new_xpath:
                if (web2result[web]['xpath_pair'][old_xpath] in new_xpath or new_xpath in web2result[web]['xpath_pair'][
                    old_xpath] ):
                    # and abs(len(new_xpath.split('/')) - len(web2result[web]['xpath_pair'][old_xpath].split('/'))) < 4:
                        # print('dayu', new_xpath,web2result[web]['xpath_pair'][old_xpath])
                    web2result[web]['detail'][pre_old_xpath] = 'true'
                    web2result[web]['num_correct'] += 1
                else:
                    pass
                    # print('web {} fails to generate correct repair, old_xpath is {}, new xpath should be {}, '
                    #       'but is {}'.format(web, old_xpath, web2result[web]['xpath_pair'][old_xpath], new_xpath))
    num_broken = 0
    num_correct = 0
    for web in web2result:
        # print(
        #     'web {}, num of locators {}, broken locators {}. correct repair {}'.format(web,
        #                                                                                web2result[web]['num_locator'],
        #                                                                                web2result[web]['num_broken'],
        #                                                                                web2result[web]['num_correct']))
        if 'num_correct' not in web2result[web]:
            continue
        num_broken += web2result[web]['num_broken']
        num_correct += web2result[web]['num_correct']
    print(num_broken, num_correct)
    return web2result


if __name__ == '__main__':
    # log_path = '/Users/wzz/Desktop/Research/scriptRepair/WebRL/report/parameter/image0.8_dom0.8_image10_combine3'
    log_path = '/Users/wzz/Desktop/Research/scriptRepair/WebRL/report/shufflenet_v2_x1_0'
    similo_path = '/Users/wzz/Desktop/Research/scriptRepair/Similo2/WidgetLocator/apps'
    manual_path = '/Users/wzz/Desktop/Research/scriptRepair/WebRL/exp/manual_.csv'
    process_log(log_path, similo_path, manual_path, "normal")
