import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_db_product = BASE_DIR + r'/database/product_list'  # 商城产品数据库
_db_shopping_car = BASE_DIR + r'/database/shopping_car'  # 购物车数据库
_db_users_dict = BASE_DIR + r'/database/users_dict'      # 用户数据库
_db_credit_dict = BASE_DIR + r'/database/credit_dict'    # 信用卡数据库
_db_shopping_record = BASE_DIR + r'/database/shopping_record'  # 购物车数据库
_db_creditcard_record = BASE_DIR + r'/database/creditcard_record'    # 信用卡流水记录数据库
_db_creditcard_details = BASE_DIR + r'/database/creditcard_details'  # 信用卡界面的提示信息

log_write = BASE_DIR + r'/logs/error.log'  # 错误日志记录