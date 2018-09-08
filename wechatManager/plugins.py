# 多用户发送
# 单开一个线程，专门用来计时，到了某个时间点就将发送列表中的内容发送出去
import time
import datetime
import threading


class SchemeTimerThead(threading.Thread):
    """
    线程版
    自动执行程序，根据给定的程序，执行次数，开始执行时间，生成一个斐波那契序列时间表，到期按时间表自动执行。
    """
    def __init__(self):
        super().__init__()
        self.taskList = []
        self.pauseList = []
        self.taskNames = {}
        self.__pause = False
        self.__stop = False

    def timingCoroutine(self):
        """
        单开一个协程，专门用来计时，到了某个时间点就将发送列表中的内容发送出去
        self.taskList = [(time, func, [], {}))]
        :return:
        """
        print('定时器已开启')
        delta = datetime.timedelta(seconds=5)
        sumOfDone = 0
        while not self.__stop:
            doneList = []
            # 定义执行时间范围
            upper = datetime.datetime.now() + delta
            lower = datetime.datetime.now() - delta
            try:
                for each in self.taskList:
                    if lower < each[0] < upper:
                        # print('当前时间：', each[0])
                        # print('func:', each[1])
                        # print('args:', each[2])
                        # 产生任务协程
                        threading.Thread(target=each[1], args=(*each[2], )).start()
                        doneList.append(each)
                        # 统计已执行任务的数量
                        sumOfDone += len(doneList)
                        print('已执行任务数量：', sumOfDone)
                    elif each[0] < lower:
                        # 移除过时任务
                        self.taskList.remove(each)
                for each in doneList:
                    # 移除已经执行过的任务
                    self.taskList.remove(each)
            except:
                pass
            time.sleep(0.1)

    @staticmethod
    def schemeOfMemery(frequency, startTime=None):
        """
        生成一个斐波那契时间列表，默认起始时间为当前时间
        :param frequency: number，多少次
        :param startTime: '%Y-%m-%d %H:%M:%S'
        :return: scheme
        """
        startTime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S') if startTime else datetime.datetime.now()

        def fibonacci(n):
            a1 = 1
            a2 = 1
            for i in range(n):
                yield a1
                a1, a2 = a2, a1 + a2

        # 生成一个斐波那契序列
        frequency = fibonacci(frequency)
        interval = 0
        scheme = []
        for f in frequency:
            # 累加时间间隔
            interval += f
            scheme.append(startTime + datetime.timedelta(days=interval))
        return scheme

    def addTask(self, taskName, scheme, func, *args, **kwargs):
        """
        添加定时器任务：时间表，执行函数，函数参数
        """
        # 记录本次任务信息
        task = []
        if taskName in self.taskNames.keys():
            return
        for startTime in scheme:
            sub_task = (startTime, func, args, kwargs)
            self.taskList.append(sub_task)
            task.append(sub_task)
            # TODO 此处没有sleep会阻塞，其他地方加sleep都没用，为什么？
            time.sleep(0.1)
        self.taskNames[taskName] = task
        return taskName, task

    def run(self):
        self.__stop = False
        return self.timingCoroutine()

    def pause(self, task, status=True):
        '''
        暂停任务
        :param task:
        :param status:
        :return:
        '''
        self.__pause = status
        if self.__pause:
            for each in self.taskList:
                if each in task:
                    self.taskList.remove(each)
                    self.pauseList.append(each)
            return '任务暂停'
        else:
            for each in self.pauseList:
                if each in task:
                    self.pauseList.remove(each)
                    self.taskList.append(each)
            return '任务继续'

    def delete(self, taskName):
        '''
        删除任务
        :param taskName:
        :return:
        '''
        task = self.taskNames[taskName]
        for each in self.taskList:
            if each in task:
                self.taskList.remove(each)
        del self.taskNames[taskName]
        return '任务删除'

    def stop(self):
        self.__stop = True


# import gevent
# from gevent import monkey
# monkey.patch_all()
# class SchemeTimer(object):
#     """
#     协程版
#     自动执行程序，根据给定的程序，执行次数，开始执行时间，生成一个斐波那契序列时间表，到期按时间表自动执行。
#     """
#     def __init__(self):
#         self.taskList = []
#         self.pauseList = []
#         self.taskNames = {}
#         self.__pause = False
#         self.__stop = False
#
#     def timingCoroutine(self):
#         """
#         单开一个协程，专门用来计时，到了某个时间点就将发送列表中的内容发送出去
#         self.taskList = [(time, func, [], {}))]
#         :return:
#         """
#         delta = datetime.timedelta(seconds=5)
#         sumOfDone = 0
#         while not self.__stop:
#             doneList = []
#             # 定义执行时间范围
#             upper = datetime.datetime.now() + delta
#             lower = datetime.datetime.now() - delta
#             for each in self.taskList:
#                 if lower < each[0] < upper:
#                     # print('当前时间：', each[0])
#                     # print('func:', each[1])
#                     # print('args:', each[2])
#                     # 产生任务协程
#                     gevent.spawn(each[1], *each[2])
#                     doneList.append(each)
#                     # 统计已执行任务的数量
#                     sumOfDone += len(doneList)
#                     print('已执行任务数量：', sumOfDone)
#                 elif each[0] < lower:
#                     # 移除过时任务
#                     self.taskList.remove(each)
#             for each in doneList:
#                 # 移除已经执行过的任务
#                 self.taskList.remove(each)
#             time.sleep(0.1)
#
#     @staticmethod
#     def schemeOfMemery(frequency, startTime=None):
#         """
#         生成一个斐波那契时间列表，默认起始时间为当前时间
#         :param frequency: number，多少次
#         :param startTime: '%Y-%m-%d %H:%M:%S'
#         :return: scheme
#         """
#         startTime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S') if startTime else datetime.datetime.now()
#
#         def fibonacci(n):
#             a1 = 1
#             a2 = 1
#             for i in range(n):
#                 yield a1
#                 a1, a2 = a2, a1 + a2
#
#         # 生成一个斐波那契序列
#         frequency = fibonacci(frequency)
#         interval = 0
#         scheme = []
#         for f in frequency:
#             # 累加时间间隔
#             interval += f
#             scheme.append(startTime + datetime.timedelta(seconds=interval))
#         return scheme
#
#     def addTask(self, taskName, scheme, func, *args, **kwargs):
#         """
#         添加定时器任务：时间表，执行函数，函数参数
#         """
#         # 记录本次任务信息
#         task = []
#         for startTime in scheme:
#             sub_task = (startTime, func, args, kwargs)
#             self.taskList.append(sub_task)
#             task.append(sub_task)
#             # TODO 此处没有sleep会阻塞，其他地方加sleep都没用，为什么？
#             time.sleep(0.1)
#         self.taskNames[taskName] = task
#         return taskName, task
#
#     def start(self):
#         self.__stop = False
#         return self.timingCoroutine()
#
#     def pause(self, task, status=True):
#         """
#         暂停任务
#         :param task:
#         :param status:
#         :return:
#         """
#         self.__pause = status
#         if self.__pause:
#             for each in self.taskList:
#                 if each in task:
#                     self.taskList.remove(each)
#                     self.pauseList.append(each)
#             return '任务暂停'
#         else:
#             for each in self.pauseList:
#                 if each in task:
#                     self.pauseList.remove(each)
#                     self.taskList.append(each)
#             return '任务继续'
#
#     def delete(self, taskName):
#         """
#         删除任务
#         :param taskName:
#         :return:
#         """
#         task = self.taskNames[taskName]
#         for each in self.taskList:
#             if each in task:
#                 self.taskList.remove(each)
#         del self.taskNames[taskName]
#         return '任务删除'
#
#     def stop(self):
#         self.__stop = True



if __name__ == '__main__':
    def foo(*args, **kwargs):
        """测试函数"""
        print('-' * 50)
        print('foo1')
        print('foo Start')
        print('args:', args)
        print('kwargs:', kwargs)
        print('-' * 50 + '\r\n')


    def foo2(*args, **kwargs):
        """测试函数"""
        print('-' * 50)
        print('foo2')
        print('foo Start')
        print('args:', args)
        print('kwargs:', kwargs)
        print('-' * 50 + '\r\n')

    SchemeTimerThead().start()
    # 主线程开启
    # autoSending = SchemeTimer()
    # gevent.spawn(autoSending.start)
    # 远程添加任务
    # scheme = autoSending.schemeOfMemery(20)
    # autoSending.addTask('看书', scheme, foo2)
    # autoSending.addTask('锻炼', scheme, foo, 1, 2, 3)
    # while True:
    #     time.sleep(5)
    #     print('待执行任务数量：', len(autoSending.taskList))
    #     autoSending.pause(autoSending.taskNames['看书'])
