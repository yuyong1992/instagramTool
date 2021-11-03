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
# from selenium.webdriver.common.action_chains import ActionChains
# 引入键盘事件
# from selenium.webdriver.common.keys import Keys
import json
import smtplib
from email.mime.text import MIMEText


def now():
    """
    格式化输出当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def is_element_exist(driver, path):
    """
    判断当前页面是否存在指定xpath路径的元素
    最长等待20s，每0.5s检查一次，直到指定路径的元素在页面上可见，返回true，否则返回false
    参数：
    1. driver：object，浏览器实例
    2. path：str，元素的xpath路径
    """
    flag = True
    try:
        DW(driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH, path)))
        return flag
    except (TimeoutError, TimeoutException):
        print('{} -- {} -- 等待20s未找到该元素，path：{}'.format(now(), threading.currentThread().name, path))
        flag = False
        return flag
    except Exception as e:
        print('{} -- {} -- 定位元素时出现未知异常，path：{}; Err:{}'.format(now(), threading.currentThread().name, path, e))
        flag = False
        return flag


def login_email(host, port, sender, pwd):
    """
    登录邮箱，smtp协议
    传入参数：
    1. host：str，邮件服务器地址
    2. port：str，邮件服务器端口
    3. sender：str，要登陆的邮件地址
    4. pwd：str，要登陆的邮箱密码
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender, pwd)
    return server


def send_email(subject=r'Instagram脚本中止通知', content=r'Instagram 脚本已停止运行，详情请查看控制台运行日志。'):
    """
    登录邮箱后发送邮件
    参数：
    1. subject：str，邮件的主题
    2. content：str，邮件的正文内容
    本方法发送的邮件正文未富文本格式，如果需要发送HTML邮件可以再处理
    """
    # TODO: 将邮箱的配置抽离到配置文件中
    host = "smtp.partner.outlook.cn"
    port = "587"
    sender = "yong.yu@sinnet-cloud.cn"
    pwd = "sinnet@12345"

    recipient = ["1305703064@qq.com", "yong.yu@sinnet-cloud.cn"]
    # subject = subject
    # content = content

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ','.join(recipient)

    try:
        server = login_email(host, port, sender, pwd)
        print('{} -- {} -- 邮箱登录成功，用户名：{}'.format(now(), threading.currentThread().name, sender))
    except Exception as err:
        print('{} -- {} -- 邮箱登录失败。ERR：{}'.format(now(), threading.currentThread().name, err))
        return
    try:
        server.sendmail(sender, recipient, msg.as_string())
        print('{} -- {} -- 邮件发送成功'.format(now(), threading.currentThread().name))
    except Exception as err:
        print('{} -- {} -- 邮件发送失败。ERR：{}'.format(now(), threading.currentThread().name, err))
        return


def stop_load_page(driver):
    """
    执行js停止加载页面，特殊情况考虑，比如为了减少脚本执行时间，在检测到目标元素后，就停止加载页面。
    目前没有用到该方法
    参数：
    1. driver：object，浏览器实例
    """
    js_stop_load_page = r'window.stop()'
    driver.execute_script(js_stop_load_page)


def open_browser(url):
    """
    启动浏览器
    参数：
    1. url：str，要访问的页面URL
    这个项目里的url就是instagram网站了
    """
    instagram_url = url
    try:
        # 设置chrome浏览器的配置
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

        # 实例化一个chrome浏览器，并加载前面设置的配置
        driver = webdriver.Chrome(options=chrome_options)
        print("{} -- {} -- 打开浏览器".format(now(), threading.currentThread().name))
    except Exception as e:
        # 如果浏览器实例化失败，抛出异常
        print('{} -- {} -- 启动浏览器失败,ERR: {}'.format(now(), threading.currentThread().name, e))
        raise
    try:
        # 浏览器打开目标网址
        driver.get(instagram_url)
        print("{} -- {} -- 访问Instagram".format(now(), threading.currentThread().name))
        # 最大化浏览器界面
        driver.maximize_window()
        # print("浏览器全屏")
        # 设置全局等待时间20s
        driver.implicitly_wait(20)
        # 浏览器访问目标网址，进行下一步操作之前增加睡眠时间，增强脚本稳定性
        sleep(1)
        return driver
    except Exception as e:
        # 如果访问网址出现问题抛出异常
        print('{} -- {} -- 访问Instagram登录页面失败，ERR：{}'.format(now(), threading.currentThread().name, e))
        # close_browser(driver)
        raise


def close_browser(driver):
    """
    关闭浏览器
    调用webdriver的quit()方法，关闭浏览器
    参数：
    1. driver：object，浏览器实例
    """
    try:
        driver.quit()
    except RecursionError:
        print('{} -- {} -- 没有实例化的浏览器，无需关闭'.format(now(), threading.currentThread().name))
        raise
    except Exception as e:
        print('{} -- {} -- 未知异常，关闭浏览器实例失败 {}'.format(now(), threading.currentThread().name, e))
        raise


# @staticmethod
def end_script(driver):
    """
    结束脚本：关闭浏览器，结束脚本
    参数：
    1. driver：object，浏览器实例
    """
    # 关闭浏览器
    try:
        close_browser(driver)
        print('{} -- {} -- 浏览器已关闭'.format(now(), threading.currentThread().name))
    except RecursionError:
        print('{} -- {} -- 没有运行的浏览器实例，无需关闭'.format(now(), threading.currentThread().name))
    except Exception as e:
        print('{} -- {} -- 未知异常，退出浏览器实例失败  {}'.format(now(), threading.currentThread().name, e))
    # 退出脚本执行
    print('{} -- {} -- 结束脚本'.format(now(), threading.currentThread().name))
    sys.exit()


def login_insta(driver, username, password):
    """
    登录Instagram
    参数：
    1. driver：object，浏览器驱动
    2. username：str，用户名
    3. pwd：str，密码
    """
    print('{} -- {} -- 准备登录的用户：{}'.format(now(), threading.currentThread().name, username))
    try:
        driver.title
    except RecursionError:
        print('{} -- {} -- 浏览器实例未运行'.format(now(), threading.currentThread().name))
        raise
    except Exception as e:
        print('{} -- {} -- 未知异常，浏览器实例不能调用。ERR：{}'.format(now(), threading, e))
        raise

    # 登录页面上用户名、密码和登录按钮元素的xpath路径
    path_mail = '//*[@id="loginForm"]/div/div[1]/div/label/input'
    path_pwd = '//*[@id="loginForm"]/div/div[2]/div/label/input'
    path_login_but = '//*[@id="loginForm"]/div/div[3]/button'

    # 先在页面上定位用户名、密码输入框和登录按钮元素，如果找不到抛出异常，结束脚本
    try:
        DW(driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, path_mail)))
        ele_username = driver.find_element_by_xpath(path_mail)
        print('{} -- {} -- 已定位到用户名输入框'.format(now(), threading.currentThread().name))
        DW(driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, path_pwd)))
        ele_pwd = driver.find_element_by_xpath(path_pwd)
        print('{} -- {} -- 已定位到密码输入框'.format(now(), threading.currentThread().name))
        DW(driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, path_login_but)))
        ele_login_but = driver.find_element_by_xpath(path_login_but)
        print('{} -- {} -- 已定位到登录按钮'.format(now(), threading.currentThread().name))
    except NoSuchElementException as e:
        print('{} -- {} -- 登录页面元素定位失败。{}'.format(now(), threading.currentThread().name, e))
        close_browser(driver)
        raise
    except TimeoutException:
        print('{} -- {} -- 登录页面长时间未能定位到输入框或【登录】按钮'.format(now(), threading.currentThread().name))
        close_browser(driver)
        raise

    # 输入用户名、密码、点击登录按钮
    ele_username.clear()
    ele_username.send_keys(username)
    print('{} -- {} -- 输入用户名'.format(now(), threading.currentThread().name))

    ele_pwd.clear()
    ele_pwd.send_keys(password)
    print('{} -- {} -- 输入密码'.format(now(), threading.currentThread().name))

    ele_login_but.click()
    print('{} -- {} -- 点击登录按钮'.format(now(), threading.currentThread().name))

    # 登录之后会出现询问是否保存登录信息的页面
    # path_save_login = '//*[@id="react-root"]/div/div/section/main/div/div/div/section/div/button'
    path_save_login = '//button[@class="sqdOP  L3NKy   y3zKF     "]'
    # 处理询问是否保存登录信息的页面
    if is_element_exist(driver, path_save_login):
        DW(driver, 20, 0.5).until(EC.element_to_be_clickable((By.XPATH, path_save_login)))
        ele_save_login = driver.find_element_by_xpath(path_save_login)
        # 保存登录信息
        ele_save_login.click()
        print('{} -- {} -- 是否保存登录信息：是'.format(now(), threading.currentThread().name))

    # 个人中心头像的元素路径
    path_personal = '//img[@class="_6q-tv"]'
    # 如果头像元素存在则判断为登录成功，否则登录失败没有进入首页
    if is_element_exist(driver, path_personal):
        print('{} -- {} -- {} 已经登录成功'.format(now(), threading.currentThread().name, username))
    else:
        print('{} -- {} -- 未进入首页!未找到主页头像元素：{}'.format(now(), threading.currentThread().name, path_personal))
        return

    # 登录之后询问是否开启消息通知的窗口以及“下次再选”选项的的元素路径
    path_handle_notice = '//button[@class="aOOlW   HoLwm "]'
    sleep(2)
    if is_element_exist(driver, path_handle_notice):
        # DW(driver, 20, 0.5).until(EC.element_to_be_clickable((By.XPATH, path_handle_notice)))
        ele_handle_notice = driver.find_element_by_xpath(path_handle_notice)
        # 点击下次再选
        ele_handle_notice.click()
        print('{} -- {} -- 通知设置：下次再选'.format(now(), threading.currentThread().name))


def logout_insta(driver):
    """
    退出登录
    参数：
    1. driver：object，浏览器实例
    """
    # 回到主页
    driver.get(instagram_url)
    print('{} -- {} -- 回到主页'.format(now(), threading.currentThread().name))
    # 头像的元素路径
    path_avatar = r'//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img'
    try:
        DW(driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH, path_avatar)))
    except TimeoutError:
        print('{} -- {} -- 未找到个人中心头像元素，不需要执行退出登录'.format(now(), threading.currentThread().name))
        return
    except TimeoutException:
        print('{} -- {} -- 未找到个人中心头像元素，不需要执行退出登录'.format(now(), threading.currentThread().name))
        return
    except Exception as e:
        print('{} -- {} -- 未知错误，定位个人中心的头像元素时出错 {}'.format(now(), threading.currentThread().name, e))
        return
    # 点击头像，打开个人中心的操作菜单
    driver.find_elements_by_class_name('_6q-tv')[-1].click()
    print('{} -- {} -- 点击头像'.format(now(), threading.currentThread().name))
    # 退出按钮地址
    path_logout = r'//div[contains(text(), "退出")]'
    # 当退出按钮出现，点击退出按钮
    DW(driver, 20, 0.5).until(EC.visibility_of_any_elements_located((By.XPATH, path_logout)))
    ele_logout = driver.find_element_by_xpath(path_logout)
    ele_logout.click()
    print('{} -- {} -- 点击退出按钮'.format(now(), threading.currentThread().name))
    # 切换账号按钮
    path_switch = r'//button[contains(text(), "切换帐户") or contains(text(), "Switch Account")]'
    DW(driver, 20, 0.5).until(EC.element_to_be_clickable((By.XPATH, path_switch)))
    driver.find_element_by_xpath(path_switch).click()


def subscribe_user(url, user, pwd, target_users, frequency, target_num):
    """
    点击关注
    参数：
    1. url:str，Instagram网址
    2. user：str，登录的Instagram用户账号
    3. pwd：str，登录的Instagram用户密码
    4. target_users：str，用来找粉丝列表的大V账号，列表
    5. frequency：num，在关注列表中点击“关注”按钮的频率
    6. target_num：num，点击关注的个数
    注：
    1. 设置频率和个数，是为了防止被Instagram平台识别出来是机器操作，否则账号会被封，严重的情况下会被永久封号
    2. target_num只是点击关注的个数，并不是最终关注的人数，一些账号会设置关注的权限，需要对方同意才能关注成功
    """

    # 启动浏览器访问Instagram
    try:
        driver = open_browser(url)
    except Exception as e:
        print('{} -- {} -- 启动浏览器失败，退出脚本.ERR: {}'.format(now(), threading.currentThread().name, e))
        content = '{} -- {} -- 启动浏览器失败，退出脚本.ERR：{}'.format(now(), threading.currentThread().name, e)
        send_email(content=content)
        return
    # 登录Instagram
    try:
        login_insta(driver, user, pwd)
    except Exception as e:
        print('{} -- {} -- 登录失败，退出脚本.ERR：{}'.format(now(),
                                                    threading.currentThread().name, e))
        content = '{} -- {} -- 登录失败，退出脚本.ERR：{}'.format(
            now(), threading.currentThread().name, e)
        send_email(content=content)
        close_browser(driver)
        return
    # 本次已经点击关注的个数
    num_sub = 0
    # 循环访问目标大V账号的主页
    for target_user in target_users:
        print('{} -- {} -- 目标用户的用户名{}'.format(now(), threading.currentThread().name, target_user))
        try:
            driver
        except RecursionError:
            print("{} -- {} -- 没有实例化的浏览器".format(now(), threading.currentThread().name))
            login_insta(driver, user, pwd)

        # 跳转到目标用户的主页，主页地址为：Instagram网站地址 + 目标用户的用户名
        target_url = '{}{}/'.format(instagram_url, target_user)
        driver.get(target_url)
        print('{} -- {} -- 跳转到目标用户的主页{}'.format(now(), threading.currentThread().name, target_url))

        # 粉丝列表按钮的元素地址
        path_fans_list = '//a[@class="-nal3 "]'

        # 点击目标用户主页上的粉丝列表，如果失败重试2次
        for i in range(3):
            try:
                print('{} -- {} -- 等待粉丝列表按钮出现'.format(now(), threading.currentThread().name))
                DW(driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, path_fans_list)))
                print('{} -- {} -- 粉丝列表按钮出现'.format(now(), threading.currentThread().name))
                break
            except (TimeoutError, TimeoutException):
                print('{} -- {} -- Timeout! 未找到粉丝列表'.format(now(), threading.currentThread().name))
                print('{} -- {} -- 判断当前页面是否为目标用户主页'.format(now(), threading.currentThread().name))
                if driver.current_url != target_url:
                    print('{} -- {} -- 当前页面的url: {}'.format(now(), threading.currentThread().name, driver.current_url))
                    print('{} -- {} -- 当前页面不是目标用户的主页'.format(now(), threading.currentThread().name))
                    print('{} -- {} -- 重新跳转到目标用户主页'.format(now(), threading.currentThread().name))
                    driver.get(target_url)
            if i == 2:
                print('{} -- {} -- 第3次加载目标用户主页，没有找到粉丝列表按钮'.format(now(), threading.currentThread().name))
                print('{} -- {} -- 结束当前账号 {} 执行'.format(now(),
                                                        threading.currentThread().name, user))
                # 邮件通知
                content = '{} -- {} -- 结束当前账号 {} 执行'.format(now(), threading.currentThread().name, user)
                send_email(content=content)
                close_browser(driver)
                return

        # 粉丝列表的窗口标题 元素地址
        path_fans_list_title = '//div[@class="m82CD  "]'
        try:
            print('{} -- {} -- 点击粉丝列表按钮'.format(now(), threading.currentThread().name))
            ele_fans_list = driver.find_element_by_xpath(path_fans_list)
            ele_fans_list.click()
        except ElementClickInterceptedException:
            if is_element_exist(driver, path_fans_list_title):
                print('{} -- {} -- 粉丝列表已打开'.format(now(), threading.currentThread().name))
            else:
                print('{} -- {} -- 当前页面未找到粉丝列表按钮，结束当前账号 {} 执行'.format(now(), threading.currentThread().name, user))
                # 邮件通知
                content = '{} -- {} -- 当前页面未找到粉丝列表按钮，结束当前账号 {} 执行'.format(now(), threading.currentThread().name, user)
                send_email(content=content)
                close_browser(driver)
                return
        except NoSuchElementException:
            print('{} -- {} -- 未知异常导致粉丝列表按钮丢失，结束当前账号 {} 执行'.format(now(), threading.currentThread().name, user))
            # 邮件通知
            content = '{} -- {} -- 未知异常导致粉丝列表按钮丢失，结束当前账号 {} 执行'.format(now(), threading.currentThread().name, user)
            send_email(content=content)
            close_browser(driver)
            return

        # 关注按钮元素路径
        path_but_subscribe = "//button[contains(@class, 'sqdOP') and contains(@class, 'L3NKy')]"
        # 判断元素列表中有没有“关注”按钮
        try:
            DW(driver, 5, 0.5).until(EC.presence_of_element_located((By.XPATH, path_but_subscribe)))
        except (TimeoutError, TimeoutException):
            print('{} -- {} -- 粉丝列表中没有【关注】按钮'.format(now(), threading.currentThread().name))
            print('{} -- {} -- 切换到另一个目标用户查找粉丝'.format(now(), threading.currentThread().name))
            continue

        num_s = 0
        num_e = 0

        # 下拉加载粉丝列表，直到点击“关注”按钮的次数达到配置的值
        while True:
            # 下拉加载粉丝列表
            for i in range(3):
                try:
                    # div的滚动条操作
                    sleep(2)
                    div_scroll_top(driver, 100)
                    print('{} -- {} -- 加载粉丝列表下一页数据。。。'.format(now(),
                                                              threading.currentThread().name))
                except Exception as e:
                    print(
                        '{} -- {} -- 加载下一页数据异常，退出当前账号 {} 的执行！{}'.format(now(), threading.currentThread().name, user, e))
                    # 邮件通知
                    content = '{} -- {} -- 加载下一页数据异常，退出当前账号 {} 的执行！{}'.format(now(), threading.currentThread().name,
                                                                              user, e)
                    send_email(content=content)
                    close_browser(driver)
                    return
                # loading图标
                path_loading = r'//svg[@class="  By4nA"]'
                for j in range(3):
                    try:
                        DW(driver, 10, 0.5).until_not(
                            EC.presence_of_element_located((By.XPATH, path_loading)))
                        print('{} -- {} -- 等待加载完成、loading消失'.format(now(),
                                                                    threading.currentThread().name))
                        break
                    except (TimeoutError, TimeoutException):
                        print('{} -- {} -- 等待了10s仍在加载中，再等10s'.format(now(),
                                                                     threading.currentThread().name))
                    if j == 2:
                        print('{} -- {} -- 等待了30s仍在加载中'.format(now(),
                                                               threading.currentThread().name))
                        print('{} -- {} -- 粉丝列表加载异常，退出当前账号 {} 的执行'.format(now(),
                                                                          threading.currentThread().name, user))
                        # 邮件通知
                        content = '{} -- {} -- 粉丝列表加载异常，退出当前账号 {} 的执行'.format(now(), threading.currentThread().name,
                                                                              user)
                        send_email(content=content)
                        close_browser(driver)
                        return
                # 所有的关注按钮
                eles_but_subscribe = driver.find_elements_by_xpath(
                    path_but_subscribe)
                num_e = len(eles_but_subscribe)
                print('{} -- {} -- 当前粉丝列表中粉丝数量：{}'.format(now(),
                                                          threading.currentThread().name, num_e))
                if num_e != num_s:
                    print('{} -- {} -- 加载完成'.format(now(),
                                                    threading.currentThread().name))
                    break
                if i == 2:
                    print('{} -- {} -- 第3次尝试，加载后粉丝数没有增加'.format(now(),
                                                                threading.currentThread().name))
                    break
                print('{} -- {} -- 加载后粉丝数与加载前粉丝数目相同，再尝试加载一次'.format(now(),
                                                                    threading.currentThread().name))
                sleep(1)
            eles_but_subscribe = driver.find_elements_by_xpath(
                path_but_subscribe)
            for ele_like_but in eles_but_subscribe:
                if ele_like_but.text == '关注' or ele_like_but.text == 'Follow':
                    num_sub += 1
                    if not ele_like_but.is_displayed():
                        # ele_like_but.location_once_scrolled_into_view
                        print('{} -- {} -- 把第 {} 个【关注】按钮移动到可见位置'.format(now(),
                                                                        threading.currentThread().name, num_sub))
                        driver.execute_script(
                            "arguments[0].scrollIntoView();", ele_like_but)
                    try:
                        ele_like_but.click()
                    except Exception as e:
                        path_err = "/html/body/div[6]/div/div/div/div[1]/h3"
                        if is_element_exist(driver, path_err):
                            print('{} -- {} -- 关注第 {} 个用户时，账号 {} 被限制，退出当前账号执行! {}'.format(now(),
                                                                                          threading.currentThread().name,
                                                                                          num_sub, user, e))
                            # 邮件通知
                            content = '{} -- {} -- 关注第 {} 个用户时，账号 {} 被限制，退出当前账号执行! {}'.format(now(),
                                                                                              threading.currentThread().name,
                                                                                              num_sub, user, e)
                            send_email(content=content)
                            close_browser(driver)
                            return
                        print('{} -- {} -- 未知异常造成点击【关注】按钮失败！ {}'.format(now(),
                                                                        threading.currentThread().name, e))
                    print('{} -- {} -- 已关注 {} 个用户'.format(now(),
                                                          threading.currentThread().name, num_sub))
                    sleep_time = random.randint(0, frequency)
                    print('{} -- {} -- 随机休息 0-{}s，随机结果：{}s'.format(now(), threading.currentThread().name, frequency,
                                                                   sleep_time))
                    sleep(sleep_time)

                    # 当关注的人数达到配置的人数，停止脚本
                    if num_sub == int(target_num):
                        print('{} -- {} -- {} 已关注 {} 个用户，账号 {} 停止执行'.format(now(), threading.currentThread().name, user,
                                                                            num_sub, user))
                        content = '{} -- {} -- {} 已关注 {} 个用户，账号 {} 停止执行'.format(now(), threading.currentThread().name,
                                                                                user, num_sub, user)
                        subject = '脚本执行完成通知'
                        send_email(subject=subject, content=content)
                        close_browser(driver)
                        return
            if num_e == num_s:
                print('{} -- {} -- 没有更多的粉丝，共加载 {} 个粉丝'.format(now(),
                                                              threading.currentThread().name, num_e))
                print('{} -- {} -- 切换到另一个目标用户'.format(now(),
                                                      threading.currentThread().name))
                break
            num_s = num_e
    # 关闭浏览器
    close_browser(driver)


def div_scroll_top(driver, height):
    """
    窗口的滚动条操作
    参数：
    1. driver：object，浏览器实例
    2. height：num，滚动的高度
    """
    # 操作滚动条的js命令
    js = "document.getElementsByClassName('isgrP')[0].scrollTop=document.getElementsByClassName('isgrP')[0].scrollHeight+{};".format(
        height)
    try:
        # 执行js命令
        driver.execute_script(js)
        print('{} -- {} -- 滚动条向下滚动 {} 高度'.format(now(), threading.currentThread().name, height))
    except Exception as e:
        print('{} -- {} -- 执行js脚本出错。 \n js:【{}】 \n ERR:{}'.format(now(), threading.currentThread().name, js, e))
        raise


def ele_scroll_to_view(driver, ele):
    """
    操作元素到页面可视区域
    参数：
    1. driver：object，浏览器实例
    2. ele：object，要操作的元素对象
    """
    # 进行操作的js脚本
    js = "arguments[0].scrollIntoView();"
    # 执行js脚本
    try:
        driver.execute_script(json, ele)
        print('{} -- {} -- 把元素移动到可见位置'.format(now(), threading.currentThread().name))
    except Exception as e:
        print('{} -- {} -- 执行js脚本出错。 \n js:【{}】 \n ERR:{}'.format(now(), threading.currentThread().name, js, e))
        raise


def unsubscribe(uname, pwd):
    """
    取消关注
    参数：
    1. uname：str，要登录的账号用户名
    2. pwd：str，要登录的账号密码
    操作：
    1. 登录账号
    2. 进入主页
    3. 打开关注列表
    4. 点击列表中的“取消关注”按钮
    """

    # 登录Instagram
    instagram_url = 'https://instagram.com'
    url = 'https://instagram.com/{}'.format(uname)
    driver = open_browser(instagram_url)
    login_insta(driver, uname, pwd)
    driver.get(url)
    # 关注人数元素
    DW(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'g47SY ')))
    ele_following_number = driver.find_elements_by_class_name('g47SY ')[2]
    # 如果关注数字是“NaN”则用户目前没有关注任何人
    if ele_following_number.text == 'NaN':
        print('{} -- {} -- 当前账号 {} 的following列表没有正在关注的人，退出脚本'.format(now(), threading.currentThread().name, uname))
        content = '{} -- {} -- 当前账号 {} 的following列表没有正在关注的人，退出脚本'.format(now(), threading.currentThread().name, uname)
        send_email(content=content)
        close_browser(driver)
        return
    print('{} -- {} -- 当前账号 {} following列表中有 {} 个人'.format(now(), threading.currentThread().name, uname,
                                                           ele_following_number.text))
    # 点击关注数字，打开关注列表
    ele_following_number.click()
    DW(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'm82CD')))
    print('{} -- {} -- 已经打开following列表'.format(now(), threading.currentThread().name))
    # 滚动加载关注列表，直到所有关注的人都被取消关注
    while True:
        try:
            # div的滚动条操作
            div_scroll_top(driver, 100)
            print('{} -- {} -- 加载列表下一页数据。。。'.format(now(), threading.currentThread().name))
        except Exception as e:
            print(
                '{} -- {} --  操作列表滚动条异常，退出当前账号 {} 的执行！{}'.format(now(), threading.currentThread().name, user, e))
            # 邮件通知
            content = '{} -- {} -- 操作列表滚动条异常，退出当前账号 {} 的执行！{}'.format(now(), threading.currentThread().name, user, e)
            send_email(content=content)
            close_browser(driver)
            return
        try:
            # 数据加载的loading元素
            DW(driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, '  By4nA')))
        except (TimeoutException, TimeoutError) as e:
            print('{} -- {} -- 加载列表下一页超时！等待20s，加载的loading还未消失。退出脚本'.format(now(), threading.currentThread().name))
            # 邮件通知
            content = '{} -- {} -- 操作列表滚动条异常，退出当前账号 {} 的执行！{}'.format(now(), threading.currentThread().name, user, e)
            send_email(content=content)
            close_browser(driver)
            return
        # “已关注”按钮元素
        path_but_following = '//button[text()="已关注" or text()="Following"]'
        DW(driver, 20).until(EC.presence_of_element_located((By.XPATH, path_but_following)))
        ele_but_following = driver.find_elements_by_xpath(path_but_following)
        number_but_following = len(ele_but_following)
        # 如果“已关注”按钮的数量为0，结束脚本
        if number_but_following == 0:
            print('{} -- {} -- 当前账号 {} following列表中没有正在关注的人，退出脚本'.format(now(), threading.currentThread().name, uname))
            content = '{} -- {} -- 当前账号 {} 的following列表中没有正在关注的人，退出脚本'.format(now(), threading.currentThread().name,
                                                                              uname)
            send_email(content=content)
            close_browser(driver)
            return
        # 点击每一个已经加载出来的“已关注”按钮
        for i in range(number_but_following):
            DW(driver, 20).until(EC.presence_of_element_located((By.XPATH, path_but_following)))
            ele_but_following = driver.find_elements_by_xpath(path_but_following)
            but_following = ele_but_following[0]
            if not but_following.is_displayed():
                ele_scroll_to_view(driver, but_following)
            but_following.click()
            print('{} -- {} -- 点击【已关注】按钮'.format(now(), threading.currentThread().name))
            # DW(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'aOOlW -Cab_   ')))
            # 确认停止关注的提示框
            path_confirm_unsubscribe = '//button[text()="停止关注" or text()="Unfollow"]'
            DW(driver, 20).until(EC.element_to_be_clickable((By.XPATH, path_confirm_unsubscribe)))
            ele_confirm_unsubscribe = driver.find_element_by_xpath(path_confirm_unsubscribe)
            ele_confirm_unsubscribe.click()
            print('{} -- {} -- 点击【停止关注】按钮'.format(now(), threading.currentThread().name))
            sleep_time = random.randint(3, 10)
            sleep(sleep_time)
            print('{} -- {} -- 随机休息 {} s'.format(now(), threading.currentThread().name, sleep_time))


def like_and_comment_label_post(url, user, pwd, comments):
    """
    从发现页面，给帖子点赞和评论
    参数：
    1. url：str，Instagram网址
    2. user：str，要登录的账号用户名
    3. pwd：str，要登陆账号密码
    4. comment：list，要评论的标签和评论的内容，不同的标签对应不同的评论内容
    """

    # 启动浏览器访问Instagram
    try:
        driver = open_browser(url)
    except Exception as e:
        print('{} -- {} -- 启动浏览器失败，退出脚本.ERR: {}'.format(now(), threading.currentThread().name, e))
        content = '{} -- {} -- 启动浏览器失败，退出脚本.ERR：{}'.format(now(), threading.currentThread().name, e)
        send_email(content=content)
        return
    # 登录Instagram
    try:
        login_insta(driver, user, pwd)
    except Exception as e:
        print('{} -- {} -- 登录失败，退出脚本.ERR：{}'.format(now(), threading.currentThread().name, e))
        content = '{} -- {} -- 登录失败，退出脚本.ERR：{}'.format(now(), threading.currentThread().name, e)
        send_email(content=content)
        return

    while True:
        for comment in comments:
            label = comment['label']
            comment_link = comment['comment']
            # 跳转到话题标签页面
            label_page = 'https://www.instagram.com/explore/tags/{}/'.format(
                label)
            driver.get(label_page)
            print('{} -- {} -- 跳转到话题标签 {} 的页面'.format(now(),
                                                      threading.currentThread().name, label))
            # 打开当前页面上第一条帖子
            DW(driver, 20).until(
                EC.visibility_of_any_elements_located((By.CLASS_NAME, '_9AhH0')))
            ele_posts = driver.find_elements_by_class_name('_9AhH0')
            n = 0
            for ele_post in ele_posts:

                print('{} -- {} -- 打开当前页第 {} 个帖子'.format(now(), threading.currentThread().name, n))
                ele_post.click()
                # 点赞按钮
                path_but_like = r'//div[@class="QBdPU "]/span/*[name()="svg"]'
                # DW(driver, 20).until(EC.presence_of_element_located((By.XPATH, path_but_like)))
                ele_but_like = driver.find_element_by_xpath(path_but_like)
                # 评论框
                path_comment_box = r'//form[@class="X7cDz"]/textarea'
                path_submit_comment = r'//form[@class="X7cDz"]/button[@type="submit"]'
                sleep(1)
                # 获取点赞按钮的‘aria-label’属性，用以判断是否已经点过赞
                is_liked = ele_but_like.get_attribute('aria-label')
                # 如果‘aria-label’属性的值是‘赞’或者‘Like'，则表示没有点过赞，执行带点赞和评论的操作
                if is_liked in ['赞', 'Like']:
                    # 点赞
                    ele_but_like.click()
                    sleep(1)
                    print('{} -- {} -- 给新帖子点赞'.format(now(), threading.currentThread().name))
                    try:
                        # 评论框元素
                        ele_comment_box = driver.find_element_by_xpath(path_comment_box)
                        # 激活评论框
                        ele_comment_box.click()
                        # 评论框激活后的输入框
                        ele_new_comment_box = driver.find_element_by_xpath(path_comment_box)
                        ele_new_comment_box.clear()
                        # 要输入的评论，指引到自己的账号
                        comment = 'It is great! There are also something amazing here: @{}'.format(comment_link)
                        ele_new_comment_box.send_keys(comment)
                        print('{} -- {} -- 给新帖子评论 {}'.format(now(), threading.currentThread().name, comment))
                        # 点击提交
                        ele_submit_comment = driver.find_element_by_xpath(path_submit_comment)
                        ele_submit_comment.click()
                    except NoSuchElementException:
                        print('{} -- {} -- 该帖子未开放评论'.format(now(), threading.currentThread().name))
                # 关闭帖子
                path_but_close_post = r'//*[name()="svg"][contains(@aria-label,"关闭") or contains(@aria-label,"Close")]'
                ele_but_close_post = driver.find_element_by_xpath(path_but_close_post)
                ele_but_close_post.click()
                print('{} -- {} -- 关闭帖子'.format(now(), threading.currentThread().name))
                n += 1
                sleep(2)
                # 刷新当前页面以获取新帖子
                # driver.refresh()


if __name__ == '__main__':
    # 加载配置文件
    conf_file = r"./config.json"
    with open(conf_file, "r") as f:
        conf = json.load(f)
    # 获取配置文件中的用户信息
    users = conf['users']
    # 用来评论的用户
    comment_user = conf['comments']['uname']
    comment_user_pwd = conf['comments']['pwd']
    # 评论的标签
    comments = conf['comments']['comments']

    # 点击关注按钮的间隔
    frequency = int(conf['frequency'])
    # 计划每个账号要关注的人数
    target_num = int(conf['target_num'])
    # Instagram网址
    instagram_url = 'https://www.instagram.com/'

    # 多线程，有多个用户的时候并行执行关注的操作
    threads = []
    for user in users:
        uname = user['uname']
        pwd = user['pwd']
        target_users = user['target_users']
        print('*' * 6)
        print('当前时间为：{} ，开始操作账号： {}'.format(time.strftime("%H:%M:%S", time.localtime()), uname))
        # subscribe_user(instagram_url, uname, pwd, target_users, frequency, target_num)
        t = threading.Thread(target=subscribe_user, name=uname,
                             args=(instagram_url, uname, pwd, target_users, frequency, target_num))
        threads.append(t)
        t.start()
        print('{} -- {} -- 账号 {} 操作完成'.format(now(), threading.currentThread().name, uname))
        print('*' * 6)

    # 多线程，点赞评论的方法与关注的方法并行执行
    t_comment = threading.Thread(target=like_and_comment_label_post, name=comment_user,
                                 args=(instagram_url, comment_user, comment_user_pwd, comments))
    t_comment.start()
    for t in threads:
        t.join()
    t_comment.join()
