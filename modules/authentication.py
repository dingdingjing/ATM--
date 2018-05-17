"""认证模块：主要进行了1、用户登录认证2、信用卡认证3、后台管理认证"""
import os
import json
import sys

# 程序主目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings

# 认证装饰器


def auth(auth_type):  # 定义认证类型函数，有三种类型：1、用户登录认证 2、信用卡认证 3、后台管理认证
    def outer_wrapper(func):
        if auth_type == 'user_auth':  # 认证类型为用户登录认证
            def inner():
                title = func()
                username = input('\033[34;1m请输入用户名：\033[0m')
                password = input('\033[34;1m请输入密码：\033[0m')
                if len(username.strip()) > 0:
                    with open(settings._db_users_dict, 'r', encoding='utf-8') as f_users_dict:
                        users_dict = json.load(f_users_dict)
                        if username in users_dict.keys():
                            if password == users_dict[username]['password']:
                                if users_dict[username]['locked'] == 0:
                                    print('\033[32;1m用户%s认证成功！\033[0m' % username)
                                    return title, username

                                else:
                                    print('\033[31;1m用户%s已经被锁定,认证失败！\033[0m' % username)
                            else:
                                print('\033[31;1m用户名或密码错误，认证失败！\033[0m')
                        else:
                            print('\033[31;1m输入的用户名%s不存在，认证失败！\033[0m' % username)
                else:
                    print('\033[31;1m您的输入为空，认证失败！\033[0m')
            return inner  # 当用户调用inner时，只会返回inner的内存地址，下次再调用时加上（）才会执行inner函数

        if auth_type == 'credit_auth':  # 认证类型为信用卡认证
            def inner():
                title = func()
                credit_card = input('\033[34;1m请输入信用卡卡号：\033[0m')
                password = input('\033[34;1m请输入信用卡密码：\033[0m')
                if len(credit_card.strip()) > 0:
                    with open(settings._db_credit_dict, 'r', encoding='utf-8') as f_credit_dict:
                        credit_dict = json.load(f_credit_dict)
                        if credit_card in credit_dict.keys():
                            if password == credit_dict[credit_card]['password']:
                                if credit_dict[credit_card]['locked'] == 0:
                                    print('\033[32;1m信用卡%s认证成功\033[0m' % credit_card)
                                    return title, credit_card
                                else:
                                    print('\033[31;1m信用卡%s已经被冻结，请联系银行，认证失败！\033[0m' % credit_card)
                            else:
                                print('\033[31;1m密码输入有误，认证失败！\033[0m')
                        else:
                            print('\033[31;1m您输入的信用卡卡号不存在，认证失败！\033[0m')
                else:
                    print('\033[31;1m您输入的信用卡卡号为空，认证失败！\033[0m')
            return inner

        if auth_type == 'admincenter_auth':  # 认证类型为管理员账户认证
            def inner():
                title = func()
                admincenter_dict = {'admin': 'admin1234'}
                adminname = input('\033[34;1m请输入管理员用户名：\033[0m')
                password = input('\033[34;1m请输入管理账户密码：\033[0m')
                if len(adminname.strip()) > 0:
                    if adminname in admincenter_dict.keys():
                        if password == admincenter_dict[adminname]:
                            print('\033[32;1m管理员%s身份认证成功！\033[0m' % adminname)
                            return title, adminname
                        else:
                            print('\033[31;1m用户名或密码错误，认证失败！\033[0m')
                    else:
                        print('\033[31;1m输入的用户名%s不存在，认证失败！\033[0m' % adminname)
                else:
                    print('\033[31;1m输入的用户名为空，认证失败！\033[0m')
            return inner
    return outer_wrapper


@auth('user_auth')
def user_auth():  # 用户登录认证
    print('\033[32;1m用户登录认证\033[0m'.center(45, '-'))
    return True
# user_auth()


@auth('credit_auth')
def credit_auth():  # 信用卡认证
    print('\033[32;1m信用卡登录认证\033[0m'.center(45, '-'))
    return True
# credit_auth()


@auth('admincenter_auth')
def admincenter_auth():  # 管理员登录认证
    print('\033[32;1m管理员登录认证\033[0m'.center(45, '-'))
    return True

# admincenter_auth()



