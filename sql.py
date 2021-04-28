import configparser
import os

from peewee import *
conf = configparser.ConfigParser()  # 实例化ConfigParser对象
db = conf.read('config.ini',encoding='utf8')  # 读取配置文件
# 连接数据库
database = MySQLDatabase(
    conf.get('DATABASE', 'db'),
    user=conf.get('DATABASE', 'user'),
    host=conf.get('DATABASE', 'host'),
    password=conf.get('DATABASE', 'password'),
    port=int(conf.get('DATABASE', 'port')))


class UserInfo(Model):  # 定义UserInfo
    name = CharField()  # 用户名称
    birth = CharField()  # 生日
    sex = CharField()  # 性别
    email = CharField()    # 注册邮箱
    password = CharField()  # 注册密码
    y_email = CharField()  # 验证邮箱
    y_pwd = CharField()  # 验证密码
    google_code = CharField()  # 二重验证码
    userid = TextField()  # cookies
    status = CharField()  # 注册状态 0为未注册 1为注册成功

    class Meta:
        database = database
