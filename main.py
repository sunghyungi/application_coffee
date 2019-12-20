
from PyQt5.QtWidgets import QApplication

from db_connection.connection_pool_ import ConnectionPool
from sql.login import login

if __name__ == "__main__":
    pool = ConnectionPool.get_instance()
    connection = pool.get_connection()

    app = QApplication([])
    w = login()
    app.exec_()
