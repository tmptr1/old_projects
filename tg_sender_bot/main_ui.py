# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(767, 321)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.SelectFileButton = QPushButton(self.centralwidget)
        self.SelectFileButton.setObjectName(u"SelectFileButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentPageSetup))
        self.SelectFileButton.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.SelectFileButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.AuthTgButton = QPushButton(self.centralwidget)
        self.AuthTgButton.setObjectName(u"AuthTgButton")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.CameraWeb))
        self.AuthTgButton.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.AuthTgButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(483, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        font = QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.Phone_comboBox = QComboBox(self.groupBox)
        self.Phone_comboBox.setObjectName(u"Phone_comboBox")

        self.gridLayout.addWidget(self.Phone_comboBox, 0, 1, 1, 1)

        self.Name_comboBox = QComboBox(self.groupBox)
        self.Name_comboBox.setObjectName(u"Name_comboBox")

        self.gridLayout.addWidget(self.Name_comboBox, 1, 1, 1, 1)

        self.Name_label = QLabel(self.groupBox)
        self.Name_label.setObjectName(u"Name_label")
        self.Name_label.setFont(font)

        self.gridLayout.addWidget(self.Name_label, 1, 0, 1, 1)

        self.Phone_label = QLabel(self.groupBox)
        self.Phone_label.setObjectName(u"Phone_label")
        self.Phone_label.setFont(font)

        self.gridLayout.addWidget(self.Phone_label, 0, 0, 1, 1)

        self.Status_label = QLabel(self.groupBox)
        self.Status_label.setObjectName(u"Status_label")

        self.gridLayout.addWidget(self.Status_label, 2, 0, 1, 1)

        self.Status_comboBox = QComboBox(self.groupBox)
        self.Status_comboBox.setObjectName(u"Status_comboBox")

        self.gridLayout.addWidget(self.Status_comboBox, 2, 1, 1, 1)


        self.horizontalLayout_3.addWidget(self.groupBox)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout.addWidget(self.label_3)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.StartRow_spinBox = QSpinBox(self.centralwidget)
        self.StartRow_spinBox.setObjectName(u"StartRow_spinBox")
        self.StartRow_spinBox.setMinimum(1)

        self.verticalLayout_2.addWidget(self.StartRow_spinBox)

        self.GetRow_spinBox = QSpinBox(self.centralwidget)
        self.GetRow_spinBox.setObjectName(u"GetRow_spinBox")
        self.GetRow_spinBox.setMinimum(1)
        self.GetRow_spinBox.setMaximum(999999)

        self.verticalLayout_2.addWidget(self.GetRow_spinBox)

        self.Delay_spinBox = QSpinBox(self.centralwidget)
        self.Delay_spinBox.setObjectName(u"Delay_spinBox")
        self.Delay_spinBox.setMinimum(1)
        self.Delay_spinBox.setMaximum(999999)
        self.Delay_spinBox.setValue(5)

        self.verticalLayout_2.addWidget(self.Delay_spinBox)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 1, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(483, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.StartButton = QPushButton(self.centralwidget)
        self.StartButton.setObjectName(u"StartButton")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart))
        self.StartButton.setIcon(icon2)

        self.horizontalLayout.addWidget(self.StartButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalSpacer_3 = QSpacerItem(483, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(4, 1)

        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 767, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.SelectFileButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0444\u0430\u0439\u043b", None))
        self.AuthTgButton.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f \u0432 Telegram", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u043e\u043b\u0431\u0446\u044b", None))
        self.Name_label.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f:", None))
        self.Phone_label.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430:", None))
        self.Status_label.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0443\u0441 \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0447\u0430\u0442\u044c \u0441\u043e \u0441\u0442\u0440\u043e\u043a\u0438:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0437\u044f\u0442\u044c \u0441\u0442\u0440\u043e\u043a:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0434\u0435\u0440\u0436\u043a\u0430 \u043c\u0435\u0436\u0434\u0443 \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0430\u043c\u0438 (\u0441\u0435\u043a):", None))
        self.StartButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u043a \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438", None))
    # retranslateUi

