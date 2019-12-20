import inspect

from mysql.connector import Error

from dao.dao_abs import Dao

insert_sql = "Insert into product values(%s, %s)"
update_sql = "Update product set code=%s,name=%s where code=%s"
delete_sql = "Delete from product where code=%s"
select_sql = "Select code, name from product"
select_sql_where = select_sql + "where code = %s"


# alt + insert
class ProductDao(Dao):
    def insert_item(self, code=None, name=None):
        print("\n_____ {}() _____".format(inspect.stack()[0][3]))
        args = (code, name)
        try:
            super().do_query(query=insert_sql, kargs=args)
            return True
        except Error:
            return False

    def update_item(self, code=None, name=None, pdt_code=None):
        print("\n_____ {}() _____".format(inspect.stack()[0][3]))
        args = (code, name, pdt_code)
        try:
            self.do_query(query=update_sql, kargs=args)
            return True
        except Error:
            return False

    def delete_item(self, code=None):
        print("\n_____ {}() _____".format(inspect.stack()[0][3]))
        args = (code,)
        try:
            self.do_query(query=delete_sql, kargs=args)
            return True
        except Error:
            return False

    def select_item(self, code=None):
        print("\n_____ {}() _____".format(inspect.stack()[0][3]))
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql) if code is None else cursor.execute(select_sql_where, (code,))
            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            print(res)
            return res
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()