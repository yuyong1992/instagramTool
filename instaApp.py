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
# 引入by方法
from selenium.webdriver.common.by import By
# 引入鼠标事件
from selenium.webdriver.common.action_chains import ActionChains
# 引入键盘事件
from selenium.webdriver.common.keys import Keys


class App(tk.Tk):
    def __init__(self, root):
        self.window = tk.Frame(root)
        self.window.grid()

    def ini_window(self):
        user1 = 'inspiration.drone'
        pwd1 = 'Hsnjhmx0'
        user2 = 'yuyong1992'
        pwd2 = 'yuyong12345'

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
        # # 日志输出框
        # self.text_log = tk.Text(self.window, font=font, height=10)
        # 登录语录账号
        self.but_login_quota =tk.Button(self.window, text='登录语录', command=lambda :self.login_insta(user1, pwd1), font=font)
        # 点赞
        self.but_like = tk.Button(self.window, text='点赞', command=self.like_post, font=font)

        # 元素布局
        self.but_open_browser.grid(column=0, row=0, pady=4)
        self.but_login_quota.grid(column=0, row=1, ipadx=8, pady=4)
        self.but_subscribe.grid(column=0, row=2, ipadx=24, pady=4, padx=4)
        self.but_like.grid(column=1, row=2, ipadx=24, pady=4, padx=4)
        self.but_stop_browser.grid(column=0, row=3, pady=4)
        self.but_end_script.grid(column=0, row=4, ipadx=24, pady=4)
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

    def now(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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

    def login_insta(self, username, password):
        # url_insta = r'http://www.instagram.com'
        # try:
        #     self.driver.get(url_insta)
        # except RecursionError:
        #     print('{} -- 没有实例化的浏览器，请先点击“打开浏览器”按钮'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        #     self.show_msg('没有实例化的浏览器，请先点击“打开浏览器”按钮')
        #     return
        # print('{} -- 访问Instagram'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        # sleep(2)
        self.open_browser()

        path_mail = '//*[@id="loginForm"]/div/div[1]/div/label/input'
        path_pwd = '//*[@id="loginForm"]/div/div[2]/div/label/input'
        path_login_but = '//*[@id="loginForm"]/div/div[3]/button'
        try:
            ele_username = self.driver.find_element_by_xpath(path_mail)
            ele_pwd = self.driver.find_element_by_xpath(path_pwd)
            ele_login_but = self.driver.find_element_by_xpath(path_login_but)
        except NoSuchElementException as e:
            print('{} -- 登录页面元素定位失败。{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), e))
            self.show_msg('登录页面元素定位失败，请检查网络连接后重试。{}'.format(e))
            return

        # 登录
        ele_username.clear()
        ele_username.send_keys(username)
        print('{} -- 输入用户名'.format(self.now()))

        ele_pwd.clear()
        ele_pwd.send_keys(password)
        print('{} -- 输入密码'.format(self.now()))

        ele_login_but.click()
        print('{} -- 点击登录按钮'.format(self.now()))
        # sleep(2)

        # 登录之后会出现询问是否保存登录信息的页面
        path_save_login = '//*[@id="react-root"]/section/main/div/div/div/section/div/button'
        # 处理询问是否保存登录信息的页面
        if self.isElementExist(path_save_login):
            ele_save_login = self.driver.find_element_by_xpath(path_save_login)
            # 保存登录信息
            ele_save_login.click()
            print('{} -- 是否保存登录信息：是'.format(self.now()))

        # sleep(2)

        path_personal = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img'
        if self.isElementExist(path_personal):
            print('{} -- {} 已经登录成功'.format(self.now(), username))
        else:
            print('{} -- 未进入首页!未找到元素{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), path_personal))
            self.show_msg('未进入首页!未找到元素{}，请重新运行脚本。'.format(path_personal))
            return

        # 登录之后询问是否开启消息通知，此处选择“下次再说”
        path_handle_notice = '/html/body/div[4]/div/div/div/div[3]/button[2]'
        # path_handle_notice = '//button[@class="aOOlW   HoLwm "]'
        path_notice_window = "//div[@class='piCib']"
        if self.isElementExist(path_notice_window):
            ele_handle_notice = self.driver.find_element_by_xpath(path_handle_notice)
            # 点击下次再选
            ele_handle_notice.click()
            print('{} -- 通知设置：下次再选'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

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
                            sleep(2)
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
                sleep(10)
        else:
            print('{} -- 该用户下没有粉丝！'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            self.show_msg('该用户下没有粉丝。')
            return

    def like_post(self):
        # 找到帖子的列表
        try:
            self.driver
        except RecursionError:
            print("{} -- 没有实例化的浏览器，请先点击“打开浏览器”按钮".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            self.show_msg('没有实例化的浏览器，请先点击“打开浏览器”按钮')
            return

        if not self.isElementExist('//div[@class="_9AhH0"]'):
            print('{} -- 当前页面没有帖子，定位到有帖子的页面后再点击“点赞按钮”'.format(self.now()))
            return

        sum_s = 0
        sum_e = 0
        # num = 0
        num_post = 0
        num_like = 0
        while True:
            ele_posts = self.driver.find_elements_by_class_name('_9AhH0')
            sum_s = len(ele_posts)
            # 模拟鼠标按下空格键再松开
            action = ActionChains(self.driver)
            action.key_down(Keys.SPACE).perform()
            action.key_up(Keys.SPACE).perform()
            print('{} -- 加载下一页帖子。。。'.format(self.now()))
            for ele_post in ele_posts:
                num_post += 1
                ele_post.location_once_scrolled_into_view
                sleep(1)
                self.driver.execute_script("arguments[0].scrollIntoView();", ele_post)
                # 打开帖子
                ele_post.click()
                print('{} -- 打开第 {} 个帖子'.format(self.now(), num_post))
                sleep(2)
                # 点赞按钮
                # path_but_like = '/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span/svg'
                path_but_like = '//div[@class="QBdPU "]'

                but_like = self.driver.find_elements_by_xpath(path_but_like)[1]
                if ('"赞"' or 'Like') in but_like.get_attribute('innerHTML'):
                    num_like += 1
                    but_like.click()
                    print('{} -- 第 {} 次点赞'.format(self.now(), num_like))

                # 关闭帖子
                path_but_close = '/html/body/div[5]/div[3]/button'
                self.driver.find_element_by_xpath(path_but_close).click()
                print('{} -- 关闭第 {} 个帖子'.format(self.now(), num_post))


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.geometry('500x300')
    root.title('instaTool')
    app.ini_window()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()
