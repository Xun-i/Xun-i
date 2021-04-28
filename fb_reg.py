
# 使用user-agent模拟浏览器注册Facebook
# 以下均可查看真实IP
# driver.get('http://httpbin.org/ip')
# driver.get('http://lumtest.com/myip.json')

import random, string, names, time, os, json, getcode
from poplib import error_proto
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from sql import UserInfo

url = 'https://m.facebook.com/campaign/landing.php'  # 访问注册地址

# 模拟user-agent列表
USER_AGENT = [
    "Mozilla/5.0 (Android 9.0; Mobile; rv:63.0) Gecko/63.0 Firefox/63.0",
    "Mozilla/5.0 (Linux; Android 9.0; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU OS 10_14 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Mobile/14E304 Safari/605.1.15",
    "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_HK",
    "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5s Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.2.2"
]
proxy = ''  # 初始化代理ip
code = ''  # 初始化确认码
def init(user_num:int):   # 生成注册信息
    UserInfo.drop_table()
    UserInfo.create_table()
    while True:
        if len(UserInfo.select()) == user_num:  # 判断数据库数量
            break
        name = names.get_full_name()  # 使用names模块生成随机英文名
        birth = str(random.randint(1975,1995)) + '-' + str(random.randint(1,12) )+ '-' + str(random.randint(1,28))  # 生成随机生日
        sex = random.choice(["女", "男"])  # 随机生成性别
        email = name.replace(" ","").lower() + random.choice(["@gmail.com", "@yahoo.com", "@outlook.com"])  # 随机生成邮箱号码
        pwd = ''.join(random.sample(string.ascii_letters + string.digits, 9))  # 随机生成9位密码
        if UserInfo.filter(email=email, password=pwd):  # 检索数据中释放存在
            continue
        else:
            UserInfo(name=name, birth=birth, sex=sex, email=email, password=pwd, status=0).save()  # 将生成数据保存至数据库


def update(o_email,y_email, y_pwd, browser):
    while True:
        new_name = names.get_full_name()
        new_email = new_name.replace(" ", "").lower() + random.choice(["@gmail.com", "@yahoo.com", "@outlook.com"])  # 生成邮箱号码
        if UserInfo.filter(email=new_email, name=new_name):
            continue
        else:
            UserInfo.update({UserInfo.email: new_email, UserInfo.name: new_name}).where(  # 修改对应邮箱账号和姓名
                UserInfo.email == o_email).execute()
            browser.delete_all_cookies()
            browser.quit()
            return register(y_email, y_pwd)  # 重启注册程序


def register(y_email, y_pwd):
    global proxy  # 导入全局代理变量
    global code  # 导入全局确认码变量
    options = webdriver.ChromeOptions()  # 实例化谷歌浏览器对象
    if proxy is None:  # 判断IP是否被禁
        proxy = "192.168.61.154:{}".format(random.randint(10011, 10020))  # 随机获取一个IP地址
        # proxy = "172.16.5.15:{}".format(random.randint(6001, 6100))
        print("proxy server：", proxy)
        options.add_argument('–-proxy-server=http://' + proxy)  # 添加代理ip
    options.add_argument('user-agent="{}"'.format(random.choice(USER_AGENT)))  # 添加随机模拟user-agent
    browser = webdriver.Chrome(options=options)  # 将请求头加入浏览器中
    browser.get(url)  # 打开指定视图
    user = UserInfo.select().where(UserInfo.status=="0").get()  # 获取表中未注册都条记录
    firstname = user.name.split(" ")[0]  # 获取名
    lastname = user.name.split(" ")[1]  # 获取姓
    day = user.birth.split("-")[2]  # 获取日
    month = user.birth.split("-")[1]  # 获取月
    year = user.birth.split("-")[0]  # 获取年
    sex = 0 if user.sex == '女' else 1  # 获取性别
    email = user.email  # 获取邮箱
    pwd = user.password  # 获取密码
    sleep(2)
    browser.find_element_by_css_selector("[name='lastname']").send_keys(lastname)  # 将名字及姓氏键入输入框中
    sleep(2)
    browser.find_element_by_css_selector("[name='firstname']").send_keys(firstname)
    sleep(2)
    browser.find_element_by_css_selector("[name='lastname']").send_keys(Keys.ENTER)
    sleep(2)
    Select(browser.find_element_by_css_selector("[name='birthday_day']")).select_by_value(day)
    Select(browser.find_element_by_css_selector("[name='birthday_month']")).select_by_value(month)
    Select(browser.find_element_by_css_selector("[name='birthday_year']")).select_by_value(year)  # 生成随机的年月日并选中
    sleep(2)
    browser.find_element_by_css_selector('[type="submit"]').click()  # 下一步
    sleep(2)
    browser.find_element_by_css_selector('[data-sigil="switch_phone_to_email"]').click()  # 使用邮箱注册
    sleep(2)
    browser.find_element_by_css_selector("[name='reg_email__']").send_keys(email)  # 键入虚拟邮箱
    sleep(2)
    browser.find_element_by_css_selector('[type="submit"]').click()  # 下一步
    sleep(2)
    browser.find_elements_by_css_selector("[name='sex']")[sex].click()  # 随机选中男女之一
    sleep(2)
    browser.find_element_by_css_selector('[type="submit"]').click()  # 下一步
    sleep(2)
    browser.find_element_by_css_selector("[name='reg_passwd__']").send_keys(pwd)  # 键入登录密码
    sleep(2)
    browser.find_elements_by_css_selector('[type="submit"]')[3].click()  # 提交注册
    sleep(20)
    try:
        browser.find_element_by_css_selector('span.mfsm')  # 注册错误提示
        try:
            browser.find_element_by_css_selector('button[type="button"]')
            print("*error 该邮箱账号已存在，需要更改注册信息重新注册！")
            update(o_email=email, y_email=y_email, y_pwd=y_pwd, browser=browser)  # 进行更改注册信息
        except NoSuchElementException:
            proxy = None  # 设置为NOne 更换代理
            print("*error 当前ip禁止访问！")
            browser.delete_all_cookies()  # 清理缓存
            browser.quit()  # 关闭视窗
            return register(y_email, y_pwd)
    except NoSuchElementException:
        pass
    if proxy is not None:
        try:
            browser.find_element_by_css_selector("[type='email']").send_keys(y_email)
        except NoSuchElementException:
            browser.get_screenshot_as_file(os.path.join('error', str(time.time()) + '.png'))
        sleep(2)
        try:
            browser.find_elements_by_css_selector("[type='submit']")[0].click()  # 确定按钮
            sleep(2)
            browser.find_element_by_xpath('.//div[@id="rootcontainer"]/div/div/div/div/div/div/a').click()  # 没有收到确认码
            sleep(2)
            browser.find_elements_by_css_selector("[sigil='no_mpc']")[1].click()  # 添加另一个邮箱
            sleep(2)
            browser.find_element_by_css_selector("[type='email']").send_keys(y_email)  # 键入绑定邮箱
            sleep(2)
            browser.find_element_by_css_selector("[type='email']").send_keys(Keys.ENTER)
            sleep(2)
            code = None
            try:
                code = getcode.main(email=y_email, password=y_pwd, pop3_server="pop3.live.com")
                if code is not None:
                    browser.find_element_by_css_selector("[type='text']").send_keys(code)  # 键入绑定邮箱
                    time.sleep(2)
                    browser.find_element_by_css_selector("[type='text']").send_keys(Keys.ENTER)
                    time.sleep(2)
                    cookie = json.dumps(browser.get_cookies())
                    UserInfo.update({UserInfo.userid: cookie, UserInfo.status: "1",UserInfo.y_email: y_email, UserInfo.y_pwd: y_pwd}).where(
                        UserInfo.email == email).execute()  # 将注册成功邮箱更新
            except (error_proto, UnicodeDecodeError):
                print(y_email + '获取确认码失败,帐户已锁定')
            finally:
                browser.delete_all_cookies()
                browser.quit()
        except (NoSuchElementException,ElementNotInteractableException):
            browser.get_screenshot_as_file(os.path.join('../test/error', str(time.time()) + '.png'))
            print("*error 当前账号可能已经停用或邮箱无效等问题需要更改注册信息重新注册！")
            update(o_email=email, y_email=y_email, y_pwd=y_pwd, browser=browser)


if __name__ == '__main__':  # 测试
    # init(13)  # 初始化注册用户信息个数
    with open(os.path.join('error.txt'), 'r') as fr:  # 读取文件中验证邮箱密码进入注册
        while True:
            userinfo = fr.readline()
            if userinfo != '':
                email = userinfo.split('----')[0]
                password = userinfo.split('----')[1].strip('\n')
                register(y_email=email, y_pwd=password)
            else:
                break


