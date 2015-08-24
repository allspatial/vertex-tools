# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SnapToGridWidget.ui'
#
# Created: Mon Aug 24 09:39:46 2015
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

class Ui_SnapToGridWidget(object):
    def setupUi(self, SnapToGridWidget):
        SnapToGridWidget.setObjectName(_fromUtf8("SnapToGridWidget"))
        SnapToGridWidget.resize(288, 561)
        SnapToGridWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.snapLayersLWidget = QtGui.QListWidget(self.dockWidgetContents)
        self.snapLayersLWidget.setGeometry(QtCore.QRect(20, 70, 251, 201))
        self.snapLayersLWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.snapLayersLWidget.setObjectName(_fromUtf8("snapLayersLWidget"))
        self.label_5 = QtGui.QLabel(self.dockWidgetContents)
        self.label_5.setGeometry(QtCore.QRect(20, 50, 206, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.groupBox_2 = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 325, 251, 166))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.layerRButton = QtGui.QRadioButton(self.groupBox_2)
        self.layerRButton.setGeometry(QtCore.QRect(10, 75, 126, 20))
        self.layerRButton.setObjectName(_fromUtf8("layerRButton"))
        self.mapExtentRButton = QtGui.QRadioButton(self.groupBox_2)
        self.mapExtentRButton.setGeometry(QtCore.QRect(10, 50, 231, 20))
        self.mapExtentRButton.setChecked(True)
        self.mapExtentRButton.setObjectName(_fromUtf8("mapExtentRButton"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(15, 105, 121, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridSizeSBox = QtGui.QDoubleSpinBox(self.groupBox_2)
        self.gridSizeSBox.setGeometry(QtCore.QRect(15, 125, 121, 24))
        self.gridSizeSBox.setDecimals(3)
        self.gridSizeSBox.setMinimum(0.001)
        self.gridSizeSBox.setMaximum(20.0)
        self.gridSizeSBox.setSingleStep(0.01)
        self.gridSizeSBox.setObjectName(_fromUtf8("gridSizeSBox"))
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(10, 30, 126, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.snapButton = QtGui.QPushButton(self.dockWidgetContents)
        self.snapButton.setGeometry(QtCore.QRect(30, 505, 115, 32))
        self.snapButton.setObjectName(_fromUtf8("snapButton"))
        self.cancelButton = QtGui.QPushButton(self.dockWidgetContents)
        self.cancelButton.setGeometry(QtCore.QRect(150, 505, 115, 32))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.removeLayerButton = QtGui.QPushButton(self.dockWidgetContents)
        self.removeLayerButton.setGeometry(QtCore.QRect(15, 275, 131, 32))
        self.removeLayerButton.setObjectName(_fromUtf8("removeLayerButton"))
        self.removeAllLayersButton = QtGui.QPushButton(self.dockWidgetContents)
        self.removeAllLayersButton.setGeometry(QtCore.QRect(145, 275, 131, 32))
        self.removeAllLayersButton.setObjectName(_fromUtf8("removeAllLayersButton"))
        self.addLayersButton = QtGui.QPushButton(self.dockWidgetContents)
        self.addLayersButton.setGeometry(QtCore.QRect(15, 10, 261, 32))
        self.addLayersButton.setObjectName(_fromUtf8("addLayersButton"))
        SnapToGridWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(SnapToGridWidget)
        QtCore.QMetaObject.connectSlotsByName(SnapToGridWidget)
        SnapToGridWidget.setTabOrder(self.addLayersButton, self.snapLayersLWidget)
        SnapToGridWidget.setTabOrder(self.snapLayersLWidget, self.removeLayerButton)
        SnapToGridWidget.setTabOrder(self.removeLayerButton, self.removeAllLayersButton)
        SnapToGridWidget.setTabOrder(self.removeAllLayersButton, self.mapExtentRButton)
        SnapToGridWidget.setTabOrder(self.mapExtentRButton, self.layerRButton)
        SnapToGridWidget.setTabOrder(self.layerRButton, self.gridSizeSBox)
        SnapToGridWidget.setTabOrder(self.gridSizeSBox, self.snapButton)
        SnapToGridWidget.setTabOrder(self.snapButton, self.cancelButton)

    def retranslateUi(self, SnapToGridWidget):
        SnapToGridWidget.setWindowTitle(_translate("SnapToGridWidget", "Snap To Grid", None))
        self.label_5.setText(_translate("SnapToGridWidget", "Layers To Be Snapped", None))
        self.groupBox_2.setTitle(_translate("SnapToGridWidget", "Snap Settings", None))
        self.layerRButton.setText(_translate("SnapToGridWidget", "Layer Extent", None))
        self.mapExtentRButton.setText(_translate("SnapToGridWidget", "Current Map View (Intersecting)", None))
        self.label_6.setText(_translate("SnapToGridWidget", "Grid Size [m]", None))
        self.label_7.setText(_translate("SnapToGridWidget", "Snap Extent:", None))
        self.snapButton.setText(_translate("SnapToGridWidget", "Snap", None))
        self.cancelButton.setText(_translate("SnapToGridWidget", "Cancel", None))
        self.removeLayerButton.setText(_translate("SnapToGridWidget", "Remove Selected", None))
        self.removeAllLayersButton.setText(_translate("SnapToGridWidget", "Remove All", None))
        self.addLayersButton.setText(_translate("SnapToGridWidget", "Add Selected TOC Layers", None))

