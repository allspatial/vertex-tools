__author__ = 'mwagner'

from PyQt4.Qt import Qt
from PyQt4.QtGui import QDialog, QIcon
from ..view.Ui_SnapToGridDialog import Ui_SnapToGridDialog
from ..model.VertexToolsError import *


class SnapToGridDialog(QDialog, Ui_SnapToGridDialog):

    def __init__(self, plugin, parent=None):

        super(SnapToGridDialog,  self).__init__(parent)

        self.plugin = plugin
        self.setupUi(self)
