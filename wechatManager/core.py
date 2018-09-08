import os
import time
import datetime
import random
import json

import itchat
from itchat.content import *
import pyecharts
import jieba
import re

from wechatManager.storage import MysqlHelper
from wechatManager.log import logging
from wechatManager.plugins import SchemeTimerThead
from wechatManager import CONFIG

class User(object):
    def __init__(self, nickName):
        self.nickName        = nickName

        self.mysqlHelper     = MysqlHelper(CONFIG.connectionDict)
        self.MysqlInspect()
        self.instance        = itchat.new_instance()
        self.schemeTimer     = SchemeTimerThead()

        self.userInfo        = self.mysqlHelper.getOne('users', column='nickName', value=nickName)
        self.userType        = self.userInfo['userType']
        self.autoLogin       = self.userInfo['autoLogin']
        self.autoReply       = self.userInfo['autoReply']
        self.fileHelper      = self.userInfo['filehelper']
        self.separator       = ',*,'
        self.autoReplyGroup  = list(self.userInfo['autoReplyGroup'].split(self.separator)) if self.userInfo[
            'autoReplyGroup'] else []

        self.cmdQR           = None
        self.loading         = None
        self.alive           = None
        self.online          = None
        self.receiveMsg      = None

        self.userName        = None
        self.uin             = None
        self.robotNickName   = None
        self.robotUserName   = None
        self.FTUserName      = None
        self.FTNickName      = None

        self.frdList         = []
        self.frdInfoList     = []
        self.chatroomList    = []
        self.chatroomMembers = []

        self.cmds            = getattr(CONFIG, 'cmdsLv' + str(self.userType))
        self.remoteCmds      = getattr(CONFIG, 'remoteCmdsLv' + str(self.userType))

        # 日志路径
        self.savedir         = os.path.dirname(os.path.abspath(__file__)) + r'/users/%s/' % self.nickName
        self.chatDir         = self.savedir + CONFIG.chatDir
        self.cmdDir          = self.savedir + CONFIG.cmdDir
        self.errDir          = self.savedir + CONFIG.errDir
        self.chatroomDir     = self.savedir + CONFIG.chatroomDir
        self.cmdFile         = self.cmdDir  + 'cmdFile.txt'
        self.errFile         = self.errDir  + 'errFile.txt'
        self.sourcedir       = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/source/'

    def setDefault(self):
        '''
        定义用户权限
        '''
        pass
    def MysqlInspect(self):
        pass
    def login(self):
        pass
    def logout(self):
        pass
    def lc(self):
        pass
    def ec(self):
        pass
    def run(self):
        pass
    def getFriends(self):
        pass
    def getChatrooms(self):
        pass
    def getChatroomMembers(self):
        pass
    def getMps(self):
        pass
    def remoteLogin(self):
        pass
    def msgProcess(self):
        pass

    def tips(self):
        pass
    def addUser(self):
        pass
    def delUser(self):
        pass
    def addReply(self, nickName):
        pass
    def delReply(self):
        pass
    def autoReplyOn(self):
        pass
    def autoReplyOff(self):
        pass
    def fileHelperOn(self):
        pass
    def fileHelperOff(self):
        pass
    def getUserDict(self):
        pass
    def userOnline(self):
        pass
    def updateFriendList(self):
        pass
    def updateChatroomList(self):
        pass

    def getAttr(self):
        pass
    def checkFriendStatus(self):
        pass
    def mfRatio(self):
        pass
    def signatureCloud(self):
        pass
    def geoData(self):
        pass
    def friendInChatrooms(self):
        pass
    def autoAddFriendInChatroom(self):
        pass
    def schemeOfMemery(self):
        pass


# ----------------------------------------------------------------
# TODO 完善管理员指令
def tips(self):  # 提示命令
    cmd = 'tips'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    try:
        self.instance.send('操作指令：\n' + str(self.cmds))
        self.instance.send('远程操作指令：\n' + str(self.remoteCmds))
        logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
    except Exception as reason:
        logging(self.errFile, self.nickName, infoType='err',other=cmd, info=reason)


def addUser(self, nickName, userType):  # 添加用户
    cmd = 'addUser-%s-%s' % (nickName, userType)
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    try:
        userType = int(userType)
    except TypeError as reason:
        self.instance.send('用户类型输入错误')
        logging(self.errFile, self.nickName, infoType='err', other=cmd, info=reason)
        return
    if self.userType < userType:
        if self.mysqlHelper.getOne('users', column='nickName', value=nickName):
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info='当前用户已存在')
            self.instance.send('当前用户已存在')
            return
        else:
            if nickName not in [each['NickName'] for each in self.frdInfoList]:
                logging(self.errFile, self.nickName, infoType='err', other=cmd, info='当前用户不在您的好友名单中')
                self.instance.send('当前用户不在您的好友名单中')
                return
            if userType not in CONFIG.userTypes:
                logging(self.errFile, self.nickName, infoType='err', other=cmd, info='用户类型输入错误')
                self.instance.send('用户类型输入错误')
                return
            try:
                self.mysqlHelper.insertOne('users', nickName=nickName, userType=userType)
                self.setDefault(nickName, userType)

                logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd, status='success', info='成功添加新用户：%s' % nickName)
                self.instance.send('成功添加新用户：%s' % nickName)
                return
            except Exception as reason:
                logging(self.errFile, self.nickName, infoType='err', other=cmd, info=reason)
                self.instance.send('%s' % str(reason))
                return
    else:
        logging(self.errFile, self.nickName, infoType='err', other=cmd, info='您的权限不足')
        self.instance.send('您的权限不足')


def delUser(self, nickName):  # 删除用户
    cmd = 'delUser-%s' % nickName
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    try:
        if self.mysqlHelper.getOne('users', 'nickName', nickName):
            if nickName in onlineDict:
                del onlineDict[nickName]
            self.mysqlHelper.delete('users', 'nickName', nickName)
            logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd, status='success', info='成功删除用户:%s' % nickName)
            self.instance.send('成功删除用户:%s' % (nickName))
            return
    except Exception as reason:
        logging(self.errFile, self.nickName, infoType='err', other=cmd, info=reason)
        self.instance.send('删除用户失败:%s' % (nickName), reason)


def remoteLogin(self, frdNickName):  # 远程登录
    cmd = 'remoteLogin-%s' % frdNickName
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    user = self.mysqlHelper.getOne('users', 'nickName', frdNickName)
    frdUserName = self.instance.search_friends(name=frdNickName)[0]['UserName']
    if user:
        if (frdNickName in onlineDict.keys()) and onlineDict[frdNickName].instance.alive:
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info='该用户已成功登录')
            self.instance.send('您已成功登录！', toUserName=frdUserName)
        else:
            try:
                del onlineDict[frdNickName]
            except Exception as reason:
                logging(self.errFile, self.nickName, infoType='err', other=cmd, info=reason)
            onlineDict[frdNickName] = User(frdNickName)
            qrPath = os.path.dirname(os.path.abspath(__file__)) + '/users/%s/QR.png' % frdNickName
            if os.path.exists(qrPath): os.remove(qrPath)
            onlineDict[frdNickName].loading = True
            for i in range(30):
                if onlineDict[frdNickName].instance.alive:
                    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
                    self.instance.send('登录成功', toUserName=frdUserName)
                    return
                if os.path.exists(qrPath):
                    self.instance.send_image(qrPath, toUserName=frdUserName)
                    self.instance.send('请扫描二维码登录，或在手机上确认登录', toUserName=frdUserName)
                    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd, status='success', info='二维码发送成功，收件人：%s' % frdNickName)
                    return
                time.sleep(1)
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info='连接失败:%s' % frdNickName)
            self.instance.send('连接超时，请稍后重试', toUserName=frdUserName)
            return
    else:
        logging(self.errFile, self.nickName, infoType='err', other=cmd, info='该用户还未注册:%s' % frdNickName)
        self.instance.send('该用户还未注册:%s' % frdNickName, toUserName=frdUserName)
        return


def addReply(self, nickName, chatroom=None):  # 添加自动回复成员
    if chatroom:  #  添加群
        cmd = 'addReply %s chatroom' % nickName
        logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
        chatroomList = self.getChatrooms()
        if nickName in [each['NickName'] for each in chatroomList]:
            memberList = self.getChatroomMembers(nickName)['MemberList']
            friendsInChatroom = [each['NickName'] for each in memberList
                                 if each['NickName'] in [each['NickName']
                                 for each in self.frdInfoList[1:]]]
            friendsInChatroom = [nickName for nickName in friendsInChatroom if nickName not in self.autoReplyGroup]
            if friendsInChatroom:
                self.autoReplyGroup.extend(friendsInChatroom)
                self.mysqlHelper.update('users', 'autoReplyGroup', self.separator.join(self.autoReplyGroup), 'nickName', self.nickName)
                logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
                self.instance.send('成功！群[%s]中的好友成功加入自动回复名单' % nickName, toUserName=self.userName)
            else:
                logging(self.errFile, self.nickName, infoType='err', other=cmd, info='群[%s]中的好友已经在自动回复名单中' % nickName)
                self.instance.send('失败！群[%s]中的好友已经在自动回复名单中' % nickName, toUserName=self.userName)
        else:
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info='[%s]不在您的群名单中' % nickName)
            self.instance.send('失败！[%s]不在您的群名单中' % nickName, toUserName=self.userName)
    else:
        cmd = 'addReply %s' % nickName
        logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
        if nickName in [each['NickName'] for each in self.frdInfoList]:
            if nickName not in self.autoReplyGroup:  # 添加指定好友
                self.autoReplyGroup.append(nickName)
                self.mysqlHelper.update('users', 'autoReplyGroup', self.separator.join(self.autoReplyGroup), 'nickName', self.nickName)
                logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
                self.instance.send('成功！好友[%s]成功加入自动回复名单' % nickName, toUserName=self.userName)
            else:
                logging(self.errFile, self.nickName, infoType='err', other=cmd, info='好友[%s]已经在自动回复名单中' % nickName)
                self.instance.send('失败！好友[%s]已经在自动回复名单中' % nickName, toUserName=self.userName)
        elif nickName == 'all':  # 添加所有好友
            self.autoReplyGroup.extend([each['NickName'] for each in self.frdInfoList])
            self.autoReplyGroup = list(set(self.autoReplyGroup))
            self.mysqlHelper.update('users', 'autoReplyGroup', self.separator.join(self.autoReplyGroup), 'nickName',
                                    self.nickName)
            logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
            self.instance.send('成功！[所有好友]成功加入自动回复名单', toUserName=self.userName)
        else:  # 错误指令
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info='[%s]不在您的好友名单中' % nickName)
            self.instance.send('失败！[%s]不在您的好友名单中' % nickName, toUserName=self.userName)


def delReply(self, nickName, chatroom=None):  # 删除自动回复成员
    if chatroom:
        cmd = 'delReply %s chatroom' % nickName
        logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
        chatroomList = self.getChatrooms()
        if nickName in [each['NickName'] for each in chatroomList]:
            memberList = self.getChatroomMembers(nickName)['MemberList']
            friendsInChatroom = [each['NickName'] for each in memberList
                                 if each['NickName'] in [each['NickName']
                                                         for each in self.frdInfoList[1:]]]
            friendsInChatroom = [nickName for nickName in friendsInChatroom if nickName in self.autoReplyGroup]
            if friendsInChatroom:
                self.autoReplyGroup = list(set(friendsInChatroom)^set(self.autoReplyGroup))
                self.mysqlHelper.update('users', 'autoReplyGroup', self.separator.join(self.autoReplyGroup), 'nickName',
                                        self.nickName)
                logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
                self.instance.send('成功！群[%s]中的好友成功加入自动回复名单' % nickName, toUserName=self.userName)
            else:
                logging(self.errFile, self.nickName, infoType='err', other=cmd, info='群[%s]中的好友不在自动回复名单中' % nickName)
                self.instance.send('失败！群[%s]中的好友不在自动回复名单中' % nickName, toUserName=self.userName)
        else:
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info='[%s]不在您的群名单中' % nickName)
            self.instance.send('失败！[%s]不在您的群名单中' % nickName, toUserName=self.userName)
    else:
        cmd = 'delReply %s' % nickName
        logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
        if nickName in self.autoReplyGroup:  # 删除指定成员
            self.autoReplyGroup.remove(nickName)
            self.mysqlHelper.update('users', 'autoReplyGroup', self.separator.join(self.autoReplyGroup), 'nickName', self.nickName)
            self.instance.send('成功！好友[%s]从自动回复名单中删除' % nickName, toUserName=self.userName)
            logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
        elif nickName == 'all':  # 删除所有成员
            self.autoReplyGroup = []
            self.mysqlHelper.update('users', 'autoReplyGroup', self.separator.join(self.autoReplyGroup), 'nickName',
                                    self.nickName)
            self.instance.send('成功！[所有好友]从自动回复名单中删除', toUserName=self.userName)
            logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
        else:  # 错误指令
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info='好友[%s]不在自动回复名单中' % nickName)
            self.instance.send('失败！好友[%s]不在自动回复名单中' % nickName, toUserName=self.userName)


def autoReplyOn(self):  # 开启自动回复
    cmd = 'autoReplyOn'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    self.autoReply = 1
    self.mysqlHelper.update('users', 'autoReply', self.autoReply, 'nickName', self.nickName)
    self.instance.send('提示：已开启自动回复', toUserName=self.userName)
    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)


def autoReplyOff(self):  # 关闭自动回复
    cmd = 'autoReplyOff'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    self.autoReply = 0
    self.mysqlHelper.update('users', 'autoReply', self.autoReply, 'nickName', self.nickName)
    self.instance.send('提示：已关闭自动回复', toUserName=self.userName)
    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)


def getUserDict(self):
    cmd = 'getUserDict'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    usersInfo = [str(each) for each in self.mysqlHelper.getAll('users', 'nickName', 'userType')]
    reply = '当前注册用户：\n' + '\n'.join(usersInfo)
    self.instance.send(reply, toUserName=self.userName)
    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)


def userOnline(self):  # 获取当前在线用户
    cmd = 'userOnline'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    usersInfo = [str(each) for each in onlineDict.keys()]
    reply = '当前在线用户：\n' + '\n'.join(usersInfo)
    self.instance.send(reply, toUserName=self.userName)
    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)


def fileHelperOn(self):
    cmd = 'fileHelperOn'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    self.filehelper = 1
    self.mysqlHelper.update('users', 'filehelper', self.filehelper, 'nickName', self.nickName)
    self.instance.send('提示：文件传输助手已开启')
    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)


def fileHelperOff(self):
    cmd = 'fileHelperOff'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    self.filehelper = 0
    self.mysqlHelper.update('users', 'filehelper', self.filehelper, 'nickName', self.nickName)
    self.instance.send('提示：文件传输助手已关闭')
    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)

def autoSending(self):
    pass

def addTimerTask(self):
    pass

# TODO 可查找属性值放入config，由config配置
def getAttr(self, nickName, attr=None):  # 获取属性值
    cmd = 'getAttr-%s-%s' % (nickName, attr)
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    if attr:
        try:
            if nickName in onlineDict.keys():
                value = getattr(onlineDict[nickName], attr)
            else:
                value = self.mysqlHelper.getOne('users', 'nickName', nickName)[attr]
            logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
            self.instance.send('%s.%s = %s' % (nickName, attr, value))
        except Exception as reason:
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info=reason)
            self.instance.send('%s.%s属性不存在' % (nickName, attr))
    else:
        try:
            if nickName in onlineDict.keys():
                attrs = self.__dict__.keys()
                info = ''.join(['%s = %s\n' % (attr, getattr(onlineDict[nickName], attr)) for attr in attrs])
                # info = 'nickName   = %s\n' \
                #        'userType   = %s\n' \
                #        'autoLogin  = %s\n' \
                #        'autoReply  = %s\n' \
                #        'loading    = %s\n' \
                #        'online     = %s\n' \
                #        'receiveMsg = %s\n' \
                #        'uin   = %s\n' \
                #        'robotNickName  = %s\n' \
                #        'autoReplyGroup = %s\n' \
                #        'cmds       = %s' % (onlineDict[nickName].nickName, onlineDict[nickName].userType,
                #                             onlineDict[nickName].autoLogin, onlineDict[nickName].autoReply,
                #                             onlineDict[nickName].loading, onlineDict[nickName].online,
                #                             onlineDict[nickName].receiveMsg, onlineDict[nickName].uin,
                #                             onlineDict[nickName].robotNickName, onlineDict[nickName].autoReplyGroup,
                #                             onlineDict[nickName].cmds)
                print('users line 422 info =', info)
            else:
                userInfo       = self.mysqlHelper.getOne('users', 'nickName', nickName)
                userType       = userInfo['userType']
                autoLogin      = userInfo['autoLogin']
                autoReply      = userInfo['autoReply']
                autoReplyGroup = userInfo['autoReplyGroup']

                info = 'nickName   = %s\n' \
                       'userType   = %s\n' \
                       'autoLogin  = %s\n' \
                       'autoReply  = %s\n' \
                       'autoReplyGroup = %s' % (nickName, userType,
                                            autoLogin, autoReply,
                                            autoReplyGroup)
            self.instance.send(info, toUserName=self.userName)
        except Exception as reason:
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info=reason)


# TODO 好友列表在变动后自动更新
def updateFriendList(self, frdNickName):
    if frdNickName in self.frdList:
        userName = self.instance.search_friends(name=frdNickName)[0]['UserName']
        memberList = self.instance.update_friend(userName)
        print(memberList)
    else:
        print('没有这个好友')


# TODO 群列表在变动后自动更新
def updateChatroomList(self):
    pass

# ----------------------------------------------------------------
# 微信内部功能
# TODO
def checkFriendStatus(self, nickName):  # 好友检测
    cmd = 'checkFriendStatus %s' % nickName
    print('[%s][%s]执行命令：checkFriendStatus %s' % (datetime.datetime.now(), self.nickName, nickName))
    result = []
    testList = []
    chatroomUserName = self.instance.search_chatrooms(name='FriendStatusChatroom')[0]['UserName']
    if nickName == 'all':
        testList = self.frdInfoList[1:]
    elif nickName in [each['NickName'] for each in self.frdInfoList]:
        testList = self.instance.search_friends(name=nickName)
    else:
        print('[%s][%s]当前好友不在您的好友名单中: checkFriendStatus %s' % (datetime.datetime.now(), self.nickName, nickName))
        self.instance.send('当前好友不在您的好友名单中:%s' % nickName)
        return
    print('testList =', testList)
    for friend in testList:
        r = self.instance.add_member_into_chatroom(chatroomUserName, [friend])
        print('r =', r)
        # if r['BaseResponse']['ErrMsg'] == '':
        #     status = r['MemberList'][0]['MemberStatus']
        #     self.instance.delete_member_from_chatroom(chatroomUserName, friend)
        #     if status in [3, 4]:
        #         result.append((friend['NickName'], {3:'该好友已经将你加入黑名单。', 4:'该好友已经将你删除。'}.get(status)))

    print('[%s][%s]成功执行命令: checkFriendStatus %s' % (datetime.datetime.now(), self.nickName, nickName))
    print('result =', result)
    self.instance.send(str(result))


def mfRatio(self, chatroom=None):  # 男女比例
    male = female = othor = 0
    lables = ['男', '女', '其他']
    path = self.savedir + 'mfRatio.html'
    if chatroom:
        cmd = 'mfRatio %s' % chatroom
        logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
        try:
            chatroom == self.instance.search_chatrooms(name=chatroom)[0]['NickName']
        except Exception as reason:
            self.instance.send('在您的通讯录中没有找到该群[%s]' % chatroom)
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info=reason)
            return
        memberList = self.getChatroomMembers(chatroom)['MemberList']
        subtitle = self.nickName + ':' + chatroom
    else:
        cmd = 'mfRatio'
        logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
        memberList = self.frdInfoList[1:]
        subtitle = self.nickName
    male = len([1 for each in memberList if each['Sex']==1])
    female = len([2 for each in memberList if each['Sex'] == 2])
    other = len([0 for each in memberList if each['Sex'] == 0])
    values = [male, female, other]
    pie = pyecharts.Pie('微信好友男女比例', subtitle)
    pie.add('男女比例', lables, values, is_label_show=True)
    pie.render(path)
    self.instance.send('@fil@%s' % path)
    os.remove(path)
    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)


def signatureCloud(self, chatroom=None):  # 签名词云
    path = self.savedir + 'signatureCloud.html'
    if chatroom:
        cmd = 'signaturCloud %s' % chatroom
        logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
        try:
            chatroom == self.instance.search_chatrooms(name=chatroom)[0]['NickName']
        except Exception as reason:
            self.instance.send('在您的通讯录中没有找到该群[%s]' % chatroom)
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info=reason)
            return
        memberList = self.getChatroomMembers(chatroom)['MemberList']
        sigList = [each['Signature'] for each in memberList]
        subtitle = self.nickName + ':' +  chatroom
    else:
        cmd = 'signaturCloud'
        logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
        sigList = [each['Signature'] for each in self.frdInfoList]
        subtitle = self.nickName

    primaryList = re.findall('\w+', ' '.join(sigList))
    wordString = re.sub(r'emoji[\d\w]*|span|class', '', ' '.join(primaryList))
    finalList = [each for each in list(jieba.cut(wordString)) if len(each)>=2]
    words = list(set(finalList))
    amount = [finalList.count(each) for each in words]
    wordCloud = pyecharts.WordCloud('微信好友个性签名词云图', subtitle)
    shape = random.choice(['circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star'])
    wordCloud.add('', words, amount, word_size_range=[12-60], shape=shape)
    wordCloud.render(path)
    self.instance.send('@fil@%s' % path)
    os.remove(path)
    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)


def geoData(self, chatroom=None):
    path = self.savedir + 'geoData.html'
    if chatroom:
        cmd = 'geoData %s' % chatroom
        logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
        try:
            chatroom == self.instance.search_chatrooms(name=chatroom)[0]['NickName']
        except Exception as reason:
            self.instance.send('在您的通讯录中没有找到该群[%s]' % chatroom)
            logging(self.errFile, self.nickName, infoType='err', other=cmd, info=reason)
            return
        memberList = self.getChatroomMembers(chatroom)['MemberList']
        subtitle = self.nickName + ':' +  chatroom
    else:
        cmd = 'geoData'
        logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
        memberList = [each['Signature'] for each in self.frdInfoList]
        subtitle = self.nickName
    cities = [each['City'] for each in memberList]
    with open(os.path.dirname(os.path.abspath(__file__)) + '/city_coordinates.json', 'rb') as f:
        cityDict = json.load(f)
    data = [(each, cities.count(each)) for each in set(cities) if each in cityDict.keys()]
    geo = pyecharts.Geo('微信好友地理分布', subtitle, title_color="#fff", title_pos="center", background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add("", attr, value, visual_range=[0, 100], visual_text_color="#fff", symbol_size=10, is_visualmap=True)
    geo.render(path)
    self.instance.send('@fil@%s' % path)
    os.remove(path)
    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)


# TODO 查看多个群内的共同好友
def friendInChatrooms(self, chatroom):
    cmd = 'friendInChatrooms'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    chatroomList = self.getChatrooms()
    chatroomList = [each['NickName'] for each in chatroomList]
    if chatroom in chatroomList:
        chatroomMembers = self.getChatroomMembers(chatroom)
        chatroomMembers = [each['NickName'] for each in chatroomMembers['MemberList']]
        if not self.frdInfoList:
            self.frdInfoList = self.getFriends()
        frdList = [each['NickName'] for each in self.frdInfoList]
        intersection = set(chatroomMembers) & set(frdList)
        reply = '与您在同在群[%s]的好友有%d个：\n%s' % (chatroom, len(intersection), str(intersection))
        logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
    else:
        reply = '失败！群[%s]不在您的群列表中！' % chatroom
        logging(self.cmdFile, self.nickName, infoType='cmd', status='fail', other=cmd, info='群[%s]不在您的群列表中！' % chatroom)
    self.instance.send(reply)


# TODO 自动加群好友（似乎无法实现了，大概微信网页版已经关闭添加好友的权限了）
def autoAddFriendInChatroom(self, chatroom):
    chatroomMembers = self.getChatroomMembers(chatroom)
    userNames = [each['UserName'] for each in chatroomMembers['MemberList']]
    for userName in userNames:
        result = self.instance.add_friend(userName, status=2, verifyContent='', autoUpdate=True)
        print(result)
# ----------------------------------------------------------------
# 扩展功能
# TODO 关注股票信息自动提醒

# TODO 定时发送复习资料
def autoSending(self, fileName, group=[]):
    filePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/webServer/static/source/' + fileName
    print(filePath)
    if os.path.exists(filePath):
        msg = '本次复习内容：' + fileName.split('.')[0] + '\nhttp://182.61.60.153/source/' + fileName
        print(msg)
        if group:
            for userName in group:
                try:
                    self.instance.send(msg, userName)
                except:
                    self.instance.send('无法发送：%s' % userName)
        else:
            self.instance.send(msg)
        return True
    else:
        msg = '该文件不存在'
        return False


def schemeOfMemery(self, frequency, startTime=None):
    return self.schemeTimer.schemeOfMemery(frequency, startTime)

# 添加定时任务
def addTimerTask(self, taskType, taskName, *args, frequency=10, startTime=None, **kwargs):
    """
    在config文件中配置任务类型。
    :param self:
    :param taskType:
    :param taskName:
    :param args:
    :param frequency:
    :param startTime:
    :param kwargs:
    :return:
    """
    for each in CONFIG.taskRoute:
        if taskType == each[0]:
            func = getattr(self, each[1])
            scheme = getattr(self, each[2])(frequency, startTime)
            result = self.schemeTimer.addTask(taskName, scheme, func, *args, **kwargs)
            if result:
                msg = '任务添加成功'
                print('scheme:', scheme)
                self.instance.send('\n'.join([each.strftime('%Y-%m-%d %H:%M:%S') for each in scheme]))
        else:
            msg = '暂无此类型任务'
        self.instance.send(msg)


# ----------------------------------------------------------------
# 框架函数
def setDefault(self, nickName, userType):
    authoritys = getattr(CONFIG, 'authorityLv' + str(userType))
    for each in authoritys.keys():
        self.mysqlHelper.update('users', each, authoritys[each], 'nickName', nickName)


# TODO 数据库初始化
def MysqlInspect(self):
    # 检查数据表，若有则跳过，若无则新建
    result = self.mysqlHelper.execute('show tables')
    table_name = 'users'
    tableConf = {'users':'id int unsigned primary key auto_increment not null,' \
                 'uin int unsigned,' \
                 'nickName varchar(20) not null,' \
                 'userType tinyint not null default 3,' \
                 'filehelper bit not null default 0,' \
                 'autoLogin bit not null default 0,' \
                 'autoReply bit not null default 1,' \
                 'autoReplyGroup text'}
    if table_name in [each['Tables_in_' + CONFIG.connectionDict['db']] for each in result]:
        pass
    else:
        values = tableConf[table_name]
        self.mysqlHelper.addTable(table_name, values)
        self.mysqlHelper.insertOne(table_name, nickName=CONFIG.superAdmins[0], userType=0)

def lc(self):
    """
    登录时的回调函数，
    :param self:
    :return:
    """
    cmd = 'lc'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    print(datetime.datetime.now(), self.nickName, '成功登陆！')
    self.online  = True
    self.receiveMsg = True
    self.frdInfoList = self.getFriends()
    self.userName = self.frdInfoList[0]['UserName']
    self.schemeTimer.start()
    try:
        self.instance.send('登录成功')
    except Exception as e:
        self.instance.send('Error in users line 698, %s' % str(e))
        print('Error in users line 698', e)
    self.msgProcess()
    try:
        os.remove(os.getcwd() + r'/users/%s/QR.png' % self.nickName)
    except Exception as reason:
        pass
    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)


def ec(self):
    cmd = 'ec'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    self.logout()
    del onlineDict[self.nickName]
    print(datetime.datetime.now(), self.nickName, '成功退出！')
    logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)


def login(self):
    for eachdir in [self.savedir, self.cmdDir, self.chatDir, self.errDir, self.chatroomDir]:
        if not os.path.exists(eachdir):
            os.makedirs(eachdir)
    hotReload = True if self.autoLogin else False
    statusPath = self.savedir + '%s.pkl' % self.nickName
    qrCodePath = self.savedir + 'QR.png'
    self.instance.auto_login(hotReload=hotReload, statusStorageDir=statusPath,
                             picDir=qrCodePath, enableCmdQR=self.cmdQR, loginCallback=self.lc, exitCallback=self.ec)


def logout(self):
    self.instance.logout()


def run(self):
    self.instance.run(blockThread=False)


def getFriends(self):
    cmd = 'getFriends'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    if self.online:
        frdInfoList = self.instance.get_friends(update=True)
        self.frdList = [each['NickName'] for each in frdInfoList]
        logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
        return frdInfoList


def getChatrooms(self):
    cmd = 'getChatrooms'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    if self.online:
        chatroomList = self.instance.get_chatrooms(update=True)
        self.chatroomList = [each['NickName'] for each in chatroomList]
        logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
        return chatroomList


def getChatroomMembers(self, nickName, detailedMember=True):
    cmd = 'getChatroomMembers'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    if self.online:
        chatroomUserName = self.instance.search_chatrooms(name=nickName)[0]['UserName']
        chatroomMembers = self.instance.update_chatroom(chatroomUserName, detailedMember=detailedMember)
        self.chatroomMembers = [each['NickName'] for each in chatroomMembers['MemberList']]
        logging(self.cmdFile, self.nickName, infoType='cmd', status='success', other=cmd)
        return chatroomMembers


def getMps(self):
    cmd = 'getMps'
    logging(self.cmdFile, self.nickName, infoType='cmd', other=cmd)
    if self.online:
        logging(self.cmdFile, self.nickName, infoType='cmd', status='succes', other=cmd)
        return self.instance.get_mps(update=True)


def msgProcess(self):
    self.uin = self.frdInfoList[0]['Uin']
    try:
        robotInfo = self.instance.search_mps(name='小冰')  # 查找指定公众号信息
        self.robotUserName = robotInfo[0]['UserName']
        self.robotNickName = robotInfo[0]['NickName']
    except Exception as reason:
        self.robotUserName = self.userName
        self.robotNickName = '无'

    def forward(msg, toUserName):
        """
        转发消息
        """
        if msg['Type'] == TEXT:
            forwardedMsg = msg['Text']
        elif msg['Type'] in [PICTURE, RECORDING, ATTACHMENT, VIDEO]:
            # TODO 怎么转发语音，而不是语音文件
            msg['Text'](msg['FileName'])
            forwardedMsg = '@%s@%s' % (
                {'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), os.path.dirname(os.path.abspath(__file__)) + '/' + msg['FileName'])
        else:
            # TODO 其他格式信息的处理
            forwardedMsg = '我想要发给你一个%s\n%s' % (msg['Type'], msg['Text'])
        self.instance.send(forwardedMsg, toUserName=toUserName)
        try:
            os.remove( os.path.dirname(os.path.abspath(__file__)) + '/' + msg['FileName'])
        except:
            pass
        time.sleep(random.randint(1, 3))

    def replyCmd(cmd, cmds):  # 处理指令消息
        if cmd in cmds:  # 无参数指令
            getattr(self, cmd)()
        elif cmd.split(' ')[0] in cmds:  # 多参数指令
            cmd, *args = cmd.split(' ')
            getattr(self, cmd)(*args)
        else:
            pass

    @self.instance.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
    def replyFriendChat(msg):
        # TODO （1）处理自己给自己的消息
        if msg['FromUserName'] == msg['ToUserName'] == self.userName:  # 来自自己的消息
            if (msg['Type'] == TEXT) and (msg['Text'][0] == '*'):  # 处理命令消息，以*开头
                replyCmd(msg['Text'][1:], self.cmds)
            else:  # TODO 处理其他消息
                pass

        # TODO （2）处理好友发来的消息
        elif msg['FromUserName'] in [each['UserName'] for each in self.frdInfoList[1:]]: # 来自好友的消息
            logging(self.chatDir + '%s.txt' % msg['User']['NickName'], self.nickName, infoType='recv', other=msg['User']['NickName'], info=msg['Text'])
            if (msg['Type'] == TEXT) and (msg['Text'][0] == '*'):  # 处理远程指令消息，以*开头
                replyCmd(msg['Text'][1:], self.remoteCmds)
            else:
                if self.autoReply:  # 自动回复
                    if msg['User']['NickName'] in self.autoReplyGroup:
                        forward(msg, msg['User']['NickName'], self.robotNickName, self.robotUserName)
                        self.FTUserName = msg['FromUserName']
                        self.FTNickName = msg['User']['NickName']
                else:
                    pass

        # TODO （3）处理自己向其他好友发送的消息
        else:
            try:
                toNickName = self.instance.search_friends(userName=msg['ToUserName'])[0]['NickName']
                print(toNickName)
                logging(self.chatDir + '%s.txt' % toNickName, self.nickName, infoType='send', other=toNickName, info=msg['Text'])
            except Exception as reason:
                print('Error: replyFriendChat, reason:', reason)

    @self.instance.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO], isMpChat=True)
    def replyMpChat(msg):
        if msg['FromUserName'] == self.robotUserName:  # 来自AI的信息
            forward(msg, self.robotNickName, self.FTNickName, self.FTUserName)
            # TODO （3-1）处理转发消息的时效
            # self.FTUserName = self.userName
            # self.FTNickName = self.nickName
        else:  # 其他公众号发来的消息
            pass

    @self.instance.msg_register([TEXT], isGroupChat=True)
    def replyGroupChat(msg):
        if msg['FromUserName'] == self.userName:  # 自己发送的群消息
            logging(self.chatroomDir + '%s.txt' % msg['User']['NickName'], self.nickName, infoType='send', other=msg['ActualNickName'],
                    info='[%s]' % msg['User']['NickName'] + msg['Text'])
        else:  # 接收的群消息
            if msg['isAt']:  # 当有人@我的
                self.instance.send('谁在@我吖，我等会就来...', toUserName=msg['FromUserName'])
            try:
                logging(self.chatroomDir + '%s.txt' % msg['User']['NickName'], self.nickName, infoType='recv', other=msg['ActualNickName'],
                    info='[%s]' % msg['User']['NickName'] + msg['Text'])
            except Exception as reason:
                logging(self.errFile, self.nickName, infoType='err', info=reason)

    @self.instance.msg_register([SYSTEM])
    def replySystemChat(msg):  # 处理系统消息
        with open(self.savedir + 'sysMsg.txt', 'a') as sysMsg:
            output = '[%s]%s' % (datetime.datetime.now(), msg['Text'])
            print(output, file=sysMsg)

    @self.instance.msg_register([FRIENDS])
    def replyFriendApply(msg):
        # self.instance.add_friend(**msg['Text'])
        self.instance.send('有新的好友申请！请查收')

# ----------------------------------------------------------------
# 初始化
User.setDefault              = setDefault
User.MysqlInspect            = MysqlInspect
User.login                   = login
User.logout                  = logout
User.lc                      = lc
User.ec                      = ec
User.run                     = run
User.getFriends              = getFriends
User.updateFriendList        = updateFriendList
User.getChatrooms            = getChatrooms
User.updateChatroomList      = updateChatroomList
User.getChatroomMembers      = getChatroomMembers
User.getMps                  = getMps
User.msgProcess              = msgProcess

User.tips                    = tips
User.getAttr                 = getAttr
User.addUser                 = addUser
User.delUser                 = delUser
User.addReply                = addReply
User.delReply                = delReply
User.autoReplyOn             = autoReplyOn
User.autoReplyOff            = autoReplyOff
User.fileHelperOn            = fileHelperOn
User.fileHelperOff           = fileHelperOff
User.getUserDict             = getUserDict
User.userOnline              = userOnline

User.remoteLogin             = remoteLogin

User.checkFriendStatus        = checkFriendStatus
User.mfRatio                 = mfRatio
User.signatureCloud          = signatureCloud
User.geoData                 = geoData
User.friendInChatrooms       = friendInChatrooms
User.autoAddFriendInChatroom = autoAddFriendInChatroom
User.autoSending             = autoSending
User.addTimerTask            = addTimerTask
User.schemeOfMemery          = schemeOfMemery

#-----------------------------------------------------------------
# 当前在线用户
onlineDict = {}


