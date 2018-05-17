"""购物模块，此模块主要包含：1、购物商城 2、清空购物车 3、购物车信息显示 4、购物记录
5.查看购物记录 6、信用卡密码认证 7、购物结算 8、信用卡绑定 9、修改登录密码 10、修改个人资料"""
import json
import os
import time
import sys
import logging
# 程序主目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings
from modules import errorlog

def shopping_mall():   # 购物商城(实现了将商城中现有显示出来，供用户挑选，在用户返回时已将用户所选商品添加到了购物车中)
    shopping_list, pro_list = [], []
    with open(settings._db_product, 'r+', encoding='utf-8') as f_product:
        for item in f_product:
            pro_list.append(item.strip('\n').split())  # 商品列表
            # pro_list.append(item)

    def pro_info():
        print('编号\t\t商品\t\t\t价格')
        for index, item in enumerate(pro_list):
            print('%s\t\t%s\t\t%s' % (index, item[0], item[1]))
    while True:
        print('\033[32;1m目前商场在售的商品信息\033[0m'.center(40, '-'))
        pro_info()
        choice_id = input('\033[34;1m选择要购买的商品编号 【购买 ID】/【返回 b】\033[0m:')
        if choice_id.isdigit():
            choice_id = int(choice_id)
            if 0 <= choice_id < len(pro_list):
                pro_item = pro_list[choice_id]
                print('\033[32;1m商品【%s】加入购物车 价格【￥%s】\033[0m' % (pro_item[0], pro_item[1]))
                shopping_list.append(pro_item)
            else:
                print('\033[31;1m输入有误，没有该编号的商品信息！\033[0m')
        elif choice_id == 'b' or 'B':
            with open(settings._db_shopping_car, 'r+', encoding='utf-8') as f_shopping_car:
                shoppings_car = json.load(f_shopping_car)
                shoppings_car.extend(shopping_list)
                dict = json.dumps(shoppings_car)
                f_shopping_car.seek(0)
                f_shopping_car.truncate(0)
                f_shopping_car.write(dict)
            break
        else:
            print('\033[31;1mERROR，输入有误！')
# shopping_mall()


def empty_shopping_car():  # 清空购物车
    with open(settings._db_shopping_car, 'r+') as f_shopping_car:
        f_shopping_car.seek(0)
        f_shopping_car.truncate(0)
        dict = json.dumps([])
        f_shopping_car.write(dict)

# empty_shopping_car()


def shopping_car():  # 购物车信息显示
    while True:
        with open(settings._db_shopping_car, 'r+') as f_shopping_car:
            dict = json.load(f_shopping_car)
            print('\033[32;1m购物车信息清单\033[0m'.center(40, '-'))
            for index, item in enumerate(dict):
                print(index, item[0], item[1])
            print('\033[32;1m商品总额共计:%s\033[0m' % len(dict))
        if_buy = input('\033[34;0m选择要进行的操作 返回【B】/购物车清空【F】:\033[0m').strip().lower()
        if if_buy == 'b':
            break
        if if_buy == 'f':
            empty_shopping_car()

# shopping_car()


def shoppingcar_record(current_user, value):   # 购物记录
    with open(settings._db_shopping_record, 'r+') as f_shopping_record:
        record_dict = json.load(f_shopping_record)
        day = time.strftime('%Y-%m-%d', time.localtime())
        times = time.strftime('%H:%M:%S')
        if str(current_user) not in record_dict.keys():
            record_dict[current_user] = {day: {times:value}}
        else:
            if day not in record_dict[current_user].keys():
                record_dict[current_user][day] = {times: value}
            else:
                record_dict[current_user][day][times] = value
        dict = json.dumps(record_dict)
        f_shopping_record.seek(0)
        f_shopping_record.truncate(0)
        f_shopping_record.write(dict)


def cat_shopping_record(current_user):  # 查看购物记录
    while True:
        print('\033[32;1m用户 %s  购物记录\033[0m'.center(40, '-') % current_user)
        with open(settings._db_shopping_record, 'r+') as f_shopping_record:
            record_dict = json.load(f_shopping_record)
            if current_user not in record_dict.keys():
                print('\033[31;1m用户 %s  此前还未进行过消费！' % current_user)
            else:
                data = sorted(record_dict[current_user])
                for d in data:
                    times = sorted(record_dict[current_user][d])
                    for t in times:
                        print('\033[32;1m【时间】 %s %s\033[0m' % (d, t))
                        items = record_dict[current_user][d][t]
                        print('\033[32;1m【商品】     【价格】\033[0m')
                        for v in items:
                            print('\033[32;1m%s\t\t%s\033[0m' % (v[0], v[1]))
            if_back = input('\033[34;1m是否返回 返回【B】:\033[0m').strip().lower()
            if if_back == 'b':
                break
# cat_shopping_record('dingding')


def creditcard_record(creditcard, value):  # 信用卡账单记录
    with open(settings._db_creditcard_record, 'r+') as f_creditcard_record:
        record_dict = json.load(f_creditcard_record)
        days = time.strftime('%Y-%m-%d', time.localtime())
        times = time.strftime('%H:%M:%S')
        if str(creditcard) not in record_dict.keys():
            record_dict[creditcard] = {days:{times: value}}
        else:
            if days not in record_dict[creditcard].keys():
                record_dict[creditcard][days] = {times: value}
            else:
                record_dict[creditcard][days][times] = value
        dict = json.dumps(record_dict)
        f_creditcard_record.seek(0)
        f_creditcard_record.truncate(0)
        f_creditcard_record.write(dict)
# creditcard_record('888888', 'iphone')


def auth_creditcard(creditcard):  # 信用卡密码认证
    with open(settings._db_credit_dict, 'r+') as f_credit_dict:
        credit_dict = json.load(f_credit_dict)
        password = input('\033[34;1m当前信用卡【%s】   请输入支付密码：\033[0m' % creditcard)
        if password == credit_dict[creditcard]['password']:
            return True
        else:
            print('\033[31;1m密码输入错误，支付失败！\033[0m')
# auth_creditcard('222222')


def pay_shopping(current_user):  # 支付模块
    while True:
        sum_money = 0
        print('\033[32;1m购物结算\033[0m'.center(40, '-'))
        with open(settings._db_shopping_car, 'r+') as f_shopping_car:
            shopping_dict = json.load(f_shopping_car)
            for item in shopping_dict:
                sum_money += int(item[1])
            if_pay = input('\033[34;1m当前商品总额：%s 是否进行支付 确定【Y】/返回【B】:\033[0m' % sum_money).strip().lower()
            if if_pay == 'y':
                with open(settings._db_users_dict, 'r+') as f_users_dict:
                    users_dict = json.load(f_users_dict)
                    creditcard = users_dict[current_user]['creditcard']
                    if creditcard == 0:
                        print('\033[31;1m账号 %s还未绑定信用卡，请到个人中心进行信用卡绑定\033[0m' % current_user)
                    else:
                        with open(settings._db_credit_dict, 'r+') as f_credit_dict:
                            credit_dict = json.load(f_credit_dict)
                            limit = credit_dict[creditcard]['limit']
                            limit_new = limit - sum_money
                            if limit_new >= 0:
                                res = auth_creditcard(creditcard)
                                if res == True:
                                    credit_dict[creditcard]['limit'] = limit_new
                                    dic = json.dumps(credit_dict)
                                    f_credit_dict.seek(0)
                                    f_credit_dict.truncate(0)
                                    f_credit_dict.write(dic)
                                    value = '购物支付 %s' % (sum_money)
                                    print('\033[32;1m支付成功，当前余额 ￥%s\033[0m' % limit_new)
                                    shoppingcar_record(current_user, shopping_dict)
                                    creditcard_record(creditcard, value)
                                    empty_shopping_car()
                            else:
                                print('\033[31;1m当前信用卡额度 %s 不足以支付当前账单，可选择绑定其他信用卡进行支付！'
                                      % limit_new)
            elif if_pay == 'b':
                break
            else:
                errorlog.log('error', logging.INFO)

# pay_shopping('laoding')


def bind_creditcard(current_user):  # 信用卡绑定
    while True:
        print('\033[32;1m信用卡绑定中心\033[0m'.center(40, '-'))
        with open(settings._db_users_dict, 'r+') as f_users_dict:
            users_dict = json.load(f_users_dict)
            creditcard = users_dict[current_user]['creditcard']
            if creditcard == 0:
                print('当前用户:    %s' % current_user)
                print('信用卡绑定状态：\033[31;1m未绑定\033[0m')
            else:
                print('当前用户：    %s' % current_user)
                print('信用卡绑定:   %s' % creditcard)
            if_update = input('\033[34;1m是否要修改信用卡绑定 确定【Y】/返回【B】\033[0m:').strip().lower()
            if if_update == 'y':
                creditcard_new = input('\033[34;1m请输入要绑定的信用卡卡号(6位数字):\033[0m')
                if creditcard_new.isdigit() and len(creditcard_new) == 6:
                    with open(settings._db_credit_dict, 'r+') as f_credit_dict:
                        credit_dict = json.load(f_credit_dict)
                        # print(credit_dict.keys())
                        if str(creditcard_new) in credit_dict.keys():
                            users_dict[current_user]['creditcard'] = creditcard_new
                            dict = json.dumps(users_dict)
                            f_users_dict.seek(0)
                            f_users_dict.truncate(0)
                            f_users_dict.write(dict)
                            print('\033[32;1m信用卡%s绑定成功！\033[0m' % creditcard_new)
                        else:
                            print('\033[31;1m输入的信用卡卡号不存在！\033[0m')
                else:
                    print('\033[31;1m信用卡格式输入有误！\033[0m')

            elif if_update == 'b':
                break
            else:
                errorlog.log('error', logging.INFO)

# bind_creditcard('ding')


def update_password(current_user):   # 修改登录密码
    while True:
        print('\033[32;1m修改登录密码\033[0m'.center(40, '-'))
        print('当前用户:\t%s\n当前密码：\t***' % current_user)
        if_update = input('\033[34;0m是否要修改 %s 登录密码 确定【Y】/返回【B】:' % current_user).strip().lower()
        if if_update == 'y':
            with open(settings._db_users_dict, 'r+') as f_users_dict:
                users_dict = json.load(f_users_dict)
                password = users_dict[current_user]['password']
                old_pwd = input('\033[34;1m请输入原来的密码：\033[0m')
                if old_pwd == password:
                    new_pwd = input('\033[34;1m请输入新密码：')
                    again_new_pwd = input('\033[34;1m请再次输入新密码：')
                    if new_pwd == again_new_pwd:
                        users_dict[current_user]['password'] = new_pwd
                        dict = json.dumps(users_dict)
                        f_users_dict.seek(0)
                        f_users_dict.truncate(0)
                        f_users_dict.write(dict)
                        print('\033[32;1m用户%s密码修改成功！' % current_user)
                    else:
                        print('\033[31;1m输入的两次密码不一致！\033[0m')
                else:
                    print('\033[31;1m密码输入错误！\033[0m')

        elif if_update == 'b':
            break
        else:
            errorlog.log('error', logging.INFO)
# update_password('ding')


def update_address(current_user):  # 修改个人资料中收货地址信息
    while True:
        print('\033[32;1m修改个人资料\033[0m'.center(40, '-'))
        with open(settings._db_users_dict, 'r+') as f_users_dict:
            users_dict = json.load(f_users_dict)
            address = users_dict[current_user]['address']
            print('当前用户：\t%s\n当前收货地址：\t%s\n' % (current_user, address))
            if_update = input('\033[34;1m是否要修改用户%s的收货地址 确定【Y】/返回【B】:').strip().lower()
            if if_update == 'y':
                address_new = input('\033[34;0m输入新的收货地址：\033[0m')
                users_dict[current_user]['address'] = address_new
                dic = json.dumps(users_dict)
                f_users_dict.seek(0)
                f_users_dict.truncate(0)
                f_users_dict.write(dic)
                print('\033[32;1m用户%s的收货地址修改成功！' % current_user)

            elif if_update == 'b':
                break
            else:
                errorlog.log('error', logging.INFO)
# update_address('ding')


