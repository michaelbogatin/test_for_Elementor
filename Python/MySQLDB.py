import pymysql

from pandas import DataFrame

class MySQLDB:

    _connection : pymysql.Connection = None
    _database: str = ''
    _table_name: str = ''

    def __init__(self, conf: dict):
        # _connection = mysql.connector.connect(**conf)
        self._connection = pymysql.connect(host=conf['host'],
                                      port=conf['port'],
                                      user=conf['user'],
                                      password=conf['password'],
                                      db=conf['database'],
                                      cursorclass=pymysql.cursors.DictCursor)
        self._database = conf['database']
        self._table_name = conf['table_name']
        self._connection.open()

    def get_connection(self):
        return self._connection

    def add_to_db(self, df: DataFrame):
        df.to_sql(name= self._table_name, con= self.get_connection(), schema= self._database,
                chunksize= 1000,
                if_exists= "append")

    def execute_select(self, sql: str):
        pass

    def close(self):
        _connection.close()
