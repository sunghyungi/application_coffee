from dao.product_dao import ProductDao
from dao.sale_dao import SaleDao
from dao.sale_detail_dao import SaledetailDao
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QWidget, QTableWidgetItem, QAction


def view_table(table=None, data=None):
    table.setHorizontalHeaderLabels(data)
    # row 단위 선택
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    # 수정 불가능 하게
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # 균일한 간격으로 재배치
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


class coffeeUI(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/coffee_ui.ui")
        self.ui.show()
        self.table = view_table(table=self.ui.tableWidget, data=["code", "name"])
        self.table = view_table(table=self.ui.tableWidget_2, data=["no", "code", "price", "saleCnt", "marginRate"])
        self.table = view_table(table=self.ui.tableWidget_3, data=["no", "sale_price", "addTax", "supply_price", "marginPrice"])

        # product slot/signal
        self.ui.btn_insert.clicked.connect(self.insert_item)
        self.ui.btn_delete.clicked.connect(self.delete_item)
        self.ui.btn_update.clicked.connect(self.update_item)
        self.ui.btn_init.clicked.connect(self.init_item)

        # sale slot/signal
        self.ui.btn_insert_2.clicked.connect(self.insert_item2)
        self.ui.btn_delete_2.clicked.connect(self.delete_item2)
        self.ui.btn_update_2.clicked.connect(self.update_item2)
        self.ui.btn_init_2.clicked.connect(self.init_item2)

        # sale_detail slot/signal
        self.load_data3()
        self.ui.btn_init_3.clicked.connect(self.load_data3)
        self.ui.btn_procedure.clicked.connect(lambda stat, x=True:self.procedure(stat, x))
        self.ui.btn_procedure2.clicked.connect(lambda stat, x=False:self.procedure(stat, x))


        pdt = ProductDao()
        data = pdt.select_item()
        self.load_data(data)

        sale = SaleDao()
        data2 = sale.select_item()
        self.load_data2(data2)


        # 우클릭 선택
        self.set_context_menu(self.ui.tableWidget)
        self.set_context_menu2(self.ui.tableWidget_2)

    # product - tab1
    def set_context_menu(self, tv):
        tv.setContextMenuPolicy(Qt.ActionsContextMenu)
        choice_action = QAction("선택", tv)
        tv.addAction(choice_action)
        choice_action.triggered.connect(self.choice_item)

    def choice_item(self):
        selectionIdx = self.ui.tableWidget.selectedIndexes()[0]
        self.ui.le_code.setText(self.ui.tableWidget.item(selectionIdx.row(), 0).text())
        self.ui.le_name.setText(self.ui.tableWidget.item(selectionIdx.row(), 1).text())

    def get_item_form_le(self):
        code = self.ui.le_code.text()
        name = self.ui.le_name.text()
        item_code, item_name = self.create_item(code, name)

        return item_code, item_name, code, name

    def load_data(self, data):
        for idx, (code, name) in enumerate(data):
            item_code, item_name= self.create_item(code, name)
            nextIdx = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(nextIdx)
            self.ui.tableWidget.setItem(nextIdx, 0, item_code)
            self.ui.tableWidget.setItem(nextIdx, 1, item_name)

    def create_item(self, code, name):
        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)

        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        return item_code, item_name

    def insert_item(self):
        item_code, item_name, code, name = self.get_item_form_le()
        currentIdx = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(currentIdx)
        self.ui.tableWidget.setItem(currentIdx, 0, item_code)
        self.ui.tableWidget.setItem(currentIdx, 1, item_name)
        pdt = ProductDao()
        pdt.insert_item(code, name)
        self.init_item()

    def delete_item(self):
        pdt = ProductDao()
        selectionIdx = self.ui.tableWidget.selectedIndexes()[0]
        pdt_code = self.ui.tableWidget.item(selectionIdx.row(), 0).text()
        pdt.delete_item(code=pdt_code)
        self.ui.tableWidget.removeRow(selectionIdx.row())

    def update_item(self):
        pdt = ProductDao()
        selectionIdx = self.ui.tableWidget.selectedIndexes()[0]
        item_code, item_name, code, name = self.get_item_form_le()

        pdt_code = (self.ui.tableWidget.item(selectionIdx.row(), 0)).text()
        pdt.update_item(code, name, pdt_code)
        self.ui.tableWidget.setItem(selectionIdx.row(), 0, item_code)
        self.ui.tableWidget.setItem(selectionIdx.row(), 1, item_name)
        self.init_item()

    def init_item(self):
        self.ui.le_code.clear()
        self.ui.le_name.clear()

    # sale - tab2
    def set_context_menu2(self, tv):
        tv.setContextMenuPolicy(Qt.ActionsContextMenu)
        choice_action = QAction("선택", tv)
        tv.addAction(choice_action)
        choice_action.triggered.connect(self.choice_item2)

    def choice_item2(self):
        selectionIdx = self.ui.tableWidget_2.selectedIndexes()[0]
        self.ui.le_code_2.setText(self.ui.tableWidget_2.item(selectionIdx.row(), 1).text())
        self.ui.le_price.setText(self.ui.tableWidget_2.item(selectionIdx.row(), 2).text())
        self.ui.le_saleCnt.setText(self.ui.tableWidget_2.item(selectionIdx.row(), 3).text())
        self.ui.le_marginRate.setText(self.ui.tableWidget_2.item(selectionIdx.row(), 4).text())

    def get_item_form_le2(self):
        selectionIdx = self.ui.tableWidget_2.selectedIndexes()[0]
        no = (self.ui.tableWidget_2.item(selectionIdx.row(), 0)).text()
        code = self.ui.le_code_2.text()
        price = self.ui.le_price.text()
        saleCnt = self.ui.le_saleCnt.text()
        marginRate = self.ui.le_marginRate.text()
        item_no, item_code, item_price, item_saleCnt, item_marginRate \
            = self.create_item2(no, code, price, saleCnt, marginRate)

        return item_no, item_code, item_price, item_saleCnt, item_marginRate, no, code, price, saleCnt, marginRate

    def load_data2(self, data2):
        self.ui.tableWidget_2.setRowCount(0)
        for idx, (no, code, price, saleCnt, marginRate) in enumerate(data2):
            item_no, item_code, item_price, item_saleCnt, item_marginRate = self.create_item2(no, code, price, saleCnt, marginRate)
            nextIdx = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(nextIdx)
            self.ui.tableWidget_2.setItem(nextIdx, 0, item_no)
            self.ui.tableWidget_2.setItem(nextIdx, 1, item_code)
            self.ui.tableWidget_2.setItem(nextIdx, 2, item_price)
            self.ui.tableWidget_2.setItem(nextIdx, 3, item_saleCnt)
            self.ui.tableWidget_2.setItem(nextIdx, 4, item_marginRate)

    def create_item2(self, no, code, price, saleCnt, marginRate):
        item_no = QTableWidgetItem()
        item_no.setTextAlignment(Qt.AlignCenter)
        item_no.setData(Qt.DisplayRole, no)

        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)

        item_price = QTableWidgetItem()
        item_price.setTextAlignment(Qt.AlignCenter)
        item_price.setData(Qt.DisplayRole, price)

        item_saleCnt = QTableWidgetItem()
        item_saleCnt.setTextAlignment(Qt.AlignCenter)
        item_saleCnt.setData(Qt.DisplayRole, saleCnt)

        item_marginRate = QTableWidgetItem()
        item_marginRate.setTextAlignment(Qt.AlignCenter)
        item_marginRate.setData(Qt.DisplayRole, marginRate)

        return item_no, item_code, item_price, item_saleCnt, item_marginRate

    def insert_item2(self):
        item_no, item_code, item_price, item_saleCnt, item_marginRate, no, code, price, saleCnt, marginRate \
            = self.get_item_form_le2()

        sale = SaleDao()
        sale.insert_item(code, price, saleCnt, marginRate)
        self.init_item2()

        currentIdx = self.ui.tableWidget_2.rowCount()
        self.ui.tableWidget_2.insertRow(currentIdx)

        sale = SaleDao()
        data2 = sale.select_item()
        self.load_data2(data2)

    def delete_item2(self):
        sale = SaleDao()
        selectionIdx = self.ui.tableWidget_2.selectedIndexes()[0]
        sale_no = self.ui.tableWidget_2.item(selectionIdx.row(), 0).text()
        sale.delete_item(no=sale_no)
        self.ui.tableWidget_2.removeRow(selectionIdx.row())

    def update_item2(self):
        sale = SaleDao()
        selectionIdx = self.ui.tableWidget_2.selectedIndexes()[0]
        item_no, item_code, item_price, item_saleCnt, item_marginRate, no, code, price, saleCnt, marginRate = self.get_item_form_le2()


        sale.update_item(code, price, saleCnt, marginRate, no)
        self.ui.tableWidget_2.setItem(selectionIdx.row(), 0, item_no)
        self.ui.tableWidget_2.setItem(selectionIdx.row(), 1, item_code)
        self.ui.tableWidget_2.setItem(selectionIdx.row(), 2, item_price)
        self.ui.tableWidget_2.setItem(selectionIdx.row(), 3, item_saleCnt)
        self.ui.tableWidget_2.setItem(selectionIdx.row(), 4, item_marginRate)
        self.init_item2()

    def init_item2(self):
        self.ui.le_code_2.clear()
        self.ui.le_price.clear()
        self.ui.le_saleCnt.clear()
        self.ui.le_marginRate.clear()

    # sale_detail - tab3
    def load_data3(self):
        self.table = view_table(table=self.ui.tableWidget_3,
                                data=["no", "sale_price", "addTax", "supply_price", "marginPrice"])
        sdt = SaledetailDao()
        data3 = sdt.select_item()
        self.ui.tableWidget_3.setRowCount(0)
        self.ui.tableWidget_3.setColumnCount(5)
        for idx, (no, sale_price, addTax, supply_price, marginPrice) in enumerate(data3):
            item_no, item_sale_price, item_addTax, item_supply_price, item_marginPrice \
                = self.create_item2(no,  sale_price, addTax, supply_price, marginPrice)
            nextIdx = self.ui.tableWidget_3.rowCount()
            self.ui.tableWidget_3.insertRow(nextIdx)
            self.ui.tableWidget_3.setItem(nextIdx, 0, item_no)
            self.ui.tableWidget_3.setItem(nextIdx, 1, item_sale_price)
            self.ui.tableWidget_3.setItem(nextIdx, 2, item_addTax)
            self.ui.tableWidget_3.setItem(nextIdx, 3, item_supply_price)
            self.ui.tableWidget_3.setItem(nextIdx, 4, item_marginPrice)

    def procedure(self, stat, x):

        sdt = SaledetailDao()
        data = sdt.procedure(x)
        self.ui.tableWidget_3.setColumnCount(10)
        self.ui.tableWidget_3.setRowCount(0)
        self.table = view_table(table=self.ui.tableWidget_3,
                                data=["no", "code", "name", "price", "saleCnt", "supply_price", "addTax",
                                      "sale_price", "marginRate",  "marginPrice"])
        for idx, (no, code, name, price, saleCnt, supply_price, addTax, sale_price, marginRate, marginPrice)\
                in enumerate(data):
            item_no, item_code, item_name, item_price, item_saleCnt, item_supply_price, item_addTax, item_sale_price,\
                item_marginRate, item_marginPrice\
                = self.create_item3(no, code, name, price, saleCnt, supply_price, addTax, sale_price, marginRate, marginPrice)
            nextIdx = self.ui.tableWidget_3.rowCount()
            self.ui.tableWidget_3.insertRow(nextIdx)
            self.ui.tableWidget_3.setItem(nextIdx, 0, item_no)
            self.ui.tableWidget_3.setItem(nextIdx, 1, item_code)
            self.ui.tableWidget_3.setItem(nextIdx, 2, item_name)
            self.ui.tableWidget_3.setItem(nextIdx, 3, item_price)
            self.ui.tableWidget_3.setItem(nextIdx, 4, item_saleCnt)
            self.ui.tableWidget_3.setItem(nextIdx, 5, item_supply_price)
            self.ui.tableWidget_3.setItem(nextIdx, 6, item_addTax)
            self.ui.tableWidget_3.setItem(nextIdx, 7, item_sale_price)
            self.ui.tableWidget_3.setItem(nextIdx, 8, item_marginRate)
            self.ui.tableWidget_3.setItem(nextIdx, 9, item_marginPrice)

    def create_item3(self, no, code, name, price, saleCnt, supply_price, addTax, sale_price, marginRate, marginPrice):
        item_no = QTableWidgetItem()
        item_no.setTextAlignment(Qt.AlignCenter)
        item_no.setData(Qt.DisplayRole, no)

        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)

        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        item_price = QTableWidgetItem()
        item_price.setTextAlignment(Qt.AlignCenter)
        item_price.setData(Qt.DisplayRole, price)

        item_saleCnt = QTableWidgetItem()
        item_saleCnt.setTextAlignment(Qt.AlignCenter)
        item_saleCnt.setData(Qt.DisplayRole, saleCnt)

        item_supply_price = QTableWidgetItem()
        item_supply_price.setTextAlignment(Qt.AlignCenter)
        item_supply_price.setData(Qt.DisplayRole, supply_price)

        item_addTax = QTableWidgetItem()
        item_addTax.setTextAlignment(Qt.AlignCenter)
        item_addTax.setData(Qt.DisplayRole, addTax)

        item_sale_price = QTableWidgetItem()
        item_sale_price.setTextAlignment(Qt.AlignCenter)
        item_sale_price.setData(Qt.DisplayRole, sale_price)

        item_marginRate = QTableWidgetItem()
        item_marginRate.setTextAlignment(Qt.AlignCenter)
        item_marginRate.setData(Qt.DisplayRole, marginRate)

        item_marginPrice = QTableWidgetItem()
        item_marginPrice.setTextAlignment(Qt.AlignCenter)
        item_marginPrice.setData(Qt.DisplayRole, marginPrice)

        return item_no, item_code, item_name, item_price, item_saleCnt, item_supply_price, item_addTax,\
               item_sale_price, item_marginRate, item_marginPrice