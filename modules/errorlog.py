"""错误日志记录模块"""
import logging
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings


def log(log_type, log_level):
    log_level = logging.INFO
    logger = logging.getLogger(log_type)   # 生成logger对象
    logger.setLevel(log_level)

    """生成handler对象，输出至屏幕、文件"""
    ch = logging.StreamHandler()   # 输出至屏幕
    ch.setLevel(log_level)

    log_file = settings.log_write     # 输出至指定文件
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level)

    """生成formatter对象"""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.warning('输入有误，没有该选项！')
# log('error', logging.INFO)