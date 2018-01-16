# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs-PyQt5/core/synthesis/Collections/TriangularIteration_dialog/collections.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 399)
        Dialog.setMinimumSize(QtCore.QSize(280, 399))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/collections.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.common_label = QtWidgets.QLabel(Dialog)
        self.common_label.setObjectName("common_label")
        self.verticalLayout_2.addWidget(self.common_label)
        self.common_linkage = QtWidgets.QListWidget(Dialog)
        self.common_linkage.setObjectName("common_linkage")
        item = QtWidgets.QListWidgetItem()
        self.common_linkage.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.common_linkage.addItem(item)
        self.verticalLayout_2.addWidget(self.common_linkage)
        self.common_load = QtWidgets.QPushButton(Dialog)
        self.common_load.setObjectName("common_load")
        self.verticalLayout_2.addWidget(self.common_load)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.Collections_label = QtWidgets.QLabel(Dialog)
        self.Collections_label.setObjectName("Collections_label")
        self.verticalLayout_3.addWidget(self.Collections_label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.collections_list = QtWidgets.QListWidget(Dialog)
        self.collections_list.setObjectName("collections_list")
        self.horizontalLayout_2.addWidget(self.collections_list)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.rename_button = QtWidgets.QPushButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/rename.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rename_button.setIcon(icon1)
        self.rename_button.setAutoDefault(False)
        self.rename_button.setObjectName("rename_button")
        self.verticalLayout.addWidget(self.rename_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.delete_button = QtWidgets.QPushButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_button.setIcon(icon2)
        self.delete_button.setAutoDefault(False)
        self.delete_button.setObjectName("delete_button")
        self.verticalLayout.addWidget(self.delete_button)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Open)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.common_load.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Workbook Collections"))
        self.common_label.setText(_translate("Dialog", "Common:"))
        __sortingEnabled = self.common_linkage.isSortingEnabled()
        self.common_linkage.setSortingEnabled(False)
        item = self.common_linkage.item(0)
        item.setText(_translate("Dialog", "Four bar linkage mechanism"))
        item = self.common_linkage.item(1)
        item.setText(_translate("Dialog", "Eight bar linkage mechanism"))
        self.common_linkage.setSortingEnabled(__sortingEnabled)
        self.common_load.setText(_translate("Dialog", "Load common structure"))
        self.Collections_label.setText(_translate("Dialog", "Workbook Collections:"))
        self.rename_button.setText(_translate("Dialog", "Rename"))
        self.delete_button.setText(_translate("Dialog", "Delete"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

