__author__ = 'mwagner'

from qgis.core import QgsVectorLayer, QgsMapLayerRegistry, QgsMessageLog
from PyQt4.Qt import QThread, pyqtSignal, QMutex, QMutexLocker, QDir, QFile


class RestoreGeometry(QThread):

    run_finished = pyqtSignal(str, bool)
    run_progressed = pyqtSignal(str, int, int)
    report_message = pyqtSignal(str, str)

    def __init__(self, plugin, backup_path, parent=None):

        super(RestoreGeometry, self).__init__(parent)
        self.plugin = plugin
        self.stopped = False
        self.mutex = QMutex()
        self.completed = False
        self.layer_id = None
        self.backup_path = backup_path

    def initialize(self, layer_id):

        self.layer_id = layer_id
        self.stopped = False
        self.completed = False

    def run(self):

        self.__restore_geometries()
        self.stop()
        self.run_finished.emit(self.layer_id, self.completed)

    def stop(self):

        with QMutexLocker(self.mutex):
            self.stopped = True

    def __restore_geometries(self):

        src_file_name = self.backup_path + QDir.separator() + self.layer_id + '.shp'
        if not QFile.exists(src_file_name):
            self.report_message.emit(self.layer_id, 'no backup file')
            self.completed = True
            return

        self.report_message.emit(self.layer_id, 'preparing ...')

        orig_layer = QgsMapLayerRegistry.instance().mapLayer(self.layer_id)
        # create a copy of the layer just for editing
        layer = QgsVectorLayer(orig_layer.source(), orig_layer.name(), orig_layer.providerType())
        layer.startEditing()
        src_layer = QgsVectorLayer(src_file_name, layer.name(), 'ogr')
        total_features = src_layer.featureCount()

        QgsMessageLog.logMessage(self.plugin.tr('Features to be restored in layer <{0}>: {1}').
                                 format(orig_layer.name(), total_features), self.plugin.tr('Vertex Tools'),
                                 QgsMessageLog.INFO)
        if total_features == 0:
            self.report_message.emit(self.layer_id, 'no features to restore')

        count = 0
        for feature in src_layer.getFeatures():
            with QMutexLocker(self.mutex):
                if self.stopped:
                    layer.rollBack()
                    return

            layer.changeGeometry(feature.id(), feature.geometry())

            count += 1
            self.run_progressed.emit(self.layer_id, count, total_features)

        layer.commitChanges()

        self.completed = True
