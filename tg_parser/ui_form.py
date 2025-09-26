# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(751, 594)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_3 = QGridLayout(self.tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)

        self.horizontalLayout.addWidget(self.label_2)

        self.Path_lineEdit = QLineEdit(self.groupBox)
        self.Path_lineEdit.setObjectName(u"Path_lineEdit")
        self.Path_lineEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.Path_lineEdit)

        self.FileBrowse_Button = QPushButton(self.groupBox)
        self.FileBrowse_Button.setObjectName(u"FileBrowse_Button")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentPageSetup))
        self.FileBrowse_Button.setIcon(icon)

        self.horizontalLayout.addWidget(self.FileBrowse_Button)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_4 = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.horizontalLayout_2.addWidget(self.label)

        self.Limit_spinBox = QSpinBox(self.groupBox)
        self.Limit_spinBox.setObjectName(u"Limit_spinBox")
        self.Limit_spinBox.setFont(font)
        self.Limit_spinBox.setMinimum(1)
        self.Limit_spinBox.setMaximum(9999)
        self.Limit_spinBox.setValue(1)

        self.horizontalLayout_2.addWidget(self.Limit_spinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_3 = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Start_Button = QPushButton(self.groupBox)
        self.Start_Button.setObjectName(u"Start_Button")

        self.horizontalLayout_3.addWidget(self.Start_Button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 3)

        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.ToDir_Button = QPushButton(self.tab)
        self.ToDir_Button.setObjectName(u"ToDir_Button")
        icon1 = QIcon(QIcon.fromTheme(u"folder-open"))
        self.ToDir_Button.setIcon(icon1)

        self.horizontalLayout_5.addWidget(self.ToDir_Button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.Logs_textBrowser = QTextBrowser(self.tab)
        self.Logs_textBrowser.setObjectName(u"Logs_textBrowser")

        self.verticalLayout_2.addWidget(self.Logs_textBrowser)

        self.verticalLayout_2.setStretch(0, 5)
        self.verticalLayout_2.setStretch(1, 3)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)
        self.verticalLayout_2.setStretch(4, 15)

        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_9 = QGridLayout(self.tab_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalSpacer_5 = QSpacerItem(196, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_5, 1, 2, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.verticalSpacer_6, 0, 1, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 166, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_5, 3, 1, 1, 1)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.groupBox_2.setFont(font1)
        self.gridLayout_7 = QGridLayout(self.groupBox_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_3.setFont(font2)

        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)

        self.api_id_tg_lineEdit = QLineEdit(self.groupBox_2)
        self.api_id_tg_lineEdit.setObjectName(u"api_id_tg_lineEdit")
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(False)
        self.api_id_tg_lineEdit.setFont(font3)

        self.gridLayout_6.addWidget(self.api_id_tg_lineEdit, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)

        self.gridLayout_6.addWidget(self.label_4, 1, 0, 1, 1)

        self.api_hash_tg_lineEdit = QLineEdit(self.groupBox_2)
        self.api_hash_tg_lineEdit.setObjectName(u"api_hash_tg_lineEdit")
        self.api_hash_tg_lineEdit.setFont(font3)

        self.gridLayout_6.addWidget(self.api_hash_tg_lineEdit, 1, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font2)

        self.gridLayout_6.addWidget(self.label_9, 2, 0, 1, 1)

        self.bot_id_lineEdit = QLineEdit(self.groupBox_2)
        self.bot_id_lineEdit.setObjectName(u"bot_id_lineEdit")
        self.bot_id_lineEdit.setFont(font3)

        self.gridLayout_6.addWidget(self.bot_id_lineEdit, 2, 1, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font1)
        self.gridLayout_5 = QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font2)

        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 1)

        self.api_key_dd_lineEdit = QLineEdit(self.groupBox_3)
        self.api_key_dd_lineEdit.setObjectName(u"api_key_dd_lineEdit")
        self.api_key_dd_lineEdit.setFont(font3)

        self.gridLayout_4.addWidget(self.api_key_dd_lineEdit, 0, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font2)

        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)

        self.api_secret_key_dd_lineEdit = QLineEdit(self.groupBox_3)
        self.api_secret_key_dd_lineEdit.setObjectName(u"api_secret_key_dd_lineEdit")
        self.api_secret_key_dd_lineEdit.setFont(font3)

        self.gridLayout_4.addWidget(self.api_secret_key_dd_lineEdit, 1, 1, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_3, 1, 0, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_8, 1, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(197, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.SaveButton = QPushButton(self.tab_2)
        self.SaveButton.setObjectName(u"SaveButton")

        self.gridLayout_9.addWidget(self.SaveButton, 2, 1, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 751, 22))
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
        self.groupBox.setTitle("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0443\u0442\u044c \u0434\u043e \u0442\u0430\u0431\u043b\u0438\u0446\u044b:", None))
        self.FileBrowse_Button.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0444\u0430\u0439\u043b", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u043c\u0438\u0442:", None))
        self.Start_Button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.ToDir_Button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u0432 \u043f\u0430\u043f\u043a\u0443 \u0441 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u043c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a \u043d\u043e\u043c\u0435\u0440\u043e\u0432", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Telegram", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"App api_id:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"App api_hash:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Tg Bot:", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Dadata", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"API-\u043a\u043b\u044e\u0447:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0435\u043a\u0440\u0435\u0442\u043d\u044b\u0439 \u043a\u043b\u044e\u0447:", None))
        self.SaveButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
    # retranslateUi

