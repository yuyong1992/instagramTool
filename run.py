# coding:utf-8

import time
import os
import json


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 加载配置文件
conf_file = r"./config.json"
with open(conf_file, "r") as f:
    config = json.load(f)
# 脚本执行时间
run_time = config['run_time']


while True:
    time_now = time.strftime("%H:%M", time.localtime())
    if time_now in run_time:
        try:
            print('开始执行脚本')
            os.system('python3 instaApp.py')
        except Exception as e:
            # 执行关注脚本报错
            print('{} -- 执行关注脚本报错'.format(now()))
        os.system('killall -9 "Google Chrome"')
        print('{} -- 结束所有Chrome进程'.format(now()))
        os.system('killall -9 chromedriver')
        print('{} -- 结束所有chromedriver进程'.format(now()))
    time.sleep(60)
