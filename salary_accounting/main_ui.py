# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QFormLayout, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTabWidget,
    QTableView, QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1077, 865)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_23)

        self.UpdateusersCB_button = QPushButton(self.centralwidget)
        self.UpdateusersCB_button.setObjectName(u"UpdateusersCB_button")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        self.UpdateusersCB_button.setIcon(icon)

        self.horizontalLayout_12.addWidget(self.UpdateusersCB_button)


        self.gridLayout.addLayout(self.horizontalLayout_12, 0, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        font = QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_2 = QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.horizontalLayout_3.addWidget(self.label)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.Users_comboBox = QComboBox(self.tab)
        self.Users_comboBox.setObjectName(u"Users_comboBox")
        self.Users_comboBox.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(False)
        self.Users_comboBox.setFont(font1)

        self.horizontalLayout_3.addWidget(self.Users_comboBox)

        self.UserCount_label = QLabel(self.tab)
        self.UserCount_label.setObjectName(u"UserCount_label")

        self.horizontalLayout_3.addWidget(self.UserCount_label)

        self.Search_lineEdit = QLineEdit(self.tab)
        self.Search_lineEdit.setObjectName(u"Search_lineEdit")

        self.horizontalLayout_3.addWidget(self.Search_lineEdit)

        self.Search_button = QPushButton(self.tab)
        self.Search_button.setObjectName(u"Search_button")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind))
        self.Search_button.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.Search_button)

        self.ClearSearchLine_button = QPushButton(self.tab)
        self.ClearSearchLine_button.setObjectName(u"ClearSearchLine_button")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.WindowClose))
        self.ClearSearchLine_button.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.ClearSearchLine_button)

        self.horizontalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(2, 15)
        self.horizontalLayout_3.setStretch(4, 15)
        self.horizontalLayout_3.setStretch(7, 4)

        self.verticalLayout_8.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.UserName_label = QLabel(self.tab)
        self.UserName_label.setObjectName(u"UserName_label")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.UserName_label.setFont(font2)

        self.horizontalLayout.addWidget(self.UserName_label)

        self.horizontalSpacer = QSpacerItem(5, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.Name_lineEdit = QLineEdit(self.tab)
        self.Name_lineEdit.setObjectName(u"Name_lineEdit")
        self.Name_lineEdit.setFont(font2)

        self.horizontalLayout.addWidget(self.Name_lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.LastPaymentDate_label = QLabel(self.tab)
        self.LastPaymentDate_label.setObjectName(u"LastPaymentDate_label")
        self.LastPaymentDate_label.setFont(font2)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.LastPaymentDate_label)

        self.LastPaymentDateVal_label = QLabel(self.tab)
        self.LastPaymentDateVal_label.setObjectName(u"LastPaymentDateVal_label")
        self.LastPaymentDateVal_label.setFont(font2)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.LastPaymentDateVal_label)

        self.AddUsertDate_label = QLabel(self.tab)
        self.AddUsertDate_label.setObjectName(u"AddUsertDate_label")
        self.AddUsertDate_label.setFont(font2)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.AddUsertDate_label)

        self.AddUsertDateVal_label = QLabel(self.tab)
        self.AddUsertDateVal_label.setObjectName(u"AddUsertDateVal_label")
        self.AddUsertDateVal_label.setFont(font2)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.AddUsertDateVal_label)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_13 = QSpacerItem(13, 86, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_13)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.UserAdd_button = QPushButton(self.tab)
        self.UserAdd_button.setObjectName(u"UserAdd_button")
        self.UserAdd_button.setFont(font2)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ContactNew))
        self.UserAdd_button.setIcon(icon3)

        self.verticalLayout_2.addWidget(self.UserAdd_button)

        self.UpdateUser_button = QPushButton(self.tab)
        self.UpdateUser_button.setObjectName(u"UpdateUser_button")
        self.UpdateUser_button.setFont(font2)
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs))
        self.UpdateUser_button.setIcon(icon4)

        self.verticalLayout_2.addWidget(self.UpdateUser_button)

        self.DeleteUser_button = QPushButton(self.tab)
        self.DeleteUser_button.setObjectName(u"DeleteUser_button")
        self.DeleteUser_button.setFont(font2)
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.DeleteUser_button.setIcon(icon5)

        self.verticalLayout_2.addWidget(self.DeleteUser_button)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_12 = QSpacerItem(13, 86, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_12)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.PaymentHistoryLimit_checkBox = QCheckBox(self.tab)
        self.PaymentHistoryLimit_checkBox.setObjectName(u"PaymentHistoryLimit_checkBox")
        self.PaymentHistoryLimit_checkBox.setChecked(True)

        self.horizontalLayout_10.addWidget(self.PaymentHistoryLimit_checkBox)

        self.PaymentHistoryLimit_spinBox = QSpinBox(self.tab)
        self.PaymentHistoryLimit_spinBox.setObjectName(u"PaymentHistoryLimit_spinBox")
        self.PaymentHistoryLimit_spinBox.setMinimum(1)
        self.PaymentHistoryLimit_spinBox.setMaximum(999999)
        self.PaymentHistoryLimit_spinBox.setValue(20)

        self.horizontalLayout_10.addWidget(self.PaymentHistoryLimit_spinBox)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_9)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.verticalSpacer_8 = QSpacerItem(256, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_8)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.SelectDate_checkBox = QCheckBox(self.tab)
        self.SelectDate_checkBox.setObjectName(u"SelectDate_checkBox")

        self.verticalLayout_7.addWidget(self.SelectDate_checkBox)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_9.addWidget(self.label_4)

        self.SelectPaymentsSince_dateEdit = QDateEdit(self.tab)
        self.SelectPaymentsSince_dateEdit.setObjectName(u"SelectPaymentsSince_dateEdit")

        self.horizontalLayout_9.addWidget(self.SelectPaymentsSince_dateEdit)

        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_9.addWidget(self.label_3)

        self.SelectPaymentsTo_dateEdit = QDateEdit(self.tab)
        self.SelectPaymentsTo_dateEdit.setObjectName(u"SelectPaymentsTo_dateEdit")

        self.horizontalLayout_9.addWidget(self.SelectPaymentsTo_dateEdit)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_8)


        self.verticalLayout_7.addLayout(self.horizontalLayout_9)


        self.verticalLayout.addLayout(self.verticalLayout_7)

        self.verticalSpacer_9 = QSpacerItem(256, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_9)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_16)

        self.ShowPayments_button = QPushButton(self.tab)
        self.ShowPayments_button.setObjectName(u"ShowPayments_button")
        self.ShowPayments_button.setIcon(icon)

        self.horizontalLayout_11.addWidget(self.ShowPayments_button)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_17)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.verticalSpacer_6 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.PaymentSum_label = QLabel(self.tab)
        self.PaymentSum_label.setObjectName(u"PaymentSum_label")

        self.horizontalLayout_8.addWidget(self.PaymentSum_label)

        self.horizontalSpacer_7 = QSpacerItem(5, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)

        self.PaymentSumVal_label = QLabel(self.tab)
        self.PaymentSumVal_label.setObjectName(u"PaymentSumVal_label")

        self.horizontalLayout_8.addWidget(self.PaymentSumVal_label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_5)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.horizontalSpacer_22 = QSpacerItem(13, 420, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_22)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.Payments_tableView = QTableView(self.tab)
        self.Payments_tableView.setObjectName(u"Payments_tableView")

        self.verticalLayout_3.addWidget(self.Payments_tableView)

        self.PaymentCount_label = QLabel(self.tab)
        self.PaymentCount_label.setObjectName(u"PaymentCount_label")

        self.verticalLayout_3.addWidget(self.PaymentCount_label)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_4.setStretch(0, 35)
        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(2, 40)

        self.verticalLayout_8.addLayout(self.horizontalLayout_4)


        self.gridLayout_2.addLayout(self.verticalLayout_8, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_3 = QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_11)

        self.ResetSelect_button = QPushButton(self.tab_2)
        self.ResetSelect_button.setObjectName(u"ResetSelect_button")
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditUndo))
        self.ResetSelect_button.setIcon(icon6)

        self.horizontalLayout_6.addWidget(self.ResetSelect_button)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.AddPayments_tableView = QTableView(self.tab_2)
        self.AddPayments_tableView.setObjectName(u"AddPayments_tableView")

        self.verticalLayout_5.addWidget(self.AddPayments_tableView)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.SetLastPayment_button = QPushButton(self.tab_2)
        self.SetLastPayment_button.setObjectName(u"SetLastPayment_button")
        self.SetLastPayment_button.setFont(font1)
        icon7 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpenRecent))
        self.SetLastPayment_button.setIcon(icon7)

        self.horizontalLayout_5.addWidget(self.SetLastPayment_button)

        self.AddPayment_button = QPushButton(self.tab_2)
        self.AddPayment_button.setObjectName(u"AddPayment_button")
        self.AddPayment_button.setFont(font1)
        icon8 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailSend))
        self.AddPayment_button.setIcon(icon8)

        self.horizontalLayout_5.addWidget(self.AddPayment_button)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_10)

        self.Log_2_button = QPushButton(self.tab_2)
        self.Log_2_button.setObjectName(u"Log_2_button")
        icon9 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FormatJustifyLeft))
        self.Log_2_button.setIcon(icon9)

        self.horizontalLayout_5.addWidget(self.Log_2_button)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.textBrowser_2 = QTextBrowser(self.tab_2)
        self.textBrowser_2.setObjectName(u"textBrowser_2")

        self.verticalLayout_5.addWidget(self.textBrowser_2)

        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 50)
        self.verticalLayout_5.setStretch(2, 1)
        self.verticalLayout_5.setStretch(3, 15)

        self.gridLayout_3.addLayout(self.verticalLayout_5, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_6 = QGridLayout(self.tab_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.verticalLayout_22 = QVBoxLayout()
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalSpacer_10 = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_10)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.TotalPaymentHistoryLimit_checkBox = QCheckBox(self.tab_3)
        self.TotalPaymentHistoryLimit_checkBox.setObjectName(u"TotalPaymentHistoryLimit_checkBox")
        self.TotalPaymentHistoryLimit_checkBox.setChecked(True)

        self.horizontalLayout_16.addWidget(self.TotalPaymentHistoryLimit_checkBox)

        self.TotalPaymentHistoryLimit_spinBox = QSpinBox(self.tab_3)
        self.TotalPaymentHistoryLimit_spinBox.setObjectName(u"TotalPaymentHistoryLimit_spinBox")
        self.TotalPaymentHistoryLimit_spinBox.setMinimum(1)
        self.TotalPaymentHistoryLimit_spinBox.setMaximum(999999)
        self.TotalPaymentHistoryLimit_spinBox.setValue(100)

        self.horizontalLayout_16.addWidget(self.TotalPaymentHistoryLimit_spinBox)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_18)


        self.verticalLayout_22.addLayout(self.horizontalLayout_16)

        self.verticalSpacer_11 = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_11)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.TotalSelectDate_checkBox = QCheckBox(self.tab_3)
        self.TotalSelectDate_checkBox.setObjectName(u"TotalSelectDate_checkBox")

        self.verticalLayout_9.addWidget(self.TotalSelectDate_checkBox)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_6 = QLabel(self.tab_3)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_15.addWidget(self.label_6)

        self.TotalSelectPaymentsSince_dateEdit = QDateEdit(self.tab_3)
        self.TotalSelectPaymentsSince_dateEdit.setObjectName(u"TotalSelectPaymentsSince_dateEdit")

        self.horizontalLayout_15.addWidget(self.TotalSelectPaymentsSince_dateEdit)

        self.label_5 = QLabel(self.tab_3)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_15.addWidget(self.label_5)

        self.TotalSelectPaymentsTo_dateEdit = QDateEdit(self.tab_3)
        self.TotalSelectPaymentsTo_dateEdit.setObjectName(u"TotalSelectPaymentsTo_dateEdit")

        self.horizontalLayout_15.addWidget(self.TotalSelectPaymentsTo_dateEdit)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_19)


        self.verticalLayout_9.addLayout(self.horizontalLayout_15)


        self.verticalLayout_22.addLayout(self.verticalLayout_9)

        self.verticalSpacer_12 = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_12)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.SelectUsers_checkBox = QCheckBox(self.tab_3)
        self.SelectUsers_checkBox.setObjectName(u"SelectUsers_checkBox")

        self.horizontalLayout_7.addWidget(self.SelectUsers_checkBox)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.SelectionCount_label = QLabel(self.tab_3)
        self.SelectionCount_label.setObjectName(u"SelectionCount_label")

        self.horizontalLayout_7.addWidget(self.SelectionCount_label)

        self.ResetSelection_pushButton = QPushButton(self.tab_3)
        self.ResetSelection_pushButton.setObjectName(u"ResetSelection_pushButton")
        self.ResetSelection_pushButton.setIcon(icon6)

        self.horizontalLayout_7.addWidget(self.ResetSelection_pushButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.SelectUsers_listWidget = QListWidget(self.tab_3)
        self.SelectUsers_listWidget.setObjectName(u"SelectUsers_listWidget")

        self.verticalLayout_6.addWidget(self.SelectUsers_listWidget)


        self.verticalLayout_22.addLayout(self.verticalLayout_6)

        self.verticalSpacer_14 = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_14)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_24)

        self.TotalShowPayments_button = QPushButton(self.tab_3)
        self.TotalShowPayments_button.setObjectName(u"TotalShowPayments_button")
        self.TotalShowPayments_button.setIcon(icon)

        self.horizontalLayout_18.addWidget(self.TotalShowPayments_button)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_25)


        self.verticalLayout_22.addLayout(self.horizontalLayout_18)

        self.verticalSpacer_13 = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_21)

        self.PaymentSum_label_2 = QLabel(self.tab_3)
        self.PaymentSum_label_2.setObjectName(u"PaymentSum_label_2")

        self.horizontalLayout_14.addWidget(self.PaymentSum_label_2)

        self.TotalPaymentSumVal_label = QLabel(self.tab_3)
        self.TotalPaymentSumVal_label.setObjectName(u"TotalPaymentSumVal_label")

        self.horizontalLayout_14.addWidget(self.TotalPaymentSumVal_label)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_20)


        self.verticalLayout_22.addLayout(self.horizontalLayout_14)

        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_16)

        self.verticalLayout_22.setStretch(1, 1)
        self.verticalLayout_22.setStretch(3, 1)
        self.verticalLayout_22.setStretch(5, 10)
        self.verticalLayout_22.setStretch(7, 1)
        self.verticalLayout_22.setStretch(9, 1)

        self.horizontalLayout_34.addLayout(self.verticalLayout_22)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.TotalPayments_tableView = QTableView(self.tab_3)
        self.TotalPayments_tableView.setObjectName(u"TotalPayments_tableView")

        self.verticalLayout_12.addWidget(self.TotalPayments_tableView)

        self.TotalPaymentCount_label = QLabel(self.tab_3)
        self.TotalPaymentCount_label.setObjectName(u"TotalPaymentCount_label")

        self.verticalLayout_12.addWidget(self.TotalPaymentCount_label)


        self.horizontalLayout_34.addLayout(self.verticalLayout_12)

        self.horizontalLayout_34.setStretch(0, 2)
        self.horizontalLayout_34.setStretch(1, 5)

        self.gridLayout_6.addLayout(self.horizontalLayout_34, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_4.addWidget(self.tabWidget)


        self.gridLayout.addLayout(self.verticalLayout_4, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1077, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.UpdateusersCB_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a \u0441\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c:", None))
        self.UserCount_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.Search_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a", None))
        self.ClearSearchLine_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c", None))
        self.UserName_label.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0418\u041e:", None))
        self.LastPaymentDate_label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u044f\u044f \u0434\u0430\u0442\u0430 \u0432\u044b\u043f\u043b\u0430\u0442\u044b:", None))
        self.LastPaymentDateVal_label.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.AddUsertDate_label.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f:", None))
        self.AddUsertDateVal_label.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.UserAdd_button.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043d\u043e\u0432\u043e\u0433\u043e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f", None))
        self.UpdateUser_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0438\u0437\u043c\u0435\u043d\u0451\u043d\u043d\u043e\u0435 \u0424\u0418\u041e", None))
        self.DeleteUser_button.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f", None))
        self.PaymentHistoryLimit_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u043c\u0438\u0442 \u0441\u0442\u0440\u043e\u043a", None))
        self.SelectDate_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u043e\u0440 \u0437\u0430 \u043f\u0435\u0440\u0438\u043e\u0434", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u0441", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0434\u043e", None))
        self.ShowPayments_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", None))
        self.PaymentSum_label.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0443\u043c\u043c\u0430:", None))
        self.PaymentSumVal_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.PaymentCount_label.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043b-\u0432\u043e \u0432\u044b\u043f\u043b\u0430\u0442: 0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u041e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435", None))
        self.ResetSelect_button.setText("")
        self.SetLastPayment_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0438\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f", None))
        self.AddPayment_button.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432\u044b\u043f\u043b\u0430\u0442\u0443", None))
        self.Log_2_button.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0432\u044b\u043f\u043b\u0430\u0442", None))
        self.TotalPaymentHistoryLimit_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u043c\u0438\u0442 \u0441\u0442\u0440\u043e\u043a", None))
        self.TotalSelectDate_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u043e\u0440 \u0437\u0430 \u043f\u0435\u0440\u0438\u043e\u0434", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u0441", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u0434\u043e", None))
        self.SelectUsers_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0434\u0435\u043b\u044c\u043d\u044b\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438", None))
        self.SelectionCount_label.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u043d\u043e: 0", None))
        self.ResetSelection_pushButton.setText("")
        self.TotalShowPayments_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", None))
        self.PaymentSum_label_2.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0443\u043c\u043c\u0430:", None))
        self.TotalPaymentSumVal_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.TotalPaymentCount_label.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043b-\u0432\u043e \u0432\u044b\u043f\u043b\u0430\u0442: 0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u0412\u0441\u0435 \u0432\u044b\u043f\u043b\u0430\u0442\u044b", None))
    # retranslateUi

