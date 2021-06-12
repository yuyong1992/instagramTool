# coding=utf-8
import ssl
import threading
# import tkinter as tk
# from tkinter import messagebox
# from tkinter import ttk
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
# 引入显性等待
from selenium.webdriver.support.wait import WebDriverWait as DW
# 引入用于对元素状态的判断条件
from selenium.webdriver.support import expected_conditions as EC
import sys
import random
import time
# 引入by方法
from selenium.webdriver.common.by import By
# 引入鼠标事件
from selenium.webdriver.common.action_chains import ActionChains
# 引入键盘事件
from selenium.webdriver.common.keys import Keys
import json
import smtplib
from email.mime.text import MIMEText


class App(object):
    """
    instagram
    """

    @staticmethod
    def now():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def is_element_exist(self, path):
        flag = True
        try:
            DW(self.driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH, path)))
            return flag
        except (TimeoutError, TimeoutException):
            print('{} -- 等待20s未找到该元素，path：{}'.format(self.now(), path))
            flag = False
            return flag
        except Exception as e:
            print('{} -- 定位元素时出现未知异常，path：{}; Err:{}'.format(self.now(), path, e))
            flag = False
            return flag

    @staticmethod
    def login_email(host, port, sender, pwd):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender, pwd)
        return server

    def send_email(self, subject=r'Instagram脚本中止通知', content=r'Instagram 脚本已停止运行，详情请查看控制台运行日志。'):
        host = "smtp.partner.outlook.cn"
        port = "587"
        sender = "yong.yu@sinnet-cloud.cn"
        pwd = "yuyong@12345"

        recipient = ["1305703064@qq.com", "yong.yu@sinnet-cloud.cn"]
        # subject = subject
        # content = content

        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ','.join(recipient)

        try:
            server = self.login_email(host, port, sender, pwd)
            print('{} -- 邮箱登录成功，用户名：{}'.format(self.now(), sender))
        except Exception as err:
            print('{} -- 邮箱登录失败。ERR：{}'.format(self.now(), err))
            return
        try:
            server.sendmail(sender, recipient, msg.as_string())
            print('{} -- 邮件发送成功'.format(self.now()))
        except Exception as err:
            print('{} -- 邮件发送失败。ERR：{}'.format(self.now(), err))
            return

    def stop_load_page(self):
        js_stop_load_page = r'window.stop()'
        self.driver.execute_script(js_stop_load_page)

    def open_browser(self, url):
        self.instagram_url = url
        try:
            chrome_options = webdriver.ChromeOptions()

            # chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            # chrome_options.add_argument("--start-maximized")
            # 禁用弹出窗口
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("no-sandbox")
            # chrome_options.add_argument("disable-extensions")
            chrome_options.add_argument("no-default-browser-check")
            # Support/Google/Chrome/") chrome_options.add_argument(
            # "--user-data-dir="+r"C:\Users\DELL\AppData\Local\Google\Chrome\User Data\\")
            chrome_options.set_capability("pageLoadStrategy", "eager")
            prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
            # prefs["excludeSwitches"] = ['enable-automation', 'enable-logging']
            chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
            chrome_options.add_experimental_option("prefs", prefs)

            self.driver = webdriver.Chrome(options=chrome_options)
            print("{} -- 打开浏览器".format(self.now()))
            self.driver.get(self.instagram_url)
            print("{} -- 访问Instagram".format(self.now()))
            self.driver.maximize_window()
            # print("浏览器全屏")
            self.driver.implicitly_wait(20)
            sleep(1)
            # return self.driver
        except Exception as e:
            print('{} -- 访问Instagram登录页面失败：{}'.format(self.now(), e))
            self.driver.quit()
            return

    def close_browser(self):
        try:
            self.driver.quit()
        except RecursionError:
            print('{} -- 没有实例化的浏览器，无需关闭'.format(self.now()))
        except Exception as e:
            print('{} -- 未知异常，关闭浏览器实例失败 {}'.format(self.now(), e))

    # @staticmethod
    def end_script(self):
        # 关闭浏览器
        try:
            self.close_browser()
            print('{} -- 关闭浏览器'.format(self.now()))
        except AttributeError:
            print('{} -- 没有运行的浏览器实例，无需关闭'.format(self.now()))
        except Exception as e:
            print('{} -- 未知异常，退出浏览器实例失败  {}'.format(self.now(), e))
        # 退出脚本执行
        print('{} -- 结束脚本'.format(self.now()))
        sys.exit()

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def login_insta(self, username, password):
        # self.instagram_url = 'https://www.instagram.com/'
        # self.open_browser(self.instagram_url)
        print('{} -- 准备登录的用户：{}'.format(self.now(), username))
        # try:
        #     if self.driver.current_url != self.instagram_url:
        #         print('{} -- 当前页面url：{}'.format(self.now(), self.driver.current_url))
        #         if 'Instagram' in self.driver.title:
        #             print('{} -- 当前已经登录Instagram'.format(self.now()))
        #             return
        #         print('{} -- 当前不在Instagram登录页面，当前页面url：{}'.format(self.now(), self.driver.title))
        #         self.driver.get(self.instagram_url)
        #         print('{} -- 跳转到Instagram登录页面'.format(self.now()))
        # except RecursionError:
        #     print('{} -- 当前没有浏览器实例'.format(self.now()))
        #     print('{} -- 重新创建浏览器实例，并访问Instagram网站'.format(self.now()))
        #     self.open_browser(self.instagram_url)

        path_mail = '//*[@id="loginForm"]/div/div[1]/div/label/input'
        path_pwd = '//*[@id="loginForm"]/div/div[2]/div/label/input'
        path_login_but = '//*[@id="loginForm"]/div/div[3]/button'
        try:
            DW(self.driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, path_mail)))
            ele_username = self.driver.find_element_by_xpath(path_mail)
            print('{} -- 已定位到用户名输入框'.format(self.now()))
            DW(self.driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, path_pwd)))
            ele_pwd = self.driver.find_element_by_xpath(path_pwd)
            print('{} -- 已定位到密码输入框'.format(self.now()))
            DW(self.driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, path_login_but)))
            ele_login_but = self.driver.find_element_by_xpath(path_login_but)
            print('{} -- 已定位到登录按钮'.format(self.now()))
        except NoSuchElementException as e:
            print('{} -- 登录页面元素定位失败。{}'.format(self.now(), e))
            return
        except TimeoutException:
            print('{} -- 登录页面长时间未能定位到输入框或【登录】按钮'.format(self.now()))
            # self.close_browser()
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

        # 登录之后会出现询问是否保存登录信息的页面
        path_save_login = '//*[@id="react-root"]/section/main/div/div/div/section/div/button'
        # 处理询问是否保存登录信息的页面
        if self.is_element_exist(path_save_login):
            DW(self.driver, 20, 0.5).until(EC.element_to_be_clickable((By.XPATH, path_save_login)))
            ele_save_login = self.driver.find_element_by_xpath(path_save_login)
            # 保存登录信息
            ele_save_login.click()
            print('{} -- 是否保存登录信息：是'.format(self.now()))

        path_personal = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img'
        if self.is_element_exist(path_personal):
            print('{} -- {} 已经登录成功'.format(self.now(), username))
        else:
            print('{} -- 未进入首页!未找到主页头像元素：{}'.format(self.now(), path_personal))
            return

        # 登录之后询问是否开启消息通知，此处选择“下次再说”
        path_handle_notice = '/html/body/div[4]/div/div/div/div[3]/button[2]'
        # path_handle_notice = '//button[@class="aOOlW   HoLwm "]'
        path_notice_window = "//div[@class='piCib']"
        if self.is_element_exist(path_notice_window):
            DW(self.driver, 20, 0.5).until(EC.element_to_be_clickable((By.XPATH, path_handle_notice)))
            ele_handle_notice = self.driver.find_element_by_xpath(path_handle_notice)
            # 点击下次再选
            ele_handle_notice.click()
            print('{} -- 通知设置：下次再选'.format(self.now()))

    def logout_insta(self):
        # 回到主页
        self.driver.get(self.instagram_url)
        print('{} -- 回到主页'.format(self.now()))
        # 头像地址
        path_avatar = r'//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img'
        try:
            DW(self.driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH, path_avatar)))
        except TimeoutError:
            print('{} -- 未找到个人中心头像元素，不需要执行退出登录'.format(self.now()))
            return
        except TimeoutException:
            print('{} -- 未找到个人中心头像元素，不需要执行退出登录'.format(self.now()))
            return
        except Exception as e:
            print('{} -- 未知错误，定位个人中心的头像元素时出错 {}'.format(self.now(), e))
            return
        # 点击头像
        self.driver.find_elements_by_class_name('_6q-tv')[-1].click()
        print('{} -- 点击头像'.format(self.now()))
        # 退出按钮地址
        path_logout = r'//div[contains(text(), "退出")]'
        DW(self.driver, 20, 0.5).until(EC.visibility_of_any_elements_located((By.XPATH, path_logout)))
        ele_logout = self.driver.find_element_by_xpath(path_logout)
        print(ele_logout)
        ele_logout.click()
        print('{} -- 点击退出按钮'.format(self.now()))
        # 切换账号按钮
        path_switch = r'//button[contains(text(), "切换帐户") or contains(text(), "Switch Account")]'
        DW(self.driver, 20, 0.5).until(EC.element_to_be_clickable((By.XPATH, path_switch)))
        self.driver.find_element_by_xpath(path_switch).click()

    def subscribe_user(self, user, pwd, target_users, frequency, target_num):
        # 目标用户
        # target_users = target_users
        # 登录用户
        # try:
        #     self.login_insta(user, pwd)
        # except Exception as e:
        #     print('{} -- 登录失败，退出脚本.ERR：{}'.format(self.now(), e))
        #     content = '{} -- 登录失败，退出脚本.ERR：{}'.format(self.now(), e)
        #     self.send_email(content=content)
        #     return
        # 本次已经点击关注的个数
        num_sub = 0
        for target_user in target_users:
            print('{} -- 目标用户的用户名{}'.format(self.now(), target_user))
            try:
                self.driver
            except RecursionError:
                print("{} -- 没有实例化的浏览器".format(self.now()))
                self.login_insta(user, pwd)

            # 跳转到目标用户的主页
            target_url = '{}{}'.format(self.instagram_url, target_user)
            self.driver.get(target_url)
            print('{} -- 跳转到目标用户的主页{}'.format(self.now(), target_url))

            # 粉丝列表按钮
            path_fans_list = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a'

            for i in range(3):
                try:
                    print('{} -- 等待粉丝列表按钮出现'.format(self.now()))
                    DW(self.driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, path_fans_list)))
                    print('{} -- 粉丝列表按钮出现'.format(self.now()))
                    break
                except (TimeoutError, TimeoutException):
                    print('{} -- Timeout! 未找到粉丝列表'.format(self.now()))
                    print('{} -- 判断当前页面是否为目标用户主页'.format(self.now()))
                    if self.driver.current_url != target_url:
                        print('{} -- 当前页面的url'.format(self.driver.current_url))
                        print('{} -- 当前页面不是目标用户的主页'.format(self.now()))
                        print('{} -- 重新跳转到目标用户主页'.format(self.now()))
                        self.driver.get(target_url)
                if i == 2:
                    print('{} -- 第3次加载目标用户主页，没有找到粉丝列表按钮'.format(self.now()))
                    print('{} -- 结束当前账号 {} 执行'.format(self.now(), user))
                    # 邮件通知
                    content = '{} -- 结束当前账号 {} 执行'.format(self.now(), user)
                    self.send_email(content=content)
                    return

            # 粉丝列表的窗口标题
            path_fans_list_title = '/html/body/div[4]/div/div/div[1]/div'
            try:
                print('{} -- 点击粉丝列表按钮'.format(self.now()))
                ele_fans_list = self.driver.find_element_by_xpath(path_fans_list)
                ele_fans_list.click()
            except ElementClickInterceptedException:
                if self.is_element_exist(path_fans_list_title):
                    print('{} -- 粉丝列表已打开'.format(self.now()))
                else:
                    print('{} -- 当前页面未找到粉丝列表按钮，结束当前账号 {} 执行'.format(self.now(), user))
                    # 邮件通知
                    content = '{} -- 当前页面未找到粉丝列表按钮，结束当前账号 {} 执行'.format(self.now(), user)
                    self.send_email(content=content)
                    return
            except NoSuchElementException:
                print('{} -- 未知异常导致粉丝列表按钮丢失，结束当前账号 {} 执行'.format(self.now(), user))
                # 邮件通知
                content = '{} -- 未知异常导致粉丝列表按钮丢失，结束当前账号 {} 执行'.format(self.now(), user)
                self.send_email(content=content)
                return

            # if self.is_element_exist(path_fans_list_title):
            #     print('{} -- 粉丝列表已打开'.format(self.now()))

            # 关注按钮
            path_but_subscribe = "//button[contains(@class, 'sqdOP') and contains(@class, 'L3NKy')]"

            try:
                DW(self.driver, 5, 0.5).until(EC.presence_of_element_located((By.XPATH, path_but_subscribe)))
            except (TimeoutError, TimeoutException):
                print('{} -- 粉丝列表中没有【关注】按钮'.format(self.now()))
                print('{} -- 切换到另一个目标用户查找粉丝'.format(self.now()))
                continue

            num_s = 0
            num_e = 0

            while True:
                # 下拉加载粉丝列表
                for i in range(3):
                    try:
                        # div的滚动条操作
                        js = "document.getElementsByClassName('isgrP')[0].scrollTop=10000000"
                        self.driver.execute_script(js)
                        print('{} -- 加载粉丝列表下一页数据。。。'.format(self.now()))
                    except Exception as e:
                        print('{} -- 加载下一页数据异常，退出当前账号 {} 的执行！{}'.format(self.now(), user, e))
                        # 邮件通知
                        content = '{} -- 加载下一页数据异常，退出当前账号 {} 的执行！{}'.format(self.now(), user, e)
                        self.send_email(content=content)
                        return
                    # loading图标
                    path_loading = r'/html/body/div[5]/div/div/div[2]/ul/div/li[64]/div/svg'
                    for j in range(3):
                        try:
                            DW(self.driver, 10, 0.5).until_not(
                                EC.visibility_of_element_located((By.XPATH, path_loading)))
                            print('{} -- 等待加载完成、loading消失'.format(self.now()))
                            break
                        except (TimeoutError, TimeoutException):
                            print('{} -- 等待了10s仍在加载中，再等10s'.format(self.now()))
                        if j == 2:
                            print('{} -- 等待了30s仍在加载中'.format(self.now()))
                            print('{} -- 粉丝列表加载异常，退出当前账号 {} 的执行'.format(self.now(), user))
                            # 邮件通知
                            content = '{} -- 粉丝列表加载异常，退出当前账号 {} 的执行'.format(self.now(), user)
                            self.send_email(content=content)
                            return
                    # 所有的关注按钮
                    eles_but_subscribe = self.driver.find_elements_by_xpath(path_but_subscribe)
                    num_e = len(eles_but_subscribe)
                    print('{} -- 当前粉丝列表中粉丝数量：{}'.format(self.now(), num_e))
                    if num_e != num_s:
                        print('{} -- 加载完成'.format(self.now()))
                        break
                    if i == 2:
                        print('{} -- 第3次尝试，加载后粉丝数没有增加'.format(self.now()))
                        break
                    print('{} -- 加载后粉丝数与加载前粉丝数目相同，再尝试加载一次'.format(self.now()))
                    sleep(1)
                eles_but_subscribe = self.driver.find_elements_by_xpath(path_but_subscribe)
                for ele_like_but in eles_but_subscribe:
                    if ele_like_but.text == '关注' or ele_like_but.text == 'Follow':
                        num_sub += 1
                        if not ele_like_but.is_displayed():
                            # ele_like_but.location_once_scrolled_into_view
                            print('{} -- 把第 {} 个【关注】按钮移动到可见位置'.format(self.now(), num_sub))
                            self.driver.execute_script("arguments[0].scrollIntoView();", ele_like_but)
                        try:
                            ele_like_but.click()
                        except Exception as e:
                            path_err = "/html/body/div[6]/div/div/div/div[1]/h3"
                            if self.is_element_exist(path_err):
                                print('{} -- 关注第 {} 个用户时，账号 {} 被限制，退出当前账号执行! {}'.format(self.now(), num_sub, user, e))
                                # 邮件通知
                                content = '{} -- 关注第 {} 个用户时，账号 {} 被限制，退出当前账号执行! {}'.format(self.now(), num_sub, user, e)
                                self.send_email(content=content)
                                return
                            print('{} -- 未知异常造成点击【关注】按钮失败！ {}'.format(self.now(), e))
                        print('{} -- 已关注 {} 个用户'.format(self.now(), num_sub))
                        sleep_time = random.randint(0, frequency)
                        print('{} -- 随机休息 0-{}s，随机结果：{}s'.format(self.now(), frequency, sleep_time))
                        sleep(sleep_time)

                        # 当关注的人数达到配置的人数，停止脚本
                        if num_sub == int(target_num):
                            print('{} -- {} 已关注 {} 个用户，账号 {} 停止执行'.format(self.now(), user, num_sub, user))
                            content = '{} -- {} 已关注 {} 个用户，账号 {} 停止执行'.format(self.now(), user, num_sub, user)
                            subject = '脚本执行完成通知'
                            self.send_email(subject=subject, content=content)
                            # self.close_browser()
                            return
                if num_e == num_s:
                    print('{} -- 没有更多的粉丝，共加载 {} 个粉丝'.format(self.now(), num_e))
                    print('{} -- 切换到另一个目标用户'.format(self.now()))
                    break
                num_s = num_e

    def like_post(self):
        # 找到帖子的列表
        try:
            self.driver
        except RecursionError:
            print("{} -- 没有实例化的浏览器，请先点击“打开浏览器”按钮".format(self.now()))
            return

        if not self.is_element_exist('//div[@class="_9AhH0"]'):
            print('{} -- 当前页面没有帖子，定位到有帖子的页面后再点击“点赞按钮”'.format(self.now()))
            return

        # sum_s = 0
        # sum_e = 0
        # num = 0
        num_post = 0
        num_like = 0
        while True:
            ele_posts = self.driver.find_elements_by_class_name('_9AhH0')
            # sum_s = len(ele_posts)
            # 模拟鼠标按下空格键再松开
            action = ActionChains(self.driver)
            action.key_down(Keys.SPACE).perform()
            action.key_up(Keys.SPACE).perform()
            print('{} -- 加载下一页帖子。。。'.format(self.now()))
            for ele_post in ele_posts:
                num_post += 1
                # ele_post.location_once_scrolled_into_view
                # sleep(1)
                self.driver.execute_script("arguments[0].scrollIntoView();", ele_post)
                # 打开帖子
                ele_post.click()
                print('{} -- 打开第 {} 个帖子'.format(self.now(), num_post))
                sleep(2)
                # 点赞按钮
                # path_but_like = '/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span/svg'
                path_but_like = '//div[@class="QBdPU "]'

                try:
                    but_like = self.driver.find_elements_by_xpath(path_but_like)[1]
                except NoSuchElementException:
                    print('{} -- 未能加载出帖子的内容，没有定位到点赞按钮'.format(self.now()))
                else:
                    if ('"赞"' or 'Like') in but_like.get_attribute('innerHTML'):
                        num_like += 1
                        but_like.click()
                        print('{} -- 第 {} 次点赞'.format(self.now(), num_like))
                # 关闭帖子
                path_but_close = '/html/body/div[5]/div[3]/button'
                self.driver.find_element_by_xpath(path_but_close).click()
                print('{} -- 关闭第 {} 个帖子'.format(self.now(), num_post))


if __name__ == '__main__':
    # 加载配置文件
    conf_file = r"./config.json"
    with open(conf_file, "r") as f:
        conf = json.load(f)
    # 获取配置文件中的用户信息
    users = conf['users']

    # 点击关注按钮的间隔
    frequency = int(conf['frequency'])
    # 计划每个账号要关注的人数
    target_num = int(conf['target_num'])
    # Instagram网址
    instagram_url = 'https://www.instagram.com/'

    insta = App()
    insta.open_browser(instagram_url)

    for user in users:
        uname = user['uname']
        pwd = user['pwd']
        target_users = user['target_users']
        print('*'*6)
        print('当前时间为：{} ，开始操作账号： {}'.format(time.strftime("%H:%M:%S", time.localtime()), uname))
        try:
            insta.login_insta(uname, pwd)
        except Exception as e:
            print('{} -- 登录失败！跳过当前账号'.format(insta.now()))
        else:
            insta.subscribe_user(uname, pwd, target_users, frequency, target_num)
            insta.logout_insta()
        print('{} -- 账号 {} 操作完成'.format(insta.now(), uname))
        print('*'*6)
