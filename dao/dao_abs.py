import inspect
from abc import ABCMeta, abstractmethod

from mysql.connector import Error

from db_connection.connection_pool_ import ConnectionPool


# 테이블 갯수가 2, 3개일 때는 추상클래스 이용 할 필요 없음, 많으면 필요
class Dao(metaclass=ABCMeta):
    def __init__(self):
        self.connection_pool = ConnectionPool.get_instance()

    @abstractmethod
    def insert_item(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def update_item(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def delete_item(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def select_item(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    def do_query(self, **kwargs):
        print("\n_____ {}() ______".format(inspect.stack()[0][3]))
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            if kwargs['kargs'] is not None:
                cursor.execute(kwargs['query'], kwargs['kargs'])
            else:
                cursor.execute(kwargs['query'])
            conn.commit()
        except Error as error:
            print(error)
            raise error
        finally:
            cursor.close()
            conn.close()

    def iter_row(self, cursor, size=5):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    def iter_row2(self, cursor):
        for result in cursor.stored_results():
            rows = result.fetchall()
            if not rows:
                break
            for row in rows:
                yield row