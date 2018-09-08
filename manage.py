#!/usr/bin/python3.6
# coding=utf-8
from wechatManager import create_admin, start_manage

# TODO 设置超级管理员密码
# TODO 管理员掉线重连


if __name__ == '__main__':
    create_admin('superadmin')
    start_manage('development')


