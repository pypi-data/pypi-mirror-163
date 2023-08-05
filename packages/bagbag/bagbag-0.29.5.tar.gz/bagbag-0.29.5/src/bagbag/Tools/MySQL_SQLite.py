from __future__ import annotations

from . import orator
from .Lock import Lock
import bagbag

class MySQLSQLiteTable():
    def __init__(self, db: MySQLSQLiteBase, schema: orator.Schema, tbname: str):
        """
        This function initializes the class with the database, schema, and table name
        
        :param db: The database object
        :type db: MySQLSQLiteBase
        :param schema: orator.Schema
        :type schema: orator.Schema
        :param tbname: The name of the table you want to use
        :type tbname: str
        """
        self.db = db
        self.schema = schema
        self.tbname = ''.join(list(map(lambda x: x if x in "_qazwsxedcrfvtgbyhnujmikolopQAZWSXEDCRFVTGBYHNUJMIKOLP0123456789" else "_", tbname)))
        self.table = self.db.db.table(self.tbname)
        self.data = {}

    def AddColumn(self, colname: str, coltype: str, default=None, nullable:bool = True) -> MySQLSQLiteTable:
        """
        :param colname: The name of the column to add
        :type colname: str
        :param coltype: int, string, float, text
        :type coltype: str
        :param default: The default value for the column
        :param nullable: Whether the column can be null, defaults to True
        :type nullable: bool (optional)
        """
        if self.schema.has_table(self.tbname):
            with self.schema.table(self.tbname) as table:
                exists = self.schema.has_column(self.tbname, colname)
        
                if coltype == "int":
                    col = table.big_integer(colname)
                elif coltype == "string":
                    col = table.string(colname, 256)
                elif coltype == "float":
                    col = table.double(colname)
                elif coltype == "text":
                    col = table.long_text(colname)
                else:
                    raise Exception("列的类型可选为: int, string, float, text")
                
                if default:
                    col.default(default)
                
                if nullable:
                    col.nullable()
                
                if exists:
                    col.change()
        else:
            with self.schema.create(self.tbname) as table:
                table.increments('id')

                if coltype == "int":
                    col = table.big_integer(colname)
                elif coltype == "string":
                    col = table.string(colname, 256)
                elif coltype == "float":
                    col = table.double(colname)
                elif coltype == "text":
                    col = table.long_text(colname)
                else:
                    raise Exception("列的类型可选为: int, string, float, text")
                
                if default:
                    col.default(default)
                
                if nullable:
                    col.nullable()

        return self
    
    def AddIndex(self, *cols: str) -> MySQLSQLiteTable:
        """
        It adds an index to the table
        
        :param : `tbname`: The name of the table
        :type : str
        :return: The table object itself.
        """
        try:
            with self.schema.table(self.tbname) as table:
                table.index(*cols)
        except Exception as e:
            if "Duplicate key name" not in str(e):
                raise e

        return self
    
    def wrap(func): # func是被包装的函数
        def ware(self, *args, **kwargs): # self是类的实例
            if self.db.driver == "mysql":
                try:
                    res = func(self, *args, **kwargs)
                except bagbag.Tools.orator.exceptions.query.QueryException as e:
                    # MySQL驱动默认不允许一个连接跨多个线程, 重连就行
                    self.db.db.reconnect()
                    res = func(self, *args, **kwargs)

            elif self.db.driver == "sqlite":
                # SQLite驱动默认不允许一个连接跨多个线程
                # 在连接的时候禁止了同线程的检测, 所以自己这里要保证同时只有一个线程在操作数据库
                self.db.lock.Acquire()
                res = func(self, *args, **kwargs)
                self.db.lock.Release()

            return res

        return ware
    
    def Fields(self, *cols: str) -> MySQLSQLiteTable:
        self.table = self.table.select(*cols)
        return self
    
    def Where(self, key:str, opera:str, value:str) -> MySQLSQLiteTable:
        self.table = self.table.where(key, opera, value)
        return self
    
    def WhereIn(self, key:str, value: list) -> MySQLSQLiteTable:
        self.table = self.table.where_in(key, value)
        return self 

    def WhereNotIn(self, key:str, value: list) -> MySQLSQLiteTable:
        self.table = self.table.where_not_in(key, value)
        return self

    def WhereNull(self, key:str) -> MySQLSQLiteTable:
        self.table = self.table.where_null(key)
        return self 
        
    def WhereNotNull_WillNotImplement(self, key:str):
        raise Exception("上游未实现，自己写SQL吧")

    def OrWhere(self, key:str, opera:str, value:str) -> MySQLSQLiteTable:
        self.table = self.table.or_where(key, opera, value)
        return self 

    def OrWhereIn_WillNotImplement(self, key:str, value: list):
        raise Exception("上游未实现，自己写SQL吧")

    def OrderBy(self, *key:str) -> MySQLSQLiteTable:
        self.table = self.table.order_by(*key)
        return self 

    def Limit(self, num:int) -> MySQLSQLiteTable:
        self.table = self.table.limit(num)
        return self 

    def Paginate(self, size:int, page:int) -> MySQLSQLiteTable:
        self.table = self.table.simple_paginate(size, page)
        return self 

    def Data(self, value:map) -> MySQLSQLiteTable:
        self.data = value
        return self 

    def Offset(self, num:int) -> MySQLSQLiteTable:
        self.table = self.table.offset(num)
        return self 

    @wrap
    def Insert(self):
        self.table.insert(self.data)
        self.data = {}
        self.table = self.db.db.table(self.tbname)

    @wrap
    def Update(self):
        self.table.update(self.data)
        self.table = self.db.db.table(self.tbname) 

    @wrap
    def Delete(self):
        self.table.delete()
        self.table = self.db.db.table(self.tbname)

    @wrap
    def InsertGetID(self) -> int:
        id = self.table.insert_get_id(self.data)
        self.data = {}
        self.table = self.db.db.table(self.tbname)

        return id

    def Exists(self) -> bool: 
        exists = False
        if self.First():
            exists = True

        return exists

    @wrap
    def Count(self) -> int:
        count = self.table.count()
        self.table = self.db.db.table(self.tbname)
        return count

    @wrap
    def Find(self, id:int) -> map:
        res = self.db.db.table(self.tbname).where('id', "=", id).first()
        
        return res

    @wrap
    def First(self) -> map: 
        """
        :return: A map of the first row in the table. Return None if the table is empty. 
        """
        res = self.table.first()
        self.table = self.db.db.table(self.tbname)
        return res

    @wrap
    def Get(self) -> list:
        """
        It gets the data from the table and then resets the table
        len(result) == 0 if the result set is empty.

        :return: A list of dictionaries.
        """
        res = self.table.get()
        self.table = self.db.db.table(self.tbname)
        return res

    def Columns(self) -> list[map]:
        """
        It returns a list of dictionaries, each dictionary containing the name and type of a column in a
        table
        :return: A list of dictionaries.
        """
        res = []
        if self.db.driver == "mysql":
            for i in self.db.Execute("SHOW COLUMNS FROM `"+self.tbname+"`"):
                res.append({'name': i["Field"], 'type': i["Type"]})
        elif self.db.driver == "sqlite":
            for i in self.db.db.select("PRAGMA table_info(`"+self.tbname+"`);"):
                res.append({'name': i["name"], 'type': i["type"]})
        return res

# > The class is a base class for MySQL and SQLite
class MySQLSQLiteBase():
    def Table(self, tbname: str) -> MySQLSQLiteTable:
        return MySQLSQLiteTable(self, self.schema, tbname)

    def Execute(self, sql: str) -> (bool | int | list):
        """
        :param sql: The SQL statement to execute
        :type sql: str
        """
        action = sql.split()[0].lower() 

        try:
            if action == "insert":
                res = self.db.insert(sql)
            elif action in ["select", "show"]:
                res = self.db.select(sql)
            elif action == "update":
                res = self.db.update(sql)
            elif action == "delete":
                res = self.db.delete(sql)
            else:
                res = self.db.statement(sql)
        except orator.exceptions.query.QueryException as e:
            if self.db.driver == "mysql":
                if action == "insert":
                    res = self.db.insert(sql)
                elif action in ["select", "show"]:
                    res = self.db.select(sql)
                elif action == "update":
                    res = self.db.update(sql)
                elif action == "delete":
                    res = self.db.delete(sql)
                else:
                    res = self.db.statement(sql)
            else:
                raise e
                
        return res

    def Tables(self) -> list:
        """
        It returns a list of all the tables in the database
        :return: A list of tables in the database.
        """
        res = []
        if self.driver == "mysql":
            tbs = self.Execute("show tables;")
        elif self.driver == "sqlite":
            tbs = self.Execute("SELECT `name` FROM sqlite_master WHERE type='table';")
        for i in tbs:
            for k in i:
                res.append(i[k])
        return res
    
    def Close(self):
        self.db.disconnect()

# > This class is a wrapper for the orator library, which is a wrapper for the mysqlclient library,
# which is a wrapper for the MySQL C API
class MySQL(MySQLSQLiteBase):
    def __init__(self, host: str, port: int, user: str, password: str, database: str, prefix:str = ""):
        """
        This function creates a database connection using the orator library
        
        :param host: The hostname of the database you are connecting to. (localhost)
        :type host: str
        :param port: The port number to connect to the database
        :type port: int
        :param user: The username to connect to the database with
        :type user: str
        :param password: The password for the user you're connecting with
        :type password: str
        :param database: The name of the database you want to connect to
        :type database: str
        :param prefix: The prefix for the table names
        :type prefix: str
        """
        config = {
            'mysql': {
                'driver': 'mysql',
                'host': host,
                'database': database,
                'user': user,
                'password': password,
                'prefix': prefix,
                'port': port,
            }
        }
        self.db = orator.DatabaseManager(config)
        self.schema = orator.Schema(self.db)
        self.driver = "mysql"
    
# > This class is a wrapper for the orator library, which is a wrapper for the sqlite3 library
class SQLite(MySQLSQLiteBase):
    def __init__(self, path:str=":memory:", prefix:str = ""):
        """
        :param path: The path to the database file
        :type path: str
        :param prefix: The prefix to use for the table names
        :type prefix: str
        """
        config = {
            'sqlite': {
                'driver': 'sqlite',
                'database': path,
                'prefix': '',
                'check_same_thread': False, # 会被传入到SQLite的驱动作为参数
            }
        }
        self.db = orator.DatabaseManager(config)
        self.schema = orator.Schema(self.db)
        self.driver = "sqlite"
        self.lock = Lock()

if __name__ == "__main__":
    # db = SQLite("data.db")
    # tbl = db.Table("test_tbl").AddColumn("string", "string").AddColumn("int", "string").AddIndex("int")
    # tbl.Data({"string":"string2", "int": 2}).Insert()
    # c = tbl.Where("string", "=", "string2").Count()
    # print(c)

    # db.Close()

    # import os 
    # os.unlink("data.db")

    # print(db.Table("test_tbl").First())

    db = MySQL("192.168.168.5", 3306, "root", "r", "test")

    for row in db.Table("__queue__name__name").Get():
        print(row)

    print(db.Table("__queue__name__name").Columns())
