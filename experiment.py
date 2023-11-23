# coding:utf-8
import time
import TestRepairRunner
import experiment_constant
speedMode= True
repairMode="Hyb"

for web in experiment_constant.WEB2SCRIPT.keys():
    url = experiment_constant.WEB2URL[web]['oldurl']
    new_url = experiment_constant.WEB2URL[web]['newurl']
    for script_name in experiment_constant.WEB2SCRIPT[web]:
        # cmd = 'python Main.py -t ' + script_name + ' -o ' + url + ' -n ' + new_url +
        print("\n"+script_name+"\n")
        test_repair_runner = TestRepairRunner.TestRepairRunner(script_name, url, new_url,
                                                               repairMode,speedMode,chromeDriverPath='/Users/wzz/Desktop/chromedriver')
        start = time.time()
        test_repair_runner.run_trace_repair()
        end = time.time()
        print("all time: " + str(end - start))




# script_list = ['walmart_home']
# url = "file:///Users/wzz/Desktop/webProject/walmart2018/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/walmart2020/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()

# script_list = ['w3c1','w3c2','w3c3']
# script_list = ['w3c1']
# url = "file:///Users/wzz/Desktop/webProject/w3schools2016/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/w3schools2019/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     start = time.time()
#     test_repair_runner.run_trace_repair()
#     end = time.time()
#     print("time: "+ str(end-start))
#
# script_list = ['ebay','ebay2']
# url = "file:///Users/wzz/Desktop/webProject/ebay2019/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/ebay2022/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
# #
# script_list = ['office', 'office2', 'office3']
# url = "file:///Users/wzz/Desktop/webProject/office2018/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/office2020/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
# #
# script_list = ['msn', 'msn2']
# url = "file:///Users/wzz/Desktop/webProject/msn2020/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/msn2021/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
#
# script_list = ['yahoo', 'yahoo2']
# # script_list = ['yahoo2']
# url = "file:///Users/wzz/Desktop/webProject/yahoo2020/Yahoo.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/yahoo2022/Yahoo.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
#
# script_list = ['microsoft', 'microsoft2']
# url = "file:///Users/wzz/Desktop/webProject/microsoft2020/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/microsoft2022/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
#
# script_list = ['weather', 'weather2','weather3']
# url = "file:///Users/wzz/Desktop/webProject/weather2020/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/weather2022/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
#
#
#
#
#
#
# script_list = ['booking','booking2']
# url = "file:///Users/wzz/Desktop/webProject/booking2018/index.en-gb.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/booking2020/index.en-gb.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
#
#
#
# script_list = ['chase','chase2']
# url = "http://1.117.174.176/chase2021/"
# newUrl = "http://1.117.174.176/chase2022/"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
#
# script_list = ['cdc','cdc2']
# url = "file:///Users/wzz/Desktop/webProject/cdc2018/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/cdc2022/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
#
# script_list = ['healthline2']
# url = "file:///Users/wzz/Desktop/webProject/healthline2021/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/healthline2022/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
#
# script_list = ['Uber','Uber2']
# url = "file:///Users/wzz/Desktop/webProject/Uber2020/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/Uber2022/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
#
# script_list = ['Youtube','Youtube2','Youtube3']
# url = "file:///Users/wzz/Desktop/webProject/Youtube2018/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/Youtube2020/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
#
# script_list = ['LinkedIn','LinkedIn2']
# url = "file:///Users/wzz/Desktop/webProject/linkedin2020/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/linkedin2021/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
# script_list = ['tripadvisor','tripadvisor2','tripadvisor3']
# url = "http://1.117.174.176/tripadvisor2019/"
# newUrl = "http://1.117.174.176/tripadvisor2022/"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
# # #
# # #
# # not full screen
# script_list = ['Fandom','Fandom2','Fandom3']
# url = "file:///Users/wzz/Desktop/webProject/fandom2020/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/fandom2022/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
#
#
#
# script_list = ['paypal2']
# url = "file:///Users/wzz/Desktop/webProject/paypal2021/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/paypal2022/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()
# script_list = ['allrecipes','allrecipes2','allrecipes3']
# url = "file:///Users/wzz/Desktop/webProject/allrecipes2019/index.html"
# newUrl = "file:///Users/wzz/Desktop/webProject/allrecipes2022/index.html"
# for script_name in script_list:
#     functionName=script_name
#     webName = script_name
#     cmd='python Main.py --webName '+webName+' --testcase '+functionName+' --oldUrl '+url+' --newUrl '+newUrl
#     print(cmd)
#     test_repair_runner = TestRepairRunner.TestRepairRunner(webName, functionName, url, newUrl)
#     test_repair_runner.run_trace_repair()