__author__ = 'mwagner'

from ..view.Ui_SnapToGridWidget import Ui_SnapToGridWidget
from qgis.core import QgsMapLayerRegistry, QgsMapLayer, QgsMessageLog
from PyQt4.Qt import Qt, pyqtSlot, QReadWriteLock, QReadLocker
from PyQt4.QtGui import QDockWidget, QListWidgetItem, QMessageBox
from ..model.VertexToolsError import *
from SnapToGrid import *


class SnapToGridWidget(QDockWidget, Ui_SnapToGridWidget):

    def __init__(self, plugin, parent=None):

        super(SnapToGridWidget,  self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin

        self.layer_count = 0
        self.threads = dict()
        self.lock = QReadWriteLock()

    @pyqtSlot()
    def on_addLayersButton_clicked(self):

        layers = self.plugin.iface.legendInterface().selectedLayers()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and not layer.isReadOnly():
                layer_id = layer.id()
                if self.__layer_in_list(layer_id):
                    continue
                name = layer.name()
                item = QListWidgetItem(name)
                item.setData(Qt.UserRole, layer_id)
                self.snapLayersLWidget.addItem(item)

    @pyqtSlot()
    def on_removeLayerButton_clicked(self):

        for item in self.snapLayersLWidget.selectedItems():
            item = self.snapLayersLWidget.takeItem(self.snapLayersLWidget.row(item))
            del item

    @pyqtSlot()
    def on_removeAllLayersButton_clicked(self):

        for row in range(0, self.snapLayersLWidget.count()):
            item = self.snapLayersLWidget.takeItem(0)
            del item

    @pyqtSlot()
    def on_snapButton_clicked(self):

        self.layer_count = 0
        self.threads = dict()
        for row in range(0, self.snapLayersLWidget.count()):
            layer_id = self.snapLayersLWidget.item(row).data(Qt.UserRole)
            thread = SnapToGrid(layer_id)
            thread.finished.connect(self.finished)
            thread.progressed.connect(self.progressed)
            self.threads[layer_id] = thread
            self.layer_count += 1
            thread.start()

    @pyqtSlot()
    def on_cancelButton_clicked(self):

        for layer_id in self.threads:
            thread = self.threads[layer_id]
            if thread.isRunning():
                thread.stop()
                self.finished(layer_id, False)

    @pyqtSlot(str, bool)
    def finished(self, layer_id, completed):

        with QReadLocker(self.lock):
            self.layer_count -= 1

        thread = self.threads[layer_id]
        thread.wait()

        if self.layer_count == 0:
            if completed:
                QMessageBox.information(self, "Snapping", "Snapping completed")
            else:
                QMessageBox.information(self, "Snapping", "Snapping cancelled")

    @pyqtSlot(str, int)
    def progressed(self, layer_id, progress_val):

        for row in range(0, self.snapLayersLWidget.count()):
            layer_id2 = self.snapLayersLWidget.item(row).data(Qt.UserRole)
            if layer_id2 == layer_id:
                item = self.snapLayersLWidget.item(row)
                break

        text = item.text()
        idx = text.find('[')
        progress_rate = (float(progress_val)*100)/5000000
        if idx != -1:
            text = text[0:idx-1]
        item.setText(text + ' [{0:6.2f} %]'.format(progress_rate))

    def __layer_in_list(self, layer_id):

        for row in range(0, self.snapLayersLWidget.count()):
            layer_id2 = self.snapLayersLWidget.item(row).data(Qt.UserRole)
            if layer_id2 == layer_id:
                return True

        return False
