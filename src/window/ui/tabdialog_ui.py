# Form implementation generated from reading ui file 'c:\Users\gabri\Documents\Github\TeleScore\src\window\ui\tabdialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ActionDialog(object):
    def setupUi(self, ActionDialog):
        ActionDialog.setObjectName("ActionDialog")
        ActionDialog.resize(480, 270)
        self.gridLayout = QtWidgets.QGridLayout(ActionDialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")

        self.retranslateUi(ActionDialog)
        QtCore.QMetaObject.connectSlotsByName(ActionDialog)

    def retranslateUi(self, ActionDialog):
        _translate = QtCore.QCoreApplication.translate
        ActionDialog.setWindowTitle(_translate("ActionDialog", "Save Project?"))
