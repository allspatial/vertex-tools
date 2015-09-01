__author__ = 'mwagner'

from ..view.Ui_SnapToGridWidget import Ui_SnapToGridWidget
from qgis.core import QgsMapLayerRegistry, QgsMapLayer, QgsVectorDataProvider
from PyQt4.Qt import Qt, pyqtSlot, QReadWriteLock, QReadLocker, QSettings
from PyQt4.QtGui import QDockWidget, QListWidgetItem, QMessageBox, QFileDialog
from SnapToGrid import *
from RestoreGeometry import *


class SnapToGridWidget(QDockWidget, Ui_SnapToGridWidget):

    def __init__(self, plugin, parent=None):

        super(SnapToGridWidget,  self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin
        self.remaining_layer_count = 0
        self.snap_thread = None
        self.restore_geom_thread = None
        self.layers = dict()
        self.selected_layers = None
        self.lock = QReadWriteLock()
        self.map_extent = None
        self.backup_folder_button.setIcon(self.plugin.get_icon("folder.png"))
        self.__set_backup_path()

    @pyqtSlot()
    def on_add_layers_button_clicked(self):

        layers = self.plugin.iface.legendInterface().selectedLayers()
        for layer in layers:
            caps = layer.dataProvider().capabilities()
            if layer.type() == QgsMapLayer.VectorLayer and not layer.isReadOnly() \
                    and caps & QgsVectorDataProvider.ChangeGeometries:
                layer_id = layer.id()
                if self.__layer_in_list(layer_id):
                    continue
                name = layer.name()
                item = QListWidgetItem(name)
                item.setData(Qt.UserRole, layer_id)
                self.snap_layers_lwidget.addItem(item)
                self.layers[layer_id] = layer

    @pyqtSlot()
    def on_remove_layer_button_clicked(self):

        for item in self.snap_layers_lwidget.selectedItems():
            item = self.snap_layers_lwidget.takeItem(self.snap_layers_lwidget.row(item))
            layer_id = item.data(Qt.UserRole)
            del self.layers[layer_id]
            del item

    @pyqtSlot()
    def on_remove_all_layers_button_clicked(self):

        for row in range(0, self.snap_layers_lwidget.count()):
            item = self.snap_layers_lwidget.takeItem(0)
            del item

        self.layers.clear()

    @pyqtSlot()
    def on_restore_button_clicked(self):

        if len(self.snap_layers_lwidget.selectedItems()) == 0:
            QMessageBox.information(self, self.tr("Restore Geometries"), self.tr("No layer(s) selected."))
            return

        if QMessageBox.question(None, self.tr('Restore Geometries'),
                                self.tr('Geometries will be restored for the selected layer(s).'
                                        ' Do you want to continue?')
                                , QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return

        self.__reset_progress()

        self.restore_button.setEnabled(False)
        self.snap_button.setEnabled(False)
        self.cancel_snap_button.setEnabled(False)
        self.remove_layer_button.setEnabled(False)
        self.remove_all_layers_button.setEnabled(False)
        self.add_layers_button.setEnabled(False)
        self.snap_settings_gbox.setEnabled(False)
        self.create_backup_gbox.setEnabled(False)

        backup_path = self.backup_folder_edit.text()
        self.restore_geom_thread = RestoreGeometry(self.plugin, backup_path, self.plugin.iface.mainWindow())
        self.restore_geom_thread.run_finished.connect(self.restore_geom_finished)
        self.restore_geom_thread.run_progressed.connect(self.progressed)
        self.restore_geom_thread.report_message.connect(self.report_message)

        self.selected_layers = list()
        for item in self.snap_layers_lwidget.selectedItems():
            layer_id = item.data(Qt.UserRole)
            self.selected_layers.append(layer_id)

        self.remaining_layer_count = len(self.selected_layers) - 1
        self.__run_restore_geom_thread(0)

    def __run_restore_geom_thread(self, row):

        layer_id = self.selected_layers[row]
        self.restore_geom_thread.initialize(layer_id)
        self.restore_geom_thread.start()

    @pyqtSlot(str, bool)
    def restore_geom_finished(self, layer_id, completed):

        self.restore_geom_thread.wait()

        if completed:

            if self.plugin.iface.mapCanvas().isCachingEnabled():
                self.layers[layer_id].setCacheImage(None)
            else:
                self.plugin.iface.mapCanvas().refresh()

            if self.remaining_layer_count > 0:
                row = len(self.selected_layers)-self.remaining_layer_count
                with QReadLocker(self.lock):
                    self.remaining_layer_count -= 1
                self.__run_restore_geom_thread(row)
                return

            QMessageBox.information(self, self.tr("Restoring Geometries"), self.tr("Restoring completed."))
        else:
            QMessageBox.information(self, self.tr("Restoring Geometries"), self.tr("Restoring cancelled."))

        self.restore_button.setEnabled(True)
        self.snap_button.setEnabled(True)
        self.cancel_snap_button.setEnabled(True)
        self.remove_layer_button.setEnabled(True)
        self.remove_all_layers_button.setEnabled(True)
        self.add_layers_button.setEnabled(True)
        self.snap_settings_gbox.setEnabled(True)
        self.create_backup_gbox.setEnabled(True)

        del self.restore_geom_thread
        self.restore_geom_thread = None

    @pyqtSlot()
    def on_cancel_restore_button_clicked(self):

        if not self.restore_geom_thread:
            return

        if self.restore_geom_thread.isRunning():
            self.restore_geom_thread.stop()

    @pyqtSlot()
    def on_snap_button_clicked(self):

        if self.snap_layers_lwidget.count() == 0:
            return

        if QMessageBox.question(None, self.tr('Snap To Grid'),
                                self.tr('Snapping to grid might change the geometries significantly'
                                        ' depending on the grid size set. Do you want to continue?'),
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return

        self.__reset_progress()

        self.snap_button.setEnabled(False)
        self.remove_layer_button.setEnabled(False)
        self.remove_all_layers_button.setEnabled(False)
        self.add_layers_button.setEnabled(False)
        self.snap_settings_gbox.setEnabled(False)
        self.create_backup_gbox.setEnabled(False)
        self.restore_geom_gbox.setEnabled(False)

        grid_size = self.grid_size_sbox.value()
        self.map_extent = self.plugin.map_canvas.extent()
        create_backup = self.create_backup_gbox.isChecked()
        backup_path = self.backup_folder_edit.text()
        self.snap_thread = SnapToGrid(self.plugin, grid_size, create_backup, backup_path,
                                      self.plugin.iface.mainWindow())
        self.snap_thread.run_finished.connect(self.snapping_finished)
        self.snap_thread.run_progressed.connect(self.progressed)
        self.snap_thread.report_message.connect(self.report_message)

        self.remaining_layer_count = self.snap_layers_lwidget.count() - 1
        self.__run_snap_thread(0)

    def __run_snap_thread(self, row):

        layer_id = self.snap_layers_lwidget.item(row).data(Qt.UserRole)
        snap_extent = self.__snap_extent(layer_id)

        self.snap_thread.initialize(layer_id, snap_extent)
        self.snap_thread.start()

    @pyqtSlot()
    def on_cancel_snap_button_clicked(self):

        if not self.snap_thread:
            return

        if self.snap_thread.isRunning():
            self.snap_thread.stop()

    @pyqtSlot(str, bool)
    def snapping_finished(self, layer_id, completed):

        self.snap_thread.wait()

        if completed:

            if self.plugin.iface.mapCanvas().isCachingEnabled():
                self.layers[layer_id].setCacheImage(None)
            else:
                self.plugin.iface.mapCanvas().refresh()

            if self.remaining_layer_count > 0:
                row = self.snap_layers_lwidget.count()-self.remaining_layer_count
                with QReadLocker(self.lock):
                    self.remaining_layer_count -= 1
                self.__run_snap_thread(row)
                return

            QMessageBox.information(self, self.tr("Snapping"), self.tr("Snapping completed."))
        else:
            QMessageBox.information(self, self.tr("Snapping"), self.tr("Snapping cancelled."))

        self.snap_button.setEnabled(True)
        self.remove_layer_button.setEnabled(True)
        self.remove_all_layers_button.setEnabled(True)
        self.add_layers_button.setEnabled(True)
        self.snap_settings_gbox.setEnabled(True)
        self.create_backup_gbox.setEnabled(True)
        self.restore_geom_gbox.setEnabled(True)

        del self.snap_thread
        self.snap_thread = None

    @pyqtSlot(str, int, int)
    def progressed(self, layer_id, progress_val, total_val):

        for row in range(0, self.snap_layers_lwidget.count()):
            layer_id2 = self.snap_layers_lwidget.item(row).data(Qt.UserRole)
            if layer_id2 == layer_id:
                item = self.snap_layers_lwidget.item(row)
                break

        text = item.text()
        idx = text.find('[')
        progress_rate = (float(progress_val)*100) / total_val
        if idx != -1:
            text = text[0:idx-1]
        item.setText(text + ' [{0:6.2f} %]'.format(progress_rate))

    @pyqtSlot(str, str)
    def report_message(self, layer_id, message):

        for row in range(0, self.snap_layers_lwidget.count()):
            layer_id2 = self.snap_layers_lwidget.item(row).data(Qt.UserRole)
            if layer_id2 == layer_id:
                item = self.snap_layers_lwidget.item(row)
                break

        text = item.text()
        idx = text.find('[')
        if idx != -1:
            text = text[0:idx-1]
        item.setText(text + self.tr(' [{0}]').format(message))

    def __layer_in_list(self, layer_id):

        for row in range(0, self.snap_layers_lwidget.count()):
            layer_id2 = self.snap_layers_lwidget.item(row).data(Qt.UserRole)
            if layer_id2 == layer_id:
                return True

        return False

    def __snap_extent(self, layer_id):

        if self.map_extent_rbutton.isChecked():
            return self.map_extent
        else:
            layer = QgsMapLayerRegistry.instance().mapLayer(layer_id)
            return layer.extent()

    def __set_backup_path(self):

        settings = QSettings("GCI", "vertex-tools")
        settings.beginGroup("BackupSettings")
        default_path = QDir.tempPath()
        backup_path = settings.value("backup_path", default_path)
        self.backup_folder_edit.setText(backup_path)
        settings.endGroup()

    @pyqtSlot()
    def on_backup_folder_button_clicked(self):

        backup_path = self.backup_folder_edit.text()
        if len(backup_path) == 0:
            backup_path = QDir.tempPath()

        backup_path = QFileDialog.getExistingDirectory(self, self.tr("Select Backup Folder"), backup_path,
                                                       QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if len(backup_path) == 0:
            return

        self.backup_folder_edit.setText(backup_path)
        settings = QSettings("GCI", "vertex-tools")
        settings.beginGroup("BackupSettings")
        settings.setValue("backup_path", backup_path)
        settings.endGroup()

    def __reset_progress(self):

        for row in range(0, self.snap_layers_lwidget.count()):
            item = self.snap_layers_lwidget.item(row)
            text = item.text()
            idx = text.find('[')
            if idx != -1:
                text = text[0:idx-1]
            item.setText(text)