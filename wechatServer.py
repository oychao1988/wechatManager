#!/usr/bin/python3.6
# coding=utf-8
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import threading
import users

# TODO 设置超级管理员密码
# TODO 管理员掉线重连

def main():
    superAdmin = '欧阳超'
    users.onlineDict[superAdmin]           = users.User(superAdmin)
    users.onlineDict[superAdmin].cmdQR     = True
    users.onlineDict[superAdmin].autoLogin = True
    users.onlineDict[superAdmin].loading   = True
    while True:  # 主循环
        try:
            dictKeys = users.onlineDict.keys()
            for userName in dictKeys:
                user = users.onlineDict[userName]
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

main()
if __name__ == '__main__':
    pass


