import inspect

from mysql.connector import Error

from dao.dao_abs import Dao

select_sql = "Select no, sale_price, addTax, supply_price, marginPrice from sale_detail"


# alt + insert
class SaledetailDao(Dao):

    def select_item(self):
        print("\n_____ {}() _____".format(inspect.stack()[0][3]))
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql)
            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            print(res)
            return res
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def update_item(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    def delete_item(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    def insert_item(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    def procedure(self, x):
        print("\n_____ {}() _____".format(inspect.stack()[0][3]))
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.callproc("proc_saledetail_orderby", [x,])
            res = []
            [res.append(row) for row in self.iter_row2(cursor)]
            print(res)
            return res
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

