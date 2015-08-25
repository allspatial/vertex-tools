__author__ = 'mwagner'

from ..view.Ui_SnapToGridWidget import Ui_SnapToGridWidget
from qgis.core import QgsMapLayerRegistry, QgsMapLayer, QgsVectorDataProvider
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
        self.remaining_layer_count = 0
        self.threads = dict()
        self.layers = dict()
        self.lock = QReadWriteLock()
        self.ideal_thread_count = QThread.idealThreadCount()-1

    @pyqtSlot()
    def on_addLayersButton_clicked(self):

        layers = self.plugin.iface.legendInterface().selectedLayers()
        for layer in layers:
            caps = layer.dataProvider().capabilities()
            if layer.type() == QgsMapLayer.VectorLayer and not layer.isReadOnly() and caps & QgsVectorDataProvider.ChangeGeometries:
                layer_id = layer.id()
                if self.__layer_in_list(layer_id):
                    continue
                name = layer.name()
                item = QListWidgetItem(name)
                item.setData(Qt.UserRole, layer_id)
                self.snapLayersLWidget.addItem(item)
                self.layers[layer_id] = layer

    @pyqtSlot()
    def on_removeLayerButton_clicked(self):

        for item in self.snapLayersLWidget.selectedItems():
            item = self.snapLayersLWidget.takeItem(self.snapLayersLWidget.row(item))
            layer_id = item.data(Qt.UserRole)
            del self.layers[layer_id]
            del item

    @pyqtSlot()
    def on_removeAllLayersButton_clicked(self):

        for row in range(0, self.snapLayersLWidget.count()):
            item = self.snapLayersLWidget.takeItem(0)
            del item

        self.layers.clear()

    @pyqtSlot()
    def on_snapButton_clicked(self):

        if self.snapLayersLWidget.count() == 0:
            return

        if QMessageBox.question(None, self.tr('Snap To Grid'), self.tr('Snapping to grid might change the geometries significantly depending on the grid size set. Do you want to continue?'), QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return

        self.snapButton.setEnabled(False)
        self.removeLayerButton.setEnabled(False)
        self.removeAllLayersButton.setEnabled(False)
        self.addLayersButton.setEnabled(False)

        self.layer_count = 0
        self.remaining_layer_count = 0
        self.threads.clear()

        QgsMessageLog.logMessage(self.tr('Ideal Thread Count: {0}').format(self.ideal_thread_count), self.tr('Vertex Tools'), QgsMessageLog.INFO)

        for row in range(0, self.snapLayersLWidget.count()):

            self.__create_thread(row)
            if self.layer_count >= self.ideal_thread_count:
                self.remaining_layer_count = self.snapLayersLWidget.count() - self.layer_count
                break

    def __create_thread(self, row):

        grid_size = self.gridSizeSBox.value()
        layer_id = self.snapLayersLWidget.item(row).data(Qt.UserRole)
        snap_extent = self.__snap_extent(layer_id)
        thread = SnapToGrid(self.plugin, layer_id, snap_extent, grid_size, self.plugin.iface.mainWindow())
        thread.run_finished.connect(self.finished)
        thread.run_progressed.connect(self.progressed)
        self.threads[layer_id] = thread
        with QReadLocker(self.lock):
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

        if self.remaining_layer_count > 0:
            self.__create_thread(self.snapLayersLWidget.count()-self.remaining_layer_count)
            with QReadLocker(self.lock):
                self.remaining_layer_count -= 1

        if self.layer_count == 0:
            if completed:
                if self.plugin.iface.mapCanvas().isCachingEnabled():
                    self.layers[layer_id].setCacheImage(None)
                else:
                    self.plugin.iface.mapCanvas().refresh()
                QMessageBox.information(self, self.tr("Snapping"), self.tr("Snapping completed."))
            else:
                QMessageBox.information(self, self.tr("Snapping"), self.tr("Snapping cancelled."))

            self.snapButton.setEnabled(True)
            self.removeLayerButton.setEnabled(True)
            self.removeAllLayersButton.setEnabled(True)
            self.addLayersButton.setEnabled(True)

    @pyqtSlot(str, int, int)
    def progressed(self, layer_id, progress_val, total_val):

        for row in range(0, self.snapLayersLWidget.count()):
            layer_id2 = self.snapLayersLWidget.item(row).data(Qt.UserRole)
            if layer_id2 == layer_id:
                item = self.snapLayersLWidget.item(row)
                break

        text = item.text()
        idx = text.find('[')
        progress_rate = (float(progress_val)*100) / total_val
        if idx != -1:
            text = text[0:idx-1]
        item.setText(text + ' [{0:6.2f} %]'.format(progress_rate))

    def __layer_in_list(self, layer_id):

        for row in range(0, self.snapLayersLWidget.count()):
            layer_id2 = self.snapLayersLWidget.item(row).data(Qt.UserRole)
            if layer_id2 == layer_id:
                return True

        return False

    def __snap_extent(self, layer_id):

        if self.mapExtentRButton.isChecked():
            return self.plugin.map_canvas.extent()
        else:
            layer = QgsMapLayerRegistry.instance().mapLayer(layer_id)
            return layer.extent()
