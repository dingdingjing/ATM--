"""
main program handle module,handle all the user interaction stuff
以下为要实现的功能
"""
# 1、额度 15000或自定义
# 2、实现购物商城，买东西加入 购物车，调用信用卡接口结账
# 3、可以提现，手续费5%
# 4、支持多账户登录
# 5、支持账户间转账
# 6、记录每月日常消费流水
# 7、提供还款接口
# 8、ATM记录操作日志
# 9、提供管理接口，包括添加账户、用户额度，冻结账户等。。。
# 10、用户认证用装饰器
import sys
import os
import logging

# 程序主目录

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 添加环境变量
sys.path.append(BASE_DIR)
from modules import admincenter, shopping, authentication, creditcard, errorlog  # 将管理模块，购物模块，认证模块和信用卡模块导入

while True:
    print('\033[35;1m欢迎进入信用卡购物模拟程序\033[0m:'.center(50, '='),
          '\n1. 购物中心\n'
          '2. 信用卡中心\n'
          '3. 后台管理\n'
          'q. 退出程序\n')
    choice_id = input('\033[34;1m请选择要进入模式的ID\033[0m:').strip().lower()
    if not choice_id: continue
    if choice_id == '1':
        res = authentication.user_auth()
        # print(res)
        # print(res[0], res[1])
        if res:
            if res[0] == True:
                current_user = res[1]
                shopping.empty_shopping_car()
                while True:
                    print('\033[36;1m欢迎进入购物中心\033[0m'.center(50, '='),
                          '\n1. 购物商场\n'
                          '2. 查看购物车\n'
                          '3. 购物结算\n'
                          '4. 个人中心\n'
                          'b. 返回\n')
                    choice_id = input('\033[34;1m选择要进入模式的ID：\033[0m').strip().lower()
                    if choice_id == '1':
                        shopping.shopping_mall()
                    elif choice_id == '2':
                        shopping.shopping_car()
                    elif choice_id == '3':
                        shopping.pay_shopping(current_user)
                    elif choice_id == '4':
                        while True:
                            print('\033[33;1m个人中心\033[0m'.center(50, '='),
                                  '\n1. 购物历史账单\n'
                                  '2. 修改登录密码\n'
                                  '3. 修改个人信息\n'
                                  '4. 修改银行卡绑定\n'
                                  'b. 返回\n')
                            choice_id = input('\033[34;1m选择要进入模式的ID:\033[0m').strip().lower()
                            if choice_id == '1':
                                shopping.cat_shopping_record(current_user)
                            elif choice_id == '2':
                                shopping.update_password(current_user)
                            elif choice_id == '3':
                                shopping.update_address(current_user)
                            elif choice_id == '4':
                                shopping.bind_creditcard(current_user)
                            elif choice_id == 'b':
                                break
                            else:
                                errorlog.log('error', logging.INFO)
                                # print('\033[31;1m无效的输入！\033[0m')
                    elif choice_id == 'b':
                        break
                    else:
                        errorlog.log('error', logging.INFO)
                        # print('\033[31;1m无效的输入！\033[0m')
    elif choice_id == '2':
        res = authentication.credit_auth()
        if res:
            if res[0] == True:
                current_creditcard = res[1]
                while True:
                    print('\033[36;1m信用卡中心\033[0m'.center(50, '='),
                          '\n1. 我的信用卡\n'
                          '2. 提现\n'
                          '3. 转账\n'
                          '4. 还款\n'
                          '5. 流水记录\n'
                          'b. 返回\n')
                    choice_id = input('\033[34;1m选择要进入模式的ID:').strip().lower()
                    if choice_id == '1':
                        creditcard.my_creditcard(current_creditcard)
                    elif choice_id == '2':
                        creditcard.cash_advance(current_creditcard)
                    elif choice_id == '3':
                        creditcard.transfer(current_creditcard)
                    elif choice_id == '4':
                        creditcard.repayment(current_creditcard)
                    elif choice_id == '5':
                        creditcard.catcard_record(current_creditcard)
                    elif choice_id == 'b':
                        break
                    else:
                        errorlog.log('error', logging.INFO)
                        # print('\033[31;1m无效的输入！\033[0m')

    elif choice_id == '3':
        res = authentication.admincenter_auth()
        if res:
            while True:
                print('\033[36;1m管理中心\033[0m'.center(50, '='),
                      '\n1. 创建账号\n'
                      '2. 锁定账号\n'
                      '3. 解锁账号\n'
                      '4. 发行信用卡\n'
                      '5. 冻结信用卡\n'
                      '6. 解冻信用卡\n'
                      '7. 提升信用卡额度\n'
                      'b. 返回\n')
                choice_id = input('\033[34;0m请选择要进入模式的ID：').strip().lower()
                if choice_id == '1':
                    admincenter.user_create()
                elif choice_id == '2':
                    admincenter.lock_user()
                elif choice_id == '3':
                    admincenter.unlock_user()
                elif choice_id == '4':
                    admincenter.creditcard_create()
                elif choice_id == '5':
                    admincenter.lock_creditcard()
                elif choice_id == '6':
                    admincenter.unlock_creditcard()
                elif choice_id == '7':
                    admincenter.update_limit()
                elif choice_id == 'b':
                    break
                else:
                    errorlog.log('error', logging.INFO)
                    # print('\033[31;1m无效的输入！\033[0m')

    elif choice_id == 'q':
        break
    else:
        errorlog.log('error', logging.INFO)
        # print('\033[31;1m无效的输入！\033[0m')

