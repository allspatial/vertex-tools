__author__ = 'mwagner'

from PyQt4.Qt import Qt
from PyQt4.QtGui import QDialog, QIcon
from ..view.Ui_VertexDialog import Ui_VertexDialog
from ..model.VertexToolsError import *


class VertexDialog(QDialog, Ui_VertexDialog):

    def __init__(self, plugin, parent=None):

        super(VertexDialog,  self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.plugin = plugin
        self.setupUi(self)

        self.helpButton.setIcon(self.plugin.getIcon("help.gif"))
        self.setWindowIcon(QIcon(":beninCad/info.png"))