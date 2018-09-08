import logging
import threading
from logging.handlers import RotatingFileHandler

from wechatManager.config import BaseConfig, configs


CONFIG = BaseConfig
from wechatManager import core

def setup_log(CONFIG):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=CONFIG.LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)



def start_manage(config_name):
    global CONFIG
    CONFIG = configs[config_name]

    setup_log(CONFIG)
    while True:  # 主循环
        try:
            dictKeys = core.onlineDict.keys()
            for userName in dictKeys:
                user = core.onlineDict[userName]
                if user.loading:
                    if user.alive:
                        if user.receiveMsg:
                            threading.Thread(target=user.run).start()
                            user.receiveMsg = False
                    else:
                        threading.Thread(target=user.login).start()
                        user.alive = True
                else:
                    if user.online:
                        user.logout()
        except RuntimeError as reason:
            print('index Error:', reason)


def create_admin(adminName):
    core.onlineDict[adminName]           = core.User(adminName)
    core.onlineDict[adminName].cmdQR     = CONFIG.CMDQR
    core.onlineDict[adminName].autoLogin = True
    core.onlineDict[adminName].loading   = True