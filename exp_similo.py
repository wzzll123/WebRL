# coding:utf-8
import time
import TestRepairRunner
import pickle

speedMode = True
# repairMode = "Hyb"
# repairMode="COLOR"
repairMode = "CNN"


with open('exp/web2url_exp.pkl', 'rb') as f:
    web2url = pickle.load(f)
choose_web = ['wikipedia']

for web in web2url.keys():
    # if web not in choose_web:
    #     continue
    url = web2url[web]['old_url']
    new_url = web2url[web]['new_url']
    # for script_name in experiment_constant.WEB2SCRIPT[web]:
    # cmd = 'python Main.py -t ' + script_name + ' -o ' + url + ' -n ' + new_url +
    script_name = web + '_similo'
    print("\n" + 'script name is: ' + script_name + "\n")
    test_repair_runner = TestRepairRunner.TestRepairRunner(script_name, url, new_url,
                                                           repairMode, speedMode,
                                                           chromeDriverPath='/Users/wzz/Desktop/chromedriver',
                                                           theta_dom=0.8,
                                                           theta_image=0.9)
    start = time.time()
    test_repair_runner.run_trace_repair()
    end = time.time()
    print("all time: " + str(end - start))
