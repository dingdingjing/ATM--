"""信用卡模块,主要进行了：1、取现提示（须知）2、显示指定的信用卡信息 3、信用卡流水记录单 4、提现操作
 5、信用卡的转账操作 6、信用卡还款操作 7.查看信用卡的流水单"""
import json
import os
import time
import sys
import logging
# 获取主目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings
from modules import errorlog


def details_tip():  # 取现须知
    with open(settings._db_creditcard_details, 'r', encoding='utf-8') as f_creditcard_details:
        print(f_creditcard_details.read())


def my_creditcard(current_creditcard):  # 显示当前信用卡信息模块，其中current_creditcard用于传入当前持卡人信息
    while True:
        print('\033[32;1m我的信用卡信息\033[0m'.center(40, '-'))
        with open(settings._db_credit_dict, 'r+') as f_credit_dict:
            credit_dict = json.load(f_credit_dict)
            print('卡号：\t【%s】\n额度:\t【￥%s】\n提现额度:\t【￥%s】\n持卡人:\t【%s】\n' %
                  (current_creditcard, credit_dict[current_creditcard]['limit'],
                   credit_dict[current_creditcard]['limitcash'], credit_dict[current_creditcard]['personinfo']))
            if_back = input('\033[34;1m是否退出当前界面 返回【b】:\033[0m').strip().lower()
            if if_back == 'b':
                break
# my_creditcard('666666')


def creditcard_record(creditcard, value):  # 信用卡流水记录,传入的是信用卡账号以及具体操作，如购买×
    with open(settings._db_creditcard_record, 'r+') as f_creditcard_record:
        record_dict = json.load(f_creditcard_record)
        day = time.strftime('%Y-%m-%d', time.localtime())
        times = time.strftime('%H:%M:%S')
        if str(creditcard) not in record_dict.keys():
            record_dict[creditcard] = {day: {times: value}}
        else:
            if day not in record_dict[creditcard].keys():
                record_dict[creditcard][day] = {times: value}
            else:
                record_dict[creditcard][day][times] = value
        dict = json.dumps(record_dict)
        f_creditcard_record.seek(0)
        f_creditcard_record.truncate(0)
        f_creditcard_record.write(dict)
# creditcard_record('222222', "购物支付 6297")


def cash_advance(current_creditcard):  # 提现操作(传入的值是当前操作的信用卡账号)
    while True:
        print('\033[32;1m提现\033[0m'.center(40, '-'))
        with open(settings._db_credit_dict, 'r+') as f_credit_dict:
            credit_dict = json.load(f_credit_dict)
            limit = credit_dict[current_creditcard]['limit']
            limitcash = credit_dict[current_creditcard]['limitcash']
            print('信用卡号：\t【%s】\n提现额度:\t【￥%s】' % (current_creditcard, limitcash))
            details_tip()
            if_cash = input('\033[34;1m是否进行提现 确定【Y】/返回【B】:\033[0m').strip().lower()
            if if_cash == 'y':
                cash = input('\033[34;1m输入要提现的金额 收取%5手续费\033[0m:')
                if cash.isdigit():
                    cash = int(cash)
                    if cash != 0:
                        if cash <= limitcash:
                            limitcash -= int(cash*1.05)
                            limit -= int(cash*1.05)
                            credit_dict[current_creditcard]['limit'] = limit
                            credit_dict[current_creditcard]['limitcash'] = limitcash
                            dict = json.dumps(credit_dict)
                            f_credit_dict.seek(0)
                            f_credit_dict.truncate(0)
                            f_credit_dict.write(dict)
                            record = '\033[31;1m提现￥%s手续费￥%s\033[0m' % (cash, int(cash*0.05))
                            print(record, '\n')
                            creditcard_record(current_creditcard, record)
                        else:
                            print('\033[31;1m超出信用卡提现额度!\033[0m')
                    else:
                        print('\033[31;1m提现额度不能为空！\033[0m')
                else:
                    print('\033[31;1m格式输入有误！\033[0m')
            elif if_cash == 'b':
                break
            else:
                errorlog.log('error', logging.INFO)
                # print('\033[31;1m输入格式有误！\033[0m')

# cash_advance('222222')


def transfer(current_creditcard):  # 信用卡转账
    while True:
        print('\033[32;1m转账\033[0m'.center(40, '-'))
        if_trans = input('\033[34;1m 是否进行转账 确定【Y】/返回【B】:\033[0m').strip().lower()
        if if_trans == 'y':
            with open(settings._db_credit_dict, 'r+') as f_credit_dict:
                credit_dict = json.load(f_credit_dict)
                current_limit = credit_dict[current_creditcard]['limit']
                transfer_creditcard = input('\033[34;1m输入要转账的银行卡卡号:\033[0m')
                if transfer_creditcard.isdigit():
                    if len(transfer_creditcard) == 6:
                        if transfer_creditcard in credit_dict.keys():
                            again_credit = input('\033[34;1m请再次确认转账的银行卡卡号：')
                            if again_credit == transfer_creditcard:
                                transfer_cash = input('\033[34;1m请输入要转账的金额：')
                                if transfer_cash.isdigit():
                                    transfer_cash = int(transfer_cash)
                                    if transfer_cash <= current_limit:
                                        credit_dict[current_creditcard]['limit'] -= transfer_cash
                                        credit_dict[transfer_creditcard]['limit'] += transfer_cash
                                        dict = json.dumps(credit_dict)
                                        f_credit_dict.seek(0)
                                        f_credit_dict.truncate(0)
                                        f_credit_dict.write(dict)
                                        record = '\033[32;1m转账卡号 %s 金额 ￥%s 转账成功!\033[0m' % \
                                                 (transfer_creditcard, transfer_cash)
                                        print(record, '\n')
                                        creditcard_record(current_creditcard, record)
                                    else:
                                        print('\033[31;1m 余额不足 转账失败！\033[0m')
                                else:
                                    print('\033[31;1m输入金额有误！\033[0m')
                            else:
                                print('\033[31;1m两次输入的银行卡卡号不一致！\033[0m')
                        else:
                            print('\033[31;1m您输入的银行卡卡号不存在！\033[0m')
                    else:
                        print('\033[31;1m输入的银行卡卡号有误！\033[0m')
                else:
                    print('\033[31;1m输入的银行卡卡号有误！\033[0m')
        elif if_trans == 'b':
            break
        else:
            errorlog.log('error', logging.INFO)
            # print('\033[31;1m输入格式有误！\033[0m')
# transfer('222222')


def repayment(current_creditcard):   # 信用卡还款
    while True:
        print('\033[32;1m还款\033[0m'.center(40, '-'))
        if_repay = input('\033[34;1m是否进行还款操作 确定【Y】/返回【B】:').strip().lower()
        if if_repay == 'y':
            repay_cash = input('\033[34;1m请输入要还款的金额\033[0m:')
            if repay_cash.isdigit():
                repay_cash = int(repay_cash)
                with open(settings._db_credit_dict, 'r+') as f_credit_dict:
                    credit_dict = json.load(f_credit_dict)
                    limit = credit_dict[current_creditcard]['limit']
                    limit += repay_cash
                    credit_dict[current_creditcard]['limit'] = limit
                    dict = json.dumps(credit_dict)
                    f_credit_dict.seek(0)
                    f_credit_dict.truncate(0)
                    f_credit_dict.write(dict)
                    record = '\033[32;1m信用卡 %s 还款金额 ￥%s 还款成功！\033[0m' % (current_creditcard, repay_cash)
                    print(record, '\n')
                    creditcard_record(current_creditcard, record)
            else:
                print('\033[31;1m还款金额格式输入有误！\033[0m')
        elif if_repay == 'b':
            break
        else:
            errorlog.log('error', logging.INFO)
            # print('\033[31;1m输入格式有误！\033[0m')
# repayment('222222')


def catcard_record(current_creditcard):  # 查看信用卡流水单
    while True:
        print('\033[32;1m信用卡流水单\033[0m'.center(40, '-'))
        with open(settings._db_creditcard_record, 'r+') as f_creditcard_record:
            f_creditcard_record.seek(0)
            record_dict = json.load(f_creditcard_record)
           # print(record_dict)
            print('\033[34;1m流水单日期\033[0m:')
            if current_creditcard in record_dict.keys():
                for key in record_dict[current_creditcard].keys():
                    print(key)
                date = input('\033[34;1m流水单查询 返回【b】/输入流水单的日期【2018-01-15】:\033[0m').strip()
                if date == 'b':
                    break
                if date in record_dict[current_creditcard].keys():
                    keys = sorted(record_dict[current_creditcard][date])
                    print('\033[31;1m当前信用卡【%s】交易记录如下：\033[0m' % current_creditcard)
                    for key in keys:
                        print('\033[32;1m时间：%s  %s\033[0m' % (key, record_dict[current_creditcard][date][key]))
                    print('')
                else:
                    print('\033[31;1m输入日期有误！\033[0m')
            else:
                print('\033[31;1m信用卡 %s 目前还未进行过消费！\033[0m' % current_creditcard)
                break

# catcard_record('222222')

