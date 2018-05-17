"""管理模块，包括：1.创建用户 2.信用卡发放 3.用户锁定 4.用户解锁 5.信用卡冻结 6.信用卡解冻 7.信用卡额度调整"""
import os
import json
import sys
import logging

# 程序主目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings
from modules import errorlog


def user_create(address='None', locked=0, creditcard=0):  # 创建用户
    while True:
        print('开始创建用户'.center(50, '-'))
        with open(settings._db_users_dict, 'r+')as f_user_dict:
            users_dict = json.load(f_user_dict)
            for key in users_dict:
                print('系统已有用户【%s】' % key)
            if_creat = input('\033[34;1m是否要创建新用户 确定【Y】/返回【B】:\033[0m').strip().lower()
            if if_creat == 'y':
                username = input('\033[34;1m请输入要添加的账户的用户名：\033[0m')
                password = input('\033[34;1m请输入要添加的账户的密码：\033[0m')
                if username not in users_dict.keys():
                    if len(username.strip()) > 0:
                        if len(password.strip()) > 0:
                            users_dict[username] = {"username": username, "password": password, "creditcard": creditcard
                                                    , "address": address, "locked": locked}
                            dict = json.dumps(users_dict)
                            f_user_dict.seek(0)
                            f_user_dict.truncate(0)
                            f_user_dict.write(dict)
                            print('\033[32;1m创建用户%s成功！\033[0m' % username)
                        else:
                            print('\033[31;1m密码输入为空，请重新输入！\033[0m')
                    else:
                        print('\033[31;1m用户名输入格式有误，请重新输入！\033[0m')
                else:
                    print('\033[31;1m用户%s已经存在！\033[0m')
            elif if_creat == 'b':
                break
            else:
                errorlog.log('error', logging.INFO)
                # print('\033[31;1m输入有误，没有该选项！\033[0m')
# user_create()


def creditcard_create(limit=15000, locked=0):  # 信用卡发放模块
    while True:
        print('进行信用卡发放'.center(50, '-'))
        with open(settings._db_credit_dict, 'r+') as f_credit_dict:
            credit_dict = json.load(f_credit_dict)
            for key in credit_dict:
                print("系统已有信用卡【%s】 \t 持卡人【%s】" % (key, credit_dict[key]['personinfo']))
            if_credit = input('\033[34;1m是否发放新的信用卡 确定【Y】/返回【B】:\033[0m').strip().lower()
            if if_credit == 'y':
                credit_card = input('\033[34;1m请输入将要发放的信用卡的卡号（6位数字）:\033[0m').strip()
                if credit_card not in credit_dict.keys():
                    if credit_card.isdigit() and len(credit_card) == 6:
                        password = input('\033[34;1m请为要发放的信用卡账号设置密码：\033[0m')
                        if len(password.strip())>0:
                            personinfo = input('\033[34;1m请输入要发放的信用卡申请人的名字：\033[0m')
                            if len(personinfo.strip()) > 0:
                                credit_dict[credit_card] = {"personinfo": personinfo, "password": password, 'limit':
                                                            limit, 'locked': locked, 'limitcash': limit//2,
                                                            'deflimit': limit, 'creditcard':credit_card}
                                dict = json.dumps(credit_dict)
                                f_credit_dict.seek(0)
                                f_credit_dict.truncate(0)
                                f_credit_dict.write(dict)
                                print('\033[32;1m信用卡%s发放成功，额度%s！\033[0m' % (credit_card, limit))
                            else:
                                print('\033[31;1m申请人姓名输入为空！\033[0m')
                        else:
                            print('\033[31;1m账号密码输入为空！\033[0m')
                    else:
                        print('\033[31;1m信用卡%s输入格式有误!\033[0m'% credit_card)
                else:
                    print('\033[31;1m信用卡%s已经存在！'% credit_card)
            elif if_credit == 'b':
                break
            else:
                errorlog.log('error', logging.INFO)
                # print('\033[31;1m输入有误，没有该选项！\033[0m')
# creditcard_create()


def lock_user():   # 用户锁定模块
    while True:
        print('\033[32;1m锁定用户\033[0m'.center(50, '-'))
        with open(settings._db_users_dict, 'r+') as f_users_dict:
            user_dict = json.load(f_users_dict)
            for key in user_dict:
                if user_dict[key]['locked'] == 0:
                    print('\033[32;1m系统用户【%s】\t\t锁定状态：【未锁定】\033[0m' % key)
                else:
                    print('\033[31;1m系统用户【%s】\t\t锁定状态：【已锁定】\033[0m' % key)
            if_lock = input('\033[34;1m是否要进行用户锁定 确定【Y】/返回【B】:\033[0m').strip().lower()
            if if_lock == 'y':
                will_lock_user = input('\033[34;1m输入要锁定的用户名：\033[0m')
                if will_lock_user in user_dict.keys():
                    if user_dict[will_lock_user]['locked'] == 0:
                        user_dict[will_lock_user]['locked'] = 1
                        dict = json.dumps(user_dict)
                        f_users_dict.seek(0)
                        f_users_dict.truncate(0)
                        f_users_dict.write(dict)
                        print('\033[32;1m用户%s锁定成功！\033[0m' % will_lock_user)
                    else:
                        print('\033[31;1m此次锁定失败，用户%s之前已被锁定！\033[0m' % will_lock_user)
                else:
                    print('\033[31;1m用户%s不存在！' % will_lock_user)
            elif if_lock == 'b':
                break
            else:
                errorlog.log('error', logging.INFO)
                # print('\033[31;1m输入有误，没有该选项！\033[0m')
# lock_user()


def unlock_user():  # 用户解锁模块
    while True:
        print('\033[32;1m解锁用户\033[0m'.center(50, '-'))
        with open(settings._db_users_dict, 'r+') as f_users_dict:
            user_dict = json.load(f_users_dict)
            for key in user_dict:
                if user_dict[key]['locked'] == 0:
                    print('\033[32;1m系统用户【%s】\t\t锁定状态：【未锁定】\033[0m' % key)
                else:
                    print('\033[31;1m系统用户【%s】\t\t锁定状态：【已锁定】\033[0m' % key)
            if_lock = input('\033[34;1m是否要进行用户解锁 确定【Y】/返回【B】:\033[0m').strip().lower()
            if if_lock == 'y':
                will_unlock_user = input('\033[34;1m输入要解锁的用户名：\033[0m')
                if will_unlock_user in user_dict.keys():
                    if user_dict[will_unlock_user]['locked'] == 1:
                        user_dict[will_unlock_user]['locked'] = 0
                        dict = json.dumps(user_dict)
                        f_users_dict.seek(0)
                        f_users_dict.truncate(0)
                        f_users_dict.write(dict)
                        print('\033[32;1m用户%s解锁成功！\033[0m' % will_unlock_user)
                    else:
                        print('\033[31;1m此次解锁失败，用户%s此前并未锁定！\033[0m' % will_unlock_user)
                else:
                    print('\033[31;1m用户%s不存在！' % will_unlock_user)
            elif if_lock == 'b':
                break
            else:
                errorlog.log('error', logging.INFO)
                # print('\033[31;1m输入有误，没有该选项！\033[0m')
# unlock_user()


def lock_creditcard():  # 信用卡冻结模块
    while True:
        print('\033[32;1m冻结信用卡\033[0m'.center(50, '-'))
        with open(settings._db_credit_dict, 'r+') as f_credit_dict:
            credit_dict = json.load(f_credit_dict)
            for key in credit_dict:
                if credit_dict[key]['locked'] == 0:
                    print('\033[32;1m信用卡账户【%s】\t\t冻结状态:【未冻结】' % key)
                else:
                    print('\033[31;1m信用卡账户【%s】\t\t冻结状态:【已冻结】' % key)
            if_lock = input('\033[34;1m是否要进行信用卡冻结 确定【Y】/返回【B】:\033[0m').strip().lower()
            if if_lock == 'y':
                will_lock_credit = input('\033[34;1m输入要冻结的信用卡账号：\033[0m')
                if will_lock_credit in credit_dict.keys():
                    if credit_dict[will_lock_credit]['locked'] == 0:
                        credit_dict[will_lock_credit]['locked'] = 1
                        dict = json.dumps(credit_dict)
                        f_credit_dict.seek(0)
                        f_credit_dict.truncate(0)
                        f_credit_dict.write(dict)
                        print('\033[32;1m信用卡账号%s冻结成功\033[0m' % will_lock_credit)
                    else:
                        print('\033[31;1m信用卡账号%s冻结失败，该账号此前已被冻结！\033[0m' % will_lock_credit)
                else:
                    print('\033[31;1m信用卡账号%s不存在！' % will_lock_credit)
            elif if_lock == 'b':
                break
            else:
                errorlog.log('error', logging.INFO)
                # print('\033[31;1m输入有误，没有该选项！\033[0m')
# lock_creditcard()


def unlock_creditcard():  # 解冻信用卡模块
    while True:
        print('\033[32;1m解冻信用卡\033[0m'.center(50, '-'))
        with open(settings._db_credit_dict, 'r+') as f_credit_dict:
            credit_dict = json.load(f_credit_dict)
            for key in credit_dict:
                if credit_dict[key]['locked'] == 0:
                    print('\033[32;1m信用卡账户【%s】\t\t冻结状态:【未冻结】' % key)
                else:
                    print('\033[31;1m信用卡账户【%s】\t\t冻结状态:【已冻结】' % key)
            if_lock = input('\033[34;1m是否要进行信用卡冻结 确定【Y】/返回【B】:\033[0m').strip().lower()
            if if_lock == 'y':
                will_lock_credit = input('\033[34;1m输入要解冻的信用卡账号：\033[0m')
                if will_lock_credit in credit_dict.keys():
                    if credit_dict[will_lock_credit]['locked'] == 1:
                        credit_dict[will_lock_credit]['locked'] = 0
                        dic = json.dumps(credit_dict)
                        f_credit_dict.seek(0)
                        f_credit_dict.truncate(0)
                        f_credit_dict.write(dic)
                        print('\033[32;1m信用卡账号%s解冻成功\033[0m' % will_lock_credit)
                    else:
                        print('\033[31;1m信用卡账号%s解冻失败，该账号此前未被冻结！\033[0m' % will_lock_credit)
                else:
                    print('\033[31;1m信用卡账号%s不存在！' % will_lock_credit)
            elif if_lock == 'b':
                break
            else:
                errorlog.log('error', logging.INFO)
                # print('\033[31;1m输入有误，没有该选项！\033[0m')
# unlock_creditcard()


def update_limit():  # 修改信用卡额度
    while True:
        print('\033[31;1m修改信用卡额度\033[0m'.center(50, '-'))
        with open(settings._db_credit_dict, 'r+') as f_credit_dict:
            credit_dict = json.load(f_credit_dict)
            for key in credit_dict:
                limitcash = credit_dict[key]['limitcash']
                print('信用卡【%s】\t目前可用额度：【￥%s】\t取现额度：【￥%s】'
                      % (key, credit_dict[key]['limit'], limitcash))
            if_update = input('\033[34;1m是否进行信用卡额度调整 确定【Y】/返回【B】：\033[0m').strip().lower()
            if if_update == 'y':
                creditcard = input('\033[34;1m输入要修改的信用卡的卡号：\033[1m').strip()
                if creditcard in credit_dict.keys():
                    limit_cash = input('\033[34;1m输入额度修改后的金额(至少5000￥)：\033[1m')
                    if limit_cash.isdigit():
                        limit_default = credit_dict[creditcard]['limit']
                        limit_cash = int(limit_cash)
                        if limit_cash >= 5000:
                            update = limit_cash - limit_default
                            credit_dict[creditcard]['limitcash'] += update//2  # 取现额度调整
                            credit_dict[creditcard]['limit'] += update  # 可用额度调整
                            credit_dict[creditcard]['deflimit'] = limit_cash  # 信用卡原本的默认额度
                            dict = json.dumps(credit_dict)
                            f_credit_dict.seek(0)
                            f_credit_dict.truncate(0)
                            f_credit_dict.write(dict)
                            print('\033[32;1m信用卡%s额度修改成功！\033[0m' % creditcard)
                        else:
                            print('\033[31;1m输入金额 ￥%s 小于￥5000\033[0m' % limit_cash)
                    else:
                        print('\033[31;1m输入金额 ￥%s 格式有误\033[0m' % limit_cash)
                else:
                    print('\033[31;1m信用卡【%s】不存在\033[0m' % creditcard)
            elif if_update == 'b':
                break
            else:
                errorlog.log('error', logging.INFO)
# update_limit()









