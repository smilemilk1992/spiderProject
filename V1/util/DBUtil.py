"""
数据库连接工具类
# """
import pymysql
import traceback
from DBUtils.PooledDB import PooledDB
from V1.setting import *

class MysqlUtil(object):
    # 获取setting文件中的配置
    config = {
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'database': MYSQL_DBNAME,
        'user': MYSQL_USER,
        'password': MYSQL_PASSWORD,
        'charset': MYSQL_CHARSET
    }

    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __pool = None

    def __init__(self):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        self._conn = MysqlUtil.get_conn()
        self._cursor = self._conn.cursor()

    # 获取链接
    @staticmethod
    def get_conn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if MysqlUtil.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=MysqlUtil.config['host'], port=MysqlUtil.config['port'], user=MysqlUtil.config['user'], passwd=MysqlUtil.config['password'], db=MysqlUtil.config['database'], charset=MysqlUtil.config['charset'])
        return __pool.connection()

    # 查询所有数据
    def get_all(self, sql, param=None):
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchall()
            else:
                result = False
            return result
        except Exception as e:
            traceback.print_exc(e)

    # 查询某一个数据
    def get_one(self, sql, param=None):
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchone()
            else:
                result = False
            return result
        except Exception as e:
            traceback.print_exc(e)

    # 查询数量
    def get_count(self, sql, param=None):
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            return count
        except Exception as e:
            traceback.print_exc(e)

    # 查询部分
    def get_many(self, sql, num, param=None):
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchmany(num)
            else:
                result = False
            return result
        except Exception as e:
            traceback.print_exc(e)

    # 插入一条数据
    def insert_one(self, sql, value=None):
        try:
            if value:
                self._cursor.execute(sql, value)
            else:
                self._cursor.execute(sql)
            return self._cursor.lastrowid
        except Exception as e:
            traceback.print_exc(e)
            self.end("rollback")

    # 插入多条数据
    def insert_many(self, sql, values):
        try:
            row_count = self._cursor.executemany(sql, values)
            return row_count
        except Exception as e:
            traceback.print_exc(e)
            self.end("rollback")

    # 执行sql,判断是否存在与否
    def query(self, sql, param=None):
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count=self._cursor.execute(sql, param)
            return count
        except Exception as e:
            traceback.print_exc(e)

    # 更新
    def update(self, sql, param=None):
        return self.query(sql, param)

    # 删除
    def delete(self, sql, param=None):

        return self.query(sql, param)

    def begin(self):
        self._conn.autocommit(0)

    def end(self, option='commit'):
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, is_end=1):
        if is_end == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()
