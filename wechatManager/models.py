import pymysql


class MysqlHelper:
    def __init__(self, connectionDict):
        self.connectionDict = connectionDict

    def connectDB(self):
        self.connection = pymysql.connect(**self.connectionDict)
        self.cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)

    def closeDB(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def configuration(func):
        def inner(self, *args, **kwargs):
            self.connectDB()
            result = func(self, *args, **kwargs)
            self.closeDB()
            return result
        return inner

    @configuration
    def execute(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    @configuration
    def createDB(self):
        pass

    @configuration
    # TODO 添加数据表
    def addTable(self, table_name, values):
        sql = "create table %s (%s)" % (table_name, values)
        return self.cursor.execute(sql)

    @configuration
    def getOne(self, table, column, value):
        sql = "select * from %s where %s='%s'" % (table, column, value)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    @configuration
    def getAll(self, table, *args):
        columns = ','.join(args)
        sql = 'select %s from %s' % (columns, table)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    @configuration
    def insertOne(self, table, **kwargs):
        columns = ', '.join(kwargs.keys())
        values = ', '.join(["'%s'" % kwargs[each] for each in kwargs])
        sql = 'insert %s(%s) values(%s)' % (table, columns, values)
        reCount = self.cursor.execute(sql)
        return reCount

    @configuration
    def insertMany(self):
        pass

    @configuration
    def alter(self, table, method, *args):
        columnInfo = ','.join(args)
        try:
            if method in ['add', 'change', 'drop', 'rename']:
                sql = "alter table %s %s %s" % (table, method, columnInfo)
                reCount = self.cursor.execute(sql)
                return reCount
            else:
                print('Error:不存在[%s]方法' % method)
        except Exception as reason:
            print('Error:', reason)

    @configuration
    def delete(self, table, column, value):
        sql = "delete from %s where %s='%s'" % (table, column, value)
        reCount = self.cursor.execute(sql)
        return reCount

    @configuration
    def dropTable(self):
        pass

    @configuration
    def update(self, table, column, cValue, axisColumn, axisValue):
        sql = "update %s set %s='%s' where %s='%s'" % (table, column, cValue, axisColumn, axisValue)
        reCount = self.cursor.execute(sql)
        return  reCount


#-------------------------------------------------------------------
if __name__ == '__main__':
    connectionDict = dict(host='localhost',
                          port=3306,
                          user='root',
                          password='mysql',
                          db='wechatMamage',
                          charset='utf8',
                          )
    mysqlHelper = MysqlHelper(connectionDict)
    # mysqlHelper.insertOne('users', nickName='admin', userType=0)
    # mysqlHelper.insertOne('users', nickName='user.', userType=3)
    result = mysqlHelper.getOne('users', column='nickName', value='admin')
    print('getOne:', result)
    result = mysqlHelper.getAll('users', 'nickName', 'userType')
    print('getAll:', result)

    result = mysqlHelper.execute('show tables')

    print('result =', result)
    table_name = 'users'
    tableConf = {'users':'id int unsigned primary key auto_increment not null,' \
                 'uin int unsigned,' \
                 'nickName varchar(20) not null,' \
                 'userType tinyint not null default 3,' \
                 'filehelper bit not null default 0,' \
                 'autoLogin bit not null default 0,' \
                 'autoReply bit not null default 1,' \
                 'autoReplyGroup text'}
    if table_name in [each['Tables_in_wechat'] for each in result]:
        print('True')
    else:
        values = tableConf[table_name]
        mysqlHelper.addTable(table_name, values)

