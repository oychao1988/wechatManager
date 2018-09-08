import logging

class BaseConfig(object):
    # 数据库配置
    charset = 'utf8mb4'
    connectionDict = dict(host='localhost',
                          port=3306,
                          user='root',
                          password='mysql',
                          db='wechatmanage',
                          charset=charset,
                          )

    # --------------------------------------------------------------------
    # 管理员
    superAdmins = ['superadmin']
    admins = []
    allAdmins = superAdmins + admins

    # --------------------------------------------------------------------
    # 用户类型
    """
    定义用户类型：
    0、超级管理员（superAdmin）
    1、管理员（admin）
    2、超级用户（superUser）
    3、普通用户（user）
    4、试用用户（freeTrailUser）
    """
    userTypes = [0, 1, 2, 3, 4]
    # 不同类型用户的默认属性
    authorityLv4 = {'autoReply': 1, 'filehelper': 1}
    authorityLv3 = {'autoLogin': 1}
    authorityLv2 = {}
    authorityLv1 = {}
    authorityLv0 = {}
    authorityLv3.update(authorityLv4)
    authorityLv2.update(authorityLv3)
    authorityLv1.update(authorityLv2)
    authorityLv0.update(authorityLv1)

    # --------------------------------------------------------------------
    # 来自自己的指令
    cmdsLv4 = ['tips']
    cmdsLv3 = ['addReply',
               'delReply',
               'autoReplyOn',
               'autoReplyOff',
               'fileHelperOn',
               'fileHelperOff',
               'mfRatio',
               'signatureCloud',
               'geoData',
               'checkFriendStatus',
               'getChatrooms',
               'getChatroomMembers',
               'getFriends',
               'updateFriendList',
               'updateChatroomList',
               'friendInChatrooms',
               'addTimerTask',
               ]
    cmdsLv2 = []
    cmdsLv1 = ['getAttr', 'addUser', 'delUser', 'getUserDict',
               'userOnline']
    cmdsLv0 = []
    cmdsLv3 += cmdsLv4
    cmdsLv2 += cmdsLv3
    cmdsLv1 += cmdsLv2
    cmdsLv0 += cmdsLv1

    # 来自好友的指令
    remoteCmdsLv4 = []
    remoteCmdsLv3 = [] + remoteCmdsLv4
    remoteCmdsLv2 = [] + remoteCmdsLv3
    remoteCmdsLv1 = ['remoteLogin'] + remoteCmdsLv2
    remoteCmdsLv0 = [] + remoteCmdsLv1

    # --------------------------------------------------------------------
    # TODO 多个AI

    # 日志文件类型：
    # 1、聊天记录
    chatDir = 'chatFile/'
    # 2、错误日志
    errDir = 'errFile/'
    # 3、日常指令
    cmdDir = 'cmdFile/'
    # 4、聊天室记录
    chatroomDir = 'chatroomFile/'

    # --------------------------------------------------------------------
    taskRoute = [('复习', 'autoSending', 'schemeOfMemery')]

    CMDQR = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    CMDQR = False
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(BaseConfig):
    DEBUG = False
    CMDQR = True
    LOG_LEVEL = logging.WARNING

configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}






