from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox

from sql.coffee_sql import coffeeUI


class login(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/login.ui")
        self.ui.show()

        self.ui.btn_login.clicked.connect(self.coffee_show)

    def coffee_show(self):
        if self.ui.le_ID.text() == "root":
            if self.ui.le_Password.text() == "rootroot":
                w = coffeeUI()
                self.ui = uic.loadUi("ui/coffee_ui.ui")
            else:
                QMessageBox.information(self, "로그인에러", "비밀번호가 틀렸습니다.", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "로그인에러", "아이디가 틀렸습니다.", QMessageBox.Ok)

