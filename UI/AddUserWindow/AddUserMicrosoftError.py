# Form implementation generated from reading ui file 'UI/AddUserWindow/AddUserMicrosoftError.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_AddUserMicrosoftError(object):
    def setupUi(self, Dialog_AddUserMicrosoftError):
        Dialog_AddUserMicrosoftError.setObjectName("Dialog_AddUserMicrosoftError")
        Dialog_AddUserMicrosoftError.resize(510, 227)
        Dialog_AddUserMicrosoftError.setStyleSheet("#widget_3{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: 1px solid rgb(33, 33, 33);\n"
"    border-radius: 8px;\n"
"    background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton{border-style:none;}")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog_AddUserMicrosoftError)
        self.horizontalLayout_2.setContentsMargins(6, 4, 10, 11)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_3 = QtWidgets.QWidget(parent=Dialog_AddUserMicrosoftError)
        self.widget_3.setObjectName("widget_3")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout.setContentsMargins(10, 5, 12, 11)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=self.widget_3)
        self.label.setMinimumSize(QtCore.QSize(50, 50))
        self.label.setMaximumSize(QtCore.QSize(50, 50))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/image/images/Error.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(parent=self.widget_3)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setContentsMargins(0, 8, 0, 0)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(19)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_h1 = QtWidgets.QLabel(parent=self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_h1.setFont(font)
        self.label_h1.setObjectName("label_h1")
        self.verticalLayout.addWidget(self.label_h1)
        self.label_h2 = QtWidgets.QLabel(parent=self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_h2.setFont(font)
        self.label_h2.setWordWrap(True)
        self.label_h2.setObjectName("label_h2")
        self.verticalLayout.addWidget(self.label_h2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.widget_2, 0, 1, 2, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 41, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.widget = QtWidgets.QWidget(parent=self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_copy = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton_copy.setMinimumSize(QtCore.QSize(49, 22))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_copy.setFont(font)
        self.pushButton_copy.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pushButton_copy.setObjectName("pushButton_copy")
        self.horizontalLayout.addWidget(self.pushButton_copy)
        self.pushButton_ok = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton_ok.setMinimumSize(QtCore.QSize(62, 22))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_ok.setFont(font)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.gridLayout.addWidget(self.widget, 2, 0, 1, 2)
        self.horizontalLayout_2.addWidget(self.widget_3)

        self.retranslateUi(Dialog_AddUserMicrosoftError)
        QtCore.QMetaObject.connectSlotsByName(Dialog_AddUserMicrosoftError)

    def retranslateUi(self, Dialog_AddUserMicrosoftError):
        _translate = QtCore.QCoreApplication.translate
        Dialog_AddUserMicrosoftError.setWindowTitle(_translate("Dialog_AddUserMicrosoftError", "Dialog"))
        self.label_2.setText(_translate("Dialog_AddUserMicrosoftError", "错误"))
        self.label_h1.setText(_translate("Dialog_AddUserMicrosoftError", "在进行微软登陆时出现错误, 可能是由于您……导致的。\n"
"错误关键字: XXX\n"
"\n"
"您可以点击下方\"复制报错详细信息\"按钮,在关于中进行反馈"))
        self.label_h2.setText(_translate("Dialog_AddUserMicrosoftError", "<html><head/><body><p>如果您没有正版Minecraft账户, 请您先<a href=\"https://www.minecraft.net/store/minecraft-java-bedrock-edition-pc\"><span style=\" text-decoration: underline; color:#0068da;\">购买正版Minecraft账户</span></a></p></body></html>"))
        self.pushButton_copy.setText(_translate("Dialog_AddUserMicrosoftError", "复制报错详细信息"))
        self.pushButton_ok.setText(_translate("Dialog_AddUserMicrosoftError", "确认"))
