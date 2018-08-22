import datetime

infoTypes = ['send', 'recv', 'sys', 'cmd', 'err']
statuses = ['success', 'fail']


def logging(path, me, infoType=None, other=None, status=None, info=None):
    output = '[%s][%s][%s][%s][%s]：%s' % (
        datetime.datetime.now(), me, infoType, other, status, info)
    with open(path, 'a') as logFile:
        print(output, file=logFile)

# TODO 记录聊天记录
# [时间][用户]['send' or 'recv'][指令][指令状态]：消息

# TODO 记录错误日志
# [时间][用户]['err'][指令][None]：reason

# TODO 记录日常指令
# [时间][用户]['cmd'][指令][指令状态]：%s


if __name__ == '__main__':
    path = r'C:\Users\oychao\Desktop\out.txt'
    me = '欧阳超'
    infoType = 'send'
    other = 'system'
    info = '测试一下'
    logging(path, me, infoType, other, info)
