# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SnapToGridDialog.ui'
#
# Created: Tue Jul 14 17:01:49 2015
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

class Ui_SnapToGridDialog(object):
    def setupUi(self, SnapToGridDialog):
        SnapToGridDialog.setObjectName(_fromUtf8("SnapToGridDialog"))
        SnapToGridDialog.resize(500, 450)
        SnapToGridDialog.setMinimumSize(QtCore.QSize(500, 450))
        SnapToGridDialog.setMaximumSize(QtCore.QSize(500, 450))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/vertex_tools/grid.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SnapToGridDialog.setWindowIcon(icon)
        self.availableLayersLWidget = QtGui.QListWidget(SnapToGridDialog)
        self.availableLayersLWidget.setGeometry(QtCore.QRect(15, 40, 206, 241))
        self.availableLayersLWidget.setObjectName(_fromUtf8("availableLayersLWidget"))
        self.snapLayersLWidget = QtGui.QListWidget(SnapToGridDialog)
        self.snapLayersLWidget.setGeometry(QtCore.QRect(280, 40, 206, 241))
        self.snapLayersLWidget.setObjectName(_fromUtf8("snapLayersLWidget"))
        self.addLayerButton = QtGui.QPushButton(SnapToGridDialog)
        self.addLayerButton.setGeometry(QtCore.QRect(225, 60, 51, 32))
        self.addLayerButton.setObjectName(_fromUtf8("addLayerButton"))
        self.addAllLayersButton = QtGui.QPushButton(SnapToGridDialog)
        self.addAllLayersButton.setGeometry(QtCore.QRect(225, 95, 51, 32))
        self.addAllLayersButton.setObjectName(_fromUtf8("addAllLayersButton"))
        self.removeLayerButton = QtGui.QPushButton(SnapToGridDialog)
        self.removeLayerButton.setGeometry(QtCore.QRect(225, 195, 51, 32))
        self.removeLayerButton.setObjectName(_fromUtf8("removeLayerButton"))
        self.removeAllLayersButton = QtGui.QPushButton(SnapToGridDialog)
        self.removeAllLayersButton.setGeometry(QtCore.QRect(225, 230, 51, 32))
        self.removeAllLayersButton.setObjectName(_fromUtf8("removeAllLayersButton"))
        self.label = QtGui.QLabel(SnapToGridDialog)
        self.label.setGeometry(QtCore.QRect(20, 25, 121, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(SnapToGridDialog)
        self.label_2.setGeometry(QtCore.QRect(280, 25, 206, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.snapButton = QtGui.QPushButton(SnapToGridDialog)
        self.snapButton.setGeometry(QtCore.QRect(260, 410, 115, 32))
        self.snapButton.setObjectName(_fromUtf8("snapButton"))
        self.closeButton = QtGui.QPushButton(SnapToGridDialog)
        self.closeButton.setGeometry(QtCore.QRect(380, 410, 115, 32))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.groupBox = QtGui.QGroupBox(SnapToGridDialog)
        self.groupBox.setGeometry(QtCore.QRect(15, 290, 471, 111))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layerRButton = QtGui.QRadioButton(self.groupBox)
        self.layerRButton.setGeometry(QtCore.QRect(30, 75, 126, 20))
        self.layerRButton.setObjectName(_fromUtf8("layerRButton"))
        self.buttonGroup = QtGui.QButtonGroup(SnapToGridDialog)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.layerRButton)
        self.mapExtentRButton = QtGui.QRadioButton(self.groupBox)
        self.mapExtentRButton.setGeometry(QtCore.QRect(30, 50, 166, 20))
        self.mapExtentRButton.setChecked(True)
        self.mapExtentRButton.setObjectName(_fromUtf8("mapExtentRButton"))
        self.buttonGroup.addButton(self.mapExtentRButton)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(300, 30, 121, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridSizeSBox = QtGui.QDoubleSpinBox(self.groupBox)
        self.gridSizeSBox.setGeometry(QtCore.QRect(300, 50, 121, 24))
        self.gridSizeSBox.setDecimals(3)
        self.gridSizeSBox.setMinimum(0.001)
        self.gridSizeSBox.setMaximum(5.0)
        self.gridSizeSBox.setSingleStep(0.01)
        self.gridSizeSBox.setObjectName(_fromUtf8("gridSizeSBox"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(30, 30, 126, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.retranslateUi(SnapToGridDialog)
        QtCore.QMetaObject.connectSlotsByName(SnapToGridDialog)
        SnapToGridDialog.setTabOrder(self.availableLayersLWidget, self.addLayerButton)
        SnapToGridDialog.setTabOrder(self.addLayerButton, self.addAllLayersButton)
        SnapToGridDialog.setTabOrder(self.addAllLayersButton, self.snapLayersLWidget)
        SnapToGridDialog.setTabOrder(self.snapLayersLWidget, self.removeLayerButton)
        SnapToGridDialog.setTabOrder(self.removeLayerButton, self.removeAllLayersButton)
        SnapToGridDialog.setTabOrder(self.removeAllLayersButton, self.mapExtentRButton)
        SnapToGridDialog.setTabOrder(self.mapExtentRButton, self.layerRButton)
        SnapToGridDialog.setTabOrder(self.layerRButton, self.gridSizeSBox)
        SnapToGridDialog.setTabOrder(self.gridSizeSBox, self.snapButton)
        SnapToGridDialog.setTabOrder(self.snapButton, self.closeButton)

    def retranslateUi(self, SnapToGridDialog):
        SnapToGridDialog.setWindowTitle(_translate("SnapToGridDialog", "Snap to Grid", None))
        self.addLayerButton.setText(_translate("SnapToGridDialog", ">", None))
        self.addAllLayersButton.setText(_translate("SnapToGridDialog", ">>", None))
        self.removeLayerButton.setText(_translate("SnapToGridDialog", "<", None))
        self.removeAllLayersButton.setText(_translate("SnapToGridDialog", "<<", None))
        self.label.setText(_translate("SnapToGridDialog", "Available Layers", None))
        self.label_2.setText(_translate("SnapToGridDialog", "Layers To Be Snapped", None))
        self.snapButton.setText(_translate("SnapToGridDialog", "Snap", None))
        self.closeButton.setText(_translate("SnapToGridDialog", "Close", None))
        self.groupBox.setTitle(_translate("SnapToGridDialog", "Snap Settings", None))
        self.layerRButton.setText(_translate("SnapToGridDialog", "Layer Extent", None))
        self.mapExtentRButton.setText(_translate("SnapToGridDialog", "Current Map View", None))
        self.label_3.setText(_translate("SnapToGridDialog", "Grid Size [m]", None))
        self.label_4.setText(_translate("SnapToGridDialog", "Snap Extent:", None))

