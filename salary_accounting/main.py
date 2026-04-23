import sys
import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QHeaderView, QMessageBox, QListWidgetItem, QListWidget, QTableView,
                               QDoubleSpinBox, QPushButton, QLabel)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QTextCursor
from PySide6.QtCore import Qt
from main_ui import Ui_MainWindow
from sqlalchemy import create_engine, select, update, insert, func, and_, or_
from sqlalchemy.orm import sessionmaker
from models import Base, Users, Payments
import os

# from SalaryAccounting import UserAdd
from Log import Log

class AppWindow(QMainWindow, Ui_MainWindow):
    selected_id = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        log_object = Log('user_module.log')  #, self.textBrowser_1)
        self.log = lambda t: log_object.log(t)
        log_object_p = Log('payment_module.log', self.textBrowser_2)
        self.log_p = lambda t: log_object_p.log(t)

        # self.Payment_doubleSpinBox.setMinimum(-99999999)
        self.ResetSelect_button.setToolTip('Обнулить значения полей')
        self.ResetSelection_pushButton.setToolTip('Снять выделение')
        # self.Log_1_button.setToolTip('Открыть логи')
        self.Log_2_button.setToolTip('Открыть логи')
        # self.Log_1_button.clicked.connect(lambda _: os.startfile('user_module.log'))
        self.Log_2_button.clicked.connect(lambda _: os.startfile('payment_module.log'))

        self.Users_comboBox.currentTextChanged.connect(self.select_user)

        self.Search_button.clicked.connect(self.find_user)
        self.Search_lineEdit.returnPressed.connect(self.find_user)
        self.ClearSearchLine_button.clicked.connect(self.clear_search)

        today = datetime.date.today()
        self.SelectPaymentsSince_dateEdit.setDate(today)
        self.SelectPaymentsTo_dateEdit.setDate(today)
        self.TotalSelectPaymentsSince_dateEdit.setDate(today)
        self.TotalSelectPaymentsTo_dateEdit.setDate(today)

        # self.ResetSelect_button.clicked.connect(self.UsersAddPayment_listWidget.clearSelection)
        self.ResetSelect_button.clicked.connect(self.reset_payment_values)
        self.ResetSelection_pushButton.clicked.connect(self.SelectUsers_listWidget.clearSelection)

        self.UpdateusersCB_button.clicked.connect(self.update_users_lists)
        self.UserAdd_button.clicked.connect(self.create_new_user)
        self.UpdateUser_button.clicked.connect(
            lambda _: self.confirmed_message_box('Изменение данных', 'Сохранить изменённое ФИО у пользователя?',
                                                 self.update_user_info))
        self.DeleteUser_button.clicked.connect(
            lambda _: self.confirmed_message_box('Удаление данных', 'Удалить выбранного пользователя?',
                                                 self.del_user))

        self.engine = create_engine(fr'sqlite:///{os.getcwd()}\data.db')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(self.engine)

        # self.user_model = QStandardItemModel()
        # self.user_model.setHorizontalHeaderLabels(['id', 'ФИО', 'Добавлен'])
        # self.Users_tableView.setModel(self.user_model)
        # self.Users_tableView.verticalHeader().hide()
        # self.Users_tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        # self.Users_tableView.setColumnWidth(0, 70)
        # self.Users_tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # ResizeToContents
        # self.Users_tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        # self.Users_tableView.setEditTriggers(QTableView.NoEditTriggers)

        self.payment_model = QStandardItemModel()
        self.payment_model.setHorizontalHeaderLabels(['id', 'Выплата', 'Время'])
        self.Payments_tableView.setModel(self.payment_model)
        self.Payments_tableView.verticalHeader().hide()
        # self.Payments_tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        # self.Payments_tableView.setColumnWidth(0, 70)
        self.Payments_tableView.setColumnHidden(0, True)
        self.Payments_tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # ResizeToContents
        self.Payments_tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.Payments_tableView.setEditTriggers(QTableView.NoEditTriggers)

        # self.Payments_tableView.clicked.connect(lambda i: self.PaumentID_spinBox.setValue(int(self.payment_model.item(i.row(), 0).text())))
        # s = self.Payments_tableView.selectionModel()
        # s.selectionChanged.connect(lambda x: print(x))

        self.add_payment_model = QStandardItemModel()
        self.add_payment_model.setHorizontalHeaderLabels(['id', 'ФИО', 'Выплата'])
        self.AddPayments_tableView.setModel(self.add_payment_model)
        self.AddPayments_tableView.verticalHeader().hide()
        # self.AddPayments_tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        # self.AddPayments_tableView.setColumnWidth(0, 70)
        self.AddPayments_tableView.setColumnHidden(0, True)
        self.AddPayments_tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # ResizeToContents
        self.AddPayments_tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.AddPayments_tableView.setEditTriggers(QTableView.NoEditTriggers)


        self.total_pay_model = QStandardItemModel()
        self.total_pay_model.setHorizontalHeaderLabels(['id', 'ФИО', 'Выплата', 'Время', 'Действие'])
        self.TotalPayments_tableView.setModel(self.total_pay_model)
        self.TotalPayments_tableView.verticalHeader().hide()
        # self.TotalPayments_tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        # self.TotalPayments_tableView.setColumnWidth(0, 70)
        self.TotalPayments_tableView.setColumnHidden(0, True)
        self.TotalPayments_tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # ResizeToContents
        # self.TotalPayments_tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.TotalPayments_tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.TotalPayments_tableView.setColumnWidth(2, 100)
        self.TotalPayments_tableView.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.TotalPayments_tableView.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.TotalPayments_tableView.setColumnWidth(4, 100)
        self.TotalPayments_tableView.setEditTriggers(QTableView.NoEditTriggers)

        # self.TotalPayments_tableView.clicked.connect(lambda i: print(self.total_pay_model.item(i.row(), 0).text()))
        self.TotalPayments_tableView.clicked.connect(lambda ind: self.change_payment(ind))


        self.SelectUsers_listWidget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.SelectUsers_listWidget.itemSelectionChanged.connect(lambda: self.SelectionCount_label.setText(
            f"Выбрано: {len(self.SelectUsers_listWidget.selectedItems())}"))
        # self.UsersAddPayment_listWidget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        # self.UsersAddPayment_listWidget.itemSelectionChanged.connect(lambda: self.SelectedCount_label.setText(
        #     f"Выбрано: {len(self.UsersAddPayment_listWidget.selectedItems())}"))

        self.AddPayment_button.clicked.connect(self.add_payment)
        # self.DelPayment_button.clicked.connect(self.del_payment)
        self.ShowPayments_button.clicked.connect(lambda: self.select_user(self.Users_comboBox.currentText()))
        self.SetLastPayment_button.clicked.connect(self.set_last_payment)

        self.TotalShowPayments_button.clicked.connect(self.load_total_payments)

        self.update_users_lists()


    def find_user(self):
        if self.Search_lineEdit.text() == '':
            self.update_users_lists()
            return

        self.Users_comboBox.clear()
        self.Users_comboBox.addItem('Выберите пользователя')
        with self.session() as sess:
            res = sess.execute(select(Users)).scalars()
            cnt = 0
            for u in res:
                if self.Search_lineEdit.text().lower() in str(u.name).lower():
                    self.Users_comboBox.addItem(f"{u.name}")  # [{u.id}]
                    cnt += 1

            self.UserCount_label.setText(f"{cnt}")

    def clear_search(self):
        self.Search_lineEdit.setText('')
        self.update_users_lists()

    def update_users_lists(self):
        self.Users_comboBox.clear()
        self.SelectUsers_listWidget.clear()

        # while self.user_model.rowCount() > 0:
        #     self.user_model.removeRow(self.user_model.rowCount()-1)
        while self.add_payment_model.rowCount() > 0:
            self.add_payment_model.removeRow(self.add_payment_model.rowCount()-1)

        self.Users_comboBox.addItem('Выберите пользователя')
        with self.session() as sess:
            res = sess.execute(select(Users).order_by(Users.name)).scalars()#.where(Users.id > 19))
            cnt = 0
            for u in res:
                self.Users_comboBox.addItem(f"{u.name}")  # [{u.id}]
                # item = [QStandardItem(str(i)) for i in [u.id, u.name, u.created_at]]
                # self.user_model.appendRow(item)

                item = [QStandardItem(str(i)) for i in [u.id, u.name, '-']]
                self.add_payment_model.appendRow(item)
                new_dspinbox = QDoubleSpinBox(minimum=-99999999, maximum=99999999, decimals=0)
                new_dspinbox.setStyleSheet("QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {width: 0;}")
                self.AddPayments_tableView.setIndexWidget(self.add_payment_model.index(cnt, 2), new_dspinbox)

                self.SelectUsers_listWidget.addItem(QListWidgetItem(f"{u.name}"))
                cnt += 1


            self.UserCount_label.setText(f"{cnt}")


    def reset_payment_values(self):
        for i in range(self.add_payment_model.rowCount()):
            new_dspinbox = QDoubleSpinBox(minimum=-99999999, maximum=99999999, decimals=0)
            new_dspinbox.setStyleSheet("QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {width: 0;}")
            self.AddPayments_tableView.setIndexWidget(self.add_payment_model.index(i, 2), new_dspinbox)

    # def user_add(self):
    #     if not self.new_user.isRunning():
    #         self.new_user.start()

    def select_user(self, user_name):
        if user_name in ['Выберите пользователя', '']:
            self.selected_id = None
            # self.confirmed_message_box('Информация', 'Выберите пользователя', icon_type=QMessageBox.Information)
            return
        # self.selected_id = int(str(user_name).split(']')[0][1:])

        with self.session() as sess:
            user = sess.execute(select(Users).where(Users.name == str(user_name))).scalar()
            self.selected_id = user.id
            # user = sess.get(Users, self.selected_id)
            # print(user.id, user.name, user.created_at)
            self.Name_lineEdit.setText(user.name)
            self.AddUsertDateVal_label.setText(str(user.created_at))

            last_pay = sess.execute(select(func.max(Payments.created_at)).where(Payments.user_id==self.selected_id)).scalar()
            self.LastPaymentDateVal_label.setText(str(last_pay) if last_pay else '-')

            # amount_sum = sess.execute(select(func.sum(Payments.amount)).where(Payments.user_id == self.selected_id)).scalar()
            # self.SumVal_label.setText(str(amount_sum) if amount_sum is not None else '0')

            while self.payment_model.rowCount() > 0:
                self.payment_model.removeRow(self.payment_model.rowCount() - 1)

            row_limit = self.PaymentHistoryLimit_spinBox.value() if self.PaymentHistoryLimit_checkBox.isChecked() else None
            conditions = [Payments.user_id==self.selected_id, ]
            if self.SelectDate_checkBox.isChecked():
                conditions.append(and_(Payments.created_at >= datetime.date(*self.SelectPaymentsSince_dateEdit.date().getDate()),
                                       Payments.created_at <= datetime.date(*self.SelectPaymentsTo_dateEdit.date().getDate()) + datetime.timedelta(days=1)))
                # conditions.append(and_(Payments.created_at <= datetime.date(*self.SelectPaymentsTo_dateEdit.date().getDate())))

            payments = sess.execute(select(Payments).where(and_(*conditions)).limit(row_limit).order_by(Payments.created_at.desc())).scalars()
            total_sum = 0
            payment_count = 0
            for p in payments:
                item = [QStandardItem(str(i)) for i in [p.id, f"{p.amount:,.0f}".replace(',', '.'), p.created_at]]
                self.payment_model.appendRow(item)
                total_sum += p.amount
                payment_count += 1
            self.PaymentSumVal_label.setText(f"{total_sum:,.0f}".replace(',', '.'))
            self.PaymentCount_label.setText(f"Кол-во выплат: {payment_count}")



    def create_new_user(self):
        if str(self.Name_lineEdit.text()) == '':
            return
        new_user = Users(name=str(self.Name_lineEdit.text()))
        with self.session() as sess:
            sess.add(new_user)
            sess.commit()
            u_id = new_user.id

        self.log(f"Пользователь {str(self.Name_lineEdit.text())} добавлен")
        self.update_users_lists()
        self.select_user(f"{self.Name_lineEdit.text()}")  # [{u_id}]

    def update_user_info(self, btn):
        if btn.text() != 'OK':
            return
        if not self.selected_id:
            return

        new_name = self.Name_lineEdit.text()
        # old_name = '] '.join(str(self.Users_comboBox.currentText()).split('] ')[1:])
        old_name = str(self.Users_comboBox.currentText())
        with self.session() as sess:
            sess.execute(update(Users).where(Users.id==self.selected_id).values(name=new_name))
            sess.commit()

        # logger.log(21, f"Изменено ФИО у пользователя с id {self.selected_id} ({old_name} => {new_name})")
        # log(U_LOG_ID, f"Изменено ФИО у пользователя с id {self.selected_id} ({old_name} => {new_name})")
        self.log(f"Изменено ФИО у пользователя с id {self.selected_id} ({old_name} => {new_name})")

        # self.Users_comboBox.setItemText(self.Users_comboBox.currentIndex(), f"[{self.selected_id}] {new_name}")
        self.update_users_lists()
        # self.select_user(new_name)



    def del_user(self, btn):
        if btn.text() != 'OK':
            return
        if not self.selected_id:
            return

        with self.session() as sess:
            sess.query(Users).where(Users.id==self.selected_id).delete()
            sess.query(Payments).where(Payments.user_id==self.selected_id).delete()
            sess.commit()

        self.selected_id = None
        self.log(f"Пользователь {str(self.Name_lineEdit.text())} удалён")
        self.update_users_lists()
        while self.total_pay_model.rowCount() > 0:
            self.total_pay_model.removeRow(self.total_pay_model.rowCount() - 1)

    # def add_payment(self):
    #     if self.UsersAddPayment_listWidget.selectedItems():  # для группы пользователей
    #         self.id_list = [int(u.text().split('] ')[0][1:]) for u in self.UsersAddPayment_listWidget.selectedItems()]
    #         self.user_list = [u.text() for u in self.UsersAddPayment_listWidget.selectedItems()]
    #         msg = f"Добавить {self.Payment_doubleSpinBox.value()}р. для выбранных пользователей?\n"
    #         msg += ',\n'.join(self.user_list)
    #         self.confirmed_message_box('Добавление выплаты', msg, self.add_payment_db)
    #         # print(msg)
    #     elif self.selected_id:  # для основного выбранного пользователя
    #         self.id_list = [self.selected_id]
    #         self.user_list = [str(self.Users_comboBox.currentText())]
    #         msg = f"Добавить {self.Payment_doubleSpinBox.value()}р. для {self.Users_comboBox.currentText()}?"
    #         self.confirmed_message_box('Добавление выплаты', msg, self.add_payment_db)
    #         # print(self.selected_id)
    #     else:
    #         self.log_p(f"Необходимо выбрать пользователя")
    #         return
    def add_payment(self):
        if self.add_payment_model.rowCount() == 0:
            return
        sum = 0
        self.payments_dict = dict()
        self.info_msg = 'Добавлены выплаты для:\n'
        for i in range(self.add_payment_model.rowCount()):
            val = int(self.AddPayments_tableView.indexWidget(self.add_payment_model.index(i, 2)).value())
            if val == 0:
                continue
            sum += val
            user_id = int(self.add_payment_model.item(i, 0).text())
            user_name = self.add_payment_model.item(i, 1).text()
            self.payments_dict[user_id] = val
            self.info_msg += f"{user_name}: {val} руб.\n"

        if len(self.payments_dict) == 0:
            self.confirmed_message_box('Информация', 'Не указаны выплаты', icon_type=QMessageBox.Information)
            return
        self.info_msg += f"\nСумма: {sum} руб."
        msg = f"Добавить выплаты для {len(self.payments_dict)} из {self.add_payment_model.rowCount()} пользователей?\nСумма: {sum} руб."
        self.confirmed_message_box('Добавление выплаты', msg, self.add_payment_db)

        while self.total_pay_model.rowCount() > 0:
            self.total_pay_model.removeRow(self.total_pay_model.rowCount() - 1)

    def add_payment_db(self, btn):
        if btn.text() != 'OK':
            return
        with self.session() as sess:
            payments_obj_list = [Payments(user_id=u_id, amount=self.payments_dict[u_id]) for u_id in self.payments_dict]
            sess.add_all(payments_obj_list)
            sess.commit()
        self.confirmed_message_box('Выплаты добавлены', self.info_msg, icon_type=QMessageBox.NoIcon)
        self.select_user(self.Users_comboBox.currentText())
        self.log_p(self.info_msg)

        cursor = self.textBrowser_2.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textBrowser_2.setTextCursor(cursor)



    # def set_last_payment(self):
    #     if self.UsersAddPayment_listWidget.selectedItems():  # для группы пользователей
    #         # если из группы выбран только один, то доп. условие
    #         conditions = []
    #         if len(self.UsersAddPayment_listWidget.selectedItems()) == 1:
    #             u_id = int(self.UsersAddPayment_listWidget.selectedItems()[0].text().split('] ')[0][1:])
    #             conditions.append(Payments.user_id==u_id)
    #         with self.session() as sess:
    #             last_payment = sess.execute(select(Payments.amount, func.max(Payments.created_at)).where(*conditions)).scalar()
    #         self.Payment_doubleSpinBox.setValue(last_payment if last_payment is not None else 0)
    #     elif self.selected_id:  # для основного выбранного пользователя
    #         with self.session() as sess:
    #             last_payment = sess.execute(select(Payments.amount, func.max(Payments.created_at)).where(
    #                 Payments.user_id==self.selected_id)).scalar()
    #         self.Payment_doubleSpinBox.setValue(last_payment if last_payment is not None else 0)
    #     else:
    #         self.log_p(f"Необходимо выбрать пользователя")
    #         return
    def set_last_payment(self):
        if self.add_payment_model.rowCount() == 0:
            return
        with self.session() as sess:
            res = sess.execute(select(Payments.user_id, Payments.amount, func.max(Payments.created_at)).group_by(Payments.user_id))
            # for last_payment, id_user, _ in res:
            last_payments_dict = {id_user: last_payment for id_user, last_payment, _ in res}
            # print(last_payments_dict)

            for i in range(self.add_payment_model.rowCount()):
                val = last_payments_dict.get(int(self.add_payment_model.item(i, 0).text()), 0)
                new_dspinbox = QDoubleSpinBox(minimum=-99999999, maximum=99999999, value=val, decimals=0)
                new_dspinbox.setStyleSheet("QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {width: 0;}")
                self.AddPayments_tableView.setIndexWidget(self.add_payment_model.index(i, 2), new_dspinbox)



    # def add_payment_db(self, btn):
    #     if btn.text() != 'OK':
    #         return
    #     with self.session() as sess:
    #         payments_obj_list = [Payments(user_id=i, amount=self.Payment_doubleSpinBox.value()) for i in self.id_list]
    #         sess.add_all(payments_obj_list)
    #         sess.commit()
    #     self.log_p(f"Добавлена выплата {self.Payment_doubleSpinBox.value()} для:\n {', '.join(self.user_list)}")
    #     self.select_user(self.Users_comboBox.currentText())

    # def del_payment(self):
    #     if not self.selected_id:
    #         self.log_p(f"Выберите пользователя")
    #         return
    #     # with self.session() as sess:
    #     #     payment_id_list = sess.execute(select(Payments.id).where(Payments.user_id==self.selected_id)).scalars().all()
    #     self.payment_id_dict = dict()
    #     for i in range(self.payment_model.rowCount()):
    #         # print(self.payment_model.item(i, 0).text())
    #         self.payment_id_dict[int(self.payment_model.item(i, 0).text())] = self.payment_model.item(i, 1).text()
    #     # print(self.payment_id_dict)
    #
    #     self.p_del_id = int(self.PaumentID_spinBox.value())
    #
    #     self.extra_msg = ''
    #     if self.p_del_id in self.payment_id_dict.keys():
    #         self.extra_msg = f' у {self.Users_comboBox.currentText()}'
    #
    #     #     self.log_p(f"Выплаты с id {self.p_del_id} нет в списке")
    #     #     return
    #
    #     self.confirmed_message_box('Удаление выплаты',f"Удалить выплату id {self.p_del_id}{self.extra_msg}?",
    #                                self.del_payment_db)
    #
    # def del_payment_db(self, btn):
    #     if btn.text() != 'OK':
    #         return
    #     with self.session() as sess:
    #         sess.query(Payments).where(Payments.id==self.p_del_id).delete()
    #         sess.commit()
    #
    #     extra_msg_2 = ''
    #     if self.extra_msg:
    #         extra_msg_2 = f"{self.extra_msg} ({self.payment_id_dict[self.p_del_id]} р.)"
    #     self.log_p(f"Выплата id {self.p_del_id} удалена{extra_msg_2}")
    #     self.select_user(self.Users_comboBox.currentText())

    def load_total_payments(self):
        while self.total_pay_model.rowCount() > 0:
            self.total_pay_model.removeRow(self.total_pay_model.rowCount() - 1)

        row_limit = self.TotalPaymentHistoryLimit_spinBox.value() if self.TotalPaymentHistoryLimit_checkBox.isChecked() else None
        conditions = []
        with self.session() as sess:
            if self.TotalSelectDate_checkBox.isChecked():
                conditions.append(
                    and_(Payments.created_at >= datetime.date(*self.TotalSelectPaymentsSince_dateEdit.date().getDate()),
                         Payments.created_at <= datetime.date(*self.TotalSelectPaymentsTo_dateEdit.date().getDate()) + datetime.timedelta(days=1)))
                # conditions.append(and_(Payments.created_at <= datetime.date(*self.SelectPaymentsTo_dateEdit.date().getDate())))
            if self.SelectUsers_checkBox.isChecked():
                if len(self.SelectUsers_listWidget.selectedItems()) == 0:
                    self.confirmed_message_box('Информация', 'Выберите пользователей', icon_type=QMessageBox.Information)
                    return
                id_list = sess.execute(select(Users.id).where(Users.name.in_(
                    [user_name.text() for user_name in self.SelectUsers_listWidget.selectedItems()]))).scalars().all()
                # print(id_list)
                conditions.append(Payments.user_id.in_(id_list))

            payments = sess.execute(select(Payments.id, Users.name, Payments.amount, Payments.created_at).where(*conditions).
                                    join(Users, Payments.user_id==Users.id).limit(row_limit).order_by(Users.name, Payments.created_at.desc())).all()
            total_sum = 0
            payment_count = 0
            for p in payments:
                # print(p.name)
                item = [QStandardItem(str(i)) for i in [p.id, p.name, f"{p.amount:,.0f}".replace(',', '.'), p.created_at]]
                doing = QStandardItem('...')
                doing.setTextAlignment(Qt.AlignCenter)
                # fnt = doing.font()
                # fnt.setBold(True)
                # doing.setFont(fnt)
                item.append(doing)
                self.total_pay_model.appendRow(item)
                # new_btn = QPushButton('Удалить')
                # new_btn.clicked.connect(lambda _: print(self.selected_payment_row))
                # self.TotalPayments_tableView.setIndexWidget(self.total_pay_model.index(payment_count, 4), new_btn)
                total_sum += p.amount
                payment_count += 1

        self.TotalPaymentSumVal_label.setText(f"{total_sum:,.0f}".replace(',', '.'))
        self.TotalPaymentCount_label.setText(f"Кол-во выплат: {payment_count}")

    def change_payment(self, ind):
        # print(ind.row(), ind.column())
        if ind.column() != 4:
            return
        self.selected_payment_id = int(self.total_pay_model.item(ind.row(), 0).text())
        old_payment = int(self.total_pay_model.item(ind.row(), 2).text().replace('.', ''))
        # print(self.selected_payment_id)
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Редактирование')
        dspinbox = QDoubleSpinBox(minimum=-99999999, maximum=99999999, decimals=0, value=old_payment)
        msg_box.layout().addWidget(QLabel('Новое значение:'), 0, 1)
        msg_box.layout().addWidget(dspinbox, 1, 1)
        # msg_box.layout().addWidget(QPushButton('Удалить'))
        # msg_box.layout().addWidget(QPushButton('Сохранить'))
        # msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Ok | QMessageBox.Cancel)

        save_b = msg_box.addButton('Сохранить', QMessageBox.AcceptRole)
        del_b = msg_box.addButton('Удалить', QMessageBox.AcceptRole)
        msg_box.addButton('Отмена', QMessageBox.AcceptRole)


        msg_box.exec()

        if msg_box.clickedButton() == save_b:
            # print('save', self.selected_payment_id, dspinbox.value())
            with self.session() as sess:
                sess.execute(update(Payments).where(Payments.id==self.selected_payment_id).values(amount=dspinbox.value()))
                sess.commit()
            u_name = self.total_pay_model.item(ind.row(), 1).text()

            self.load_total_payments()
            self.confirmed_message_box('Информация', f"Для {u_name} изменена выплата: {old_payment} => {int(dspinbox.value())}",
                                       icon_type=QMessageBox.NoIcon)
            self.select_user(self.Users_comboBox.currentText())
        elif msg_box.clickedButton() == del_b:
            # print('del', self.selected_payment_id)
            with self.session() as sess:
                sess.query(Payments).where(Payments.id==self.selected_payment_id).delete()
                sess.commit()
            u_name = self.total_pay_model.item(ind.row(), 1).text()
            self.load_total_payments()
            self.confirmed_message_box('Информация',f"Для {u_name} удалена выплата ({old_payment} руб.)",
                                       icon_type=QMessageBox.NoIcon)
            self.select_user(self.Users_comboBox.currentText())

    def confirmed_message_box(self, title, msg, function=None, icon_type=QMessageBox.Question):
        ConfirmMsgBox = QMessageBox()
        ConfirmMsgBox.setWindowTitle(title)
        ConfirmMsgBox.setText(msg)
        ConfirmMsgBox.setIcon(icon_type)
        ConfirmMsgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ConfirmMsgBox.setDefaultButton(QMessageBox.Ok)
        if function:
            ConfirmMsgBox.buttonClicked.connect(function)

        ConfirmMsgBox.exec()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    app.exec()