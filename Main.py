# coding:utf-8
import TestRepairRunner

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--testcase", dest="testMethod", type=str, default=None)
parser.add_argument("-o", "--oldUrl", dest="oldUrl", type=str, default=None)
parser.add_argument("-n", "--newUrl", dest="newUrl", type=str, default=None)
parser.add_argument("-m", "--mode", dest="mode", type=str, default=None)
parser.add_argument("-c", "--chromeDriverPath", dest="chromeDriverPath", type=str, default=None)


parser_args = parser.parse_args()
script_name = parser_args.testMethod
url=parser_args.oldUrl
new_url=parser_args.newUrl
repairMode=parser_args.mode
test_repair_runner = TestRepairRunner.TestRepairRunner(script_name, url, new_url,
                                                               repairMode,chromeDriverPath=parser_args.chromeDriverPath)
test_repair_runner.run_trace_repair()

