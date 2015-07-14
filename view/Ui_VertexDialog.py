# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VertexDialog.ui'
#
# Created: Tue Jul 14 17:01:17 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_VertexDialog(object):
    def setupUi(self, VertexDialog):
        VertexDialog.setObjectName(_fromUtf8("VertexDialog"))
        VertexDialog.resize(300, 400)
        VertexDialog.setMinimumSize(QtCore.QSize(300, 400))
        VertexDialog.setMaximumSize(QtCore.QSize(300, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/vertex_tools/vertex.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        VertexDialog.setWindowIcon(icon)
        self.buttonBox = QtGui.QDialogButtonBox(VertexDialog)
        self.buttonBox.setGeometry(QtCore.QRect(115, 360, 176, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vertexTWidget = QtGui.QTableWidget(VertexDialog)
        self.vertexTWidget.setGeometry(QtCore.QRect(15, 40, 271, 261))
        self.vertexTWidget.setObjectName(_fromUtf8("vertexTWidget"))
        self.vertexTWidget.setColumnCount(3)
        self.vertexTWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.vertexTWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.vertexTWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.vertexTWidget.setHorizontalHeaderItem(2, item)
        self.reverseOrderButton = QtGui.QPushButton(VertexDialog)
        self.reverseOrderButton.setGeometry(QtCore.QRect(10, 310, 196, 32))
        self.reverseOrderButton.setObjectName(_fromUtf8("reverseOrderButton"))
        self.label = QtGui.QLabel(VertexDialog)
        self.label.setGeometry(QtCore.QRect(20, 25, 161, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(VertexDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VertexDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VertexDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(VertexDialog)

    def retranslateUi(self, VertexDialog):
        VertexDialog.setWindowTitle(_translate("VertexDialog", "View / Edit Vertices", None))
        item = self.vertexTWidget.horizontalHeaderItem(0)
        item.setText(_translate("VertexDialog", "ID", None))
        item = self.vertexTWidget.horizontalHeaderItem(1)
        item.setText(_translate("VertexDialog", "X", None))
        item = self.vertexTWidget.horizontalHeaderItem(2)
        item.setText(_translate("VertexDialog", "Y", None))
        self.reverseOrderButton.setText(_translate("VertexDialog", "Revert Coordinate Order", None))
        self.label.setText(_translate("VertexDialog", "Vertex Coordinates", None))

