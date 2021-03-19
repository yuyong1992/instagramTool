# coding=utf-8

import tkinter as tk
from tkinter import messagebox
# from tkinter import ttk
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import sys
import random
import time


class App(tk.Tk):
    def __init__(self, root):
        self.window = tk.Frame(root)
        self.window.grid()

    def ini_window(self):

        # 元素的文本样式
        font = ('Microsoft YaHei', 12)

        # 元素定义
        # 打开浏览器
        self.but_open_browser = tk.Button(self.window, text='打开浏览器', command=self.open_browser, font=font)
        # 关闭浏览器
        self.but_stop_browser = tk.Button(self.window, text='关闭浏览器', command=self.stop_browser, font=font)
        # 结束脚本
        self.but_end_script = tk.Button(self.window, text='退出', command=self.end_script, font=font)
        # 点击关注
        self.but_subscribe = tk.Button(self.window, text='关注', command=self.subscribe_user, font=font)
        # 日志输出框
        self.text_log = tk.Text(self.window, font=font, height=10)

        # 元素布局
        self.but_open_browser.grid(column=0, row=0, padx=10)
        self.but_stop_browser.grid(column=0, row=2, padx=10)
        self.but_subscribe.grid(column=0, row=1, padx=10)
        self.but_end_script.grid(column=0, row=3, padx=10)
        # self.text_log.grid(column=1, row=0, rowspan=4)

    # def get_opt(self):
    #     opt = self.combox.get()
    #     return opt

    # def print_user(self):
    #     uname, pwd = self.get_user()
    #     print(uname, pwd)

    # def get_user(self):
    #     uname = self.username_mine.get()
    #     pwd = self.pwd_mine.get()
    #     return uname, pwd

    def out_log(self, log):
        log = '*** {} \n'.format(log)
        self.text_log.insert(tk.END, log)
        self.text_log.see(tk.END)
        self.text_log.update()
        if len(self.text_log.get(1.0, tk.END)) >= 500:
            self.text_log.delete(1.0, 2.0)

    def show_msg(self, message):
        tk.messagebox.askyesno(title='提示', message='提示：{}'.format(message))

    def isElementExist(self, path):
        flag = True
        try:
            self.driver.find_element_by_xpath(path)
            return flag
        except NoSuchElementException:
            flag = False
            return flag
        except RecursionError:
            # print('请先点击“打开浏览器”按钮')
            print('{} -- 请先点击“打开浏览器”按钮'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ))
            return

    def open_browser(self):
        base_url = 'https://www.instagram.com/'
        # target_url = '{}{}'.format(base_url, target_user)
        try:
            chrome_options = webdriver.ChromeOptions()

            # chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("no-sandbox")
            chrome_options.add_argument("disable-extensions")
            chrome_options.add_argument("no-default-browser-check")
            # # 加载chrome浏览器的插件
            # chrome_options.add_argument("--user-data-dir="+r"/Users/shanhui/Library/Application Support/Google/Chrome/")
            # chrome_options.add_argument("--user-data-dir="+r"C:\Users\DELL\AppData\Local\Google\Chrome\User Data\\")
            prefs = {"": ""}
            prefs["credentials_enable_service"] = False
            prefs["profile.password_manager_enabled"] = False
            # prefs["excludeSwitches"] = ['enable-automation', 'enable-logging']
            chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
            chrome_options.add_experimental_option("prefs", prefs)

            self.driver = webdriver.Chrome(chrome_options=chrome_options)
            print("{} -- 打开浏览器".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            self.driver.get(base_url)
            print("{} -- 访问Instagram".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ))
            # self.driver.maximize_window()
            # print("浏览器全屏")
            self.driver.implicitly_wait(10)

            sleep(1)
        except Exception as e:
            print('{} -- 访问Instagram登录页面失败：{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), e))
            self.driver.quit()
            self.show_msg('访问Instagram登录页面失败，请检查网络连接后重试。{}'.format(e))
            return

    def stop_browser(self):
        try:
            self.driver.quit()
        except RecursionError:
            print('{} -- 没有实例化的浏览器，请先点击“打开浏览器”按钮'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            self.show_msg("没有实例化的浏览器，请先点击“打开浏览器”按钮")

    def end_script(self):
        # 退出脚本执行
        sys.exit()

    def subscribe_user(self):
        # 打开粉丝列表
        path_fans_list = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a'
        # class_but_subscribe = r'sqdOP  L3NKy   y3zKF     '
        path_but_subscribe = "//button[contains(@class, 'sqdOP') and contains(@class, 'L3NKy')]"

        try:
            self.driver
        except RecursionError:
            print("{} -- 没有实例化的浏览器，请先点击“打开浏览器”按钮".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            self.show_msg('没有实例化的浏览器，请先点击“打开浏览器”按钮')
            return
        if self.isElementExist(path_fans_list):
            ele_fans_list = self.driver.find_element_by_xpath(path_fans_list)
            try:
                ele_fans_list.click()
            except ElementClickInterceptedException:
                if self.isElementExist(path_but_subscribe):
                    print('{} -- 粉丝列表已打开'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                else:
                    print('{} -- 当前页面未找到粉丝列表。'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                    # self.driver.quit()
                    self.show_msg('当前页面未找到粉丝列表。')
                    return
            else:
                print('{} -- 打开粉丝列表'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                sleep(2)
        else:
            print('{} -- 当前页面未找到粉丝列表。'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            # self.driver.quit()
            self.show_msg('当前页面未找到粉丝列表。')
            return

        sum_s = 0
        sum_e = 0
        # num = 0
        num_sub = 0

        if self.isElementExist(path_but_subscribe):
            eles_but_subscribe = self.driver.find_elements_by_xpath(path_but_subscribe)
            sum_s = len(eles_but_subscribe)
            while True:
                try:
                    # div的滚动条操作
                    js = "document.getElementsByClassName('isgrP')[0].scrollTop=10000000"
                    self.driver.execute_script(js)
                    print('{} -- 加载粉丝列表下一页数据。。。'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                    sleep(2)
                except Exception as e:
                    print('{} -- 加载下一页数据异常！{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), e))
                    # self.driver.quit()
                    self.show_msg('加载粉丝列表下一页数据异常！{}'.format(e))
                    return
                # 所有的关注按钮
                eles_but_subscribe = self.driver.find_elements_by_xpath(path_but_subscribe)
                for ele_like_but in eles_but_subscribe:
                    # num += 1
                    if ele_like_but.text == '关注' or ele_like_but.text == 'Follow':
                        num_sub += 1
                        if not ele_like_but.is_displayed():
                            ele_like_but.location_once_scrolled_into_view
                            self.driver.execute_script("arguments[0].scrollIntoView();", ele_like_but)
                        sleep(2)
                        ele_like_but.click()
                        path_err = "/html/body/div[6]/div/div/div/div[1]/h3"
                        # TODO：如果有稍后再试的提示，关闭弹窗，sleep 30分钟后继续
                        if self.isElementExist(path_err):
                            # ele_msg_box = self.driver.find_element_by_xpath(path_err).text
                            # if ele_msg_box == '稍后重试':
                            print('{} -- 关注第 {} 个用户时，账号被限制，请明天再试。'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), num_sub))
                            self.show_msg('关注第 {} 个用户时，账号被限制，请明天再试。'.format(num_sub))
                            return
                        print('{} -- 已关注 {} 个用户'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), num_sub))
                        print('{} -- 等待10-20s，再关注下一个用户'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                        sleep(random.randint(10, 20))

                eles_but_subscribe = self.driver.find_elements_by_xpath(path_but_subscribe)
                sum_e = len(eles_but_subscribe)

                # # 没有加载出更多粉丝后，重复10次尝试加载
                # i = 0
                # for i in range(10):
                #     i += 1
                #     if sum_e != sum_s:
                #         break
                #     self.driver.execute_script(js)
                #     print('加载粉丝列表下一页数据。。。')
                #     sleep(10)
                #
                #     eles_but_subscribe = self.driver.find_elements_by_xpath(path_but_subscribe)
                #     sum_e = len(eles_but_subscribe)
                #
                # if sum_e == sum_s:
                #     print('已经加载该账号的所有 {} 个粉丝'.format(sum_e))
                #     break
                # sum_s = sum_e
                sleep(1)
        else:
            print('{} -- 该用户下没有粉丝！'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            self.show_msg('该用户下没有粉丝。')
            return


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.geometry('500x300')
    root.title('instaTool')
    app.ini_window()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()
