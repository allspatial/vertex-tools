__author__ = 'mwagner'

from qgis.core import QgsVectorLayer, QgsGeometry, QgsFeature, QgsMapLayerRegistry, QgsPoint, QgsSnapper, QgsSpatialIndex, QgsFeatureRequest, QgsMessageLog, QGis
from PyQt4.Qt import QThread, pyqtSignal, QMutex, QMutexLocker, QReadWriteLock, QReadLocker


class SnapToGrid(QThread):

    run_finished = pyqtSignal(str, bool)
    run_progressed = pyqtSignal(str, int, int)

    def __init__(self, layer_id, snap_extent, grid_size, parent=None):

        super(SnapToGrid, self).__init__(parent)
        self.layer_id = layer_id
        self.snap_extent = snap_extent
        self.grid_size = grid_size
        self.stopped = False
        self.mutex = QMutex()
        self.completed = False

    def run(self):

        self.snap()
        self.stop()
        self.run_finished.emit(self.layer_id, self.completed)

    def stop(self):

        with QMutexLocker(self.mutex):
            self.stopped = True

    def snap2(self):

        limit = 5000000
        for x in range(0, limit):
            with QMutexLocker(self.mutex):
                if self.stopped:
                    return

            if x % 500 == 0:
                self.run_progressed.emit(self.layer_id, x, limit)

        self.completed = True

    def snap(self):

        orig_layer = QgsMapLayerRegistry.instance().mapLayer(self.layer_id)
        layer = QgsVectorLayer(orig_layer.source(), orig_layer.name(), orig_layer.providerType())
        geom_type = layer.geometryType()
        wkb_type = layer.wkbType()

        layer.startEditing()
        request = QgsFeatureRequest().setFilterRect(self.snap_extent)
        total_features = 0
        for feature in layer.getFeatures(request):
            total_features += 1

        QgsMessageLog.logMessage('Total features: {0}'.format(total_features), 'Vertex Tools', QgsMessageLog.WARNING)

        count = 0
        for feature in layer.getFeatures(request):
            with QMutexLocker(self.mutex):
                if self.stopped:
                    layer.rollback()
                    return

            if geom_type == QGis.Point:
                self.__point_grid(layer, feature, wkb_type)

            if count % 500 == 0:
                layer.commitChanges()
                layer.startEditing()

            count += 1

            self.run_progressed.emit(self.layer_id, count, total_features)

        layer.commitChanges()

        self.completed = True

    def __point_grid(self, layer, feature, wkb_type):

        points = list()
        if wkb_type == QGis.WKBMultiPoint or wkb_type == QGis.WKBMultiPoint25D:
            pass
        else:
            points.append(feature.geometry().asPoint())

        snapped_points = self.__points_to_grid(points)

        if wkb_type == QGis.WKBMultiPoint or wkb_type == QGis.WKBMultiPoint25D:
            pass
        else:
            geom = QgsGeometry.fromPoint(snapped_points[0])

        layer.dataProvider().changeGeometryValues({feature.id(): geom})

    def __points_to_grid(self, points, remove_duplicates=True):

        snapped_points = list()

        for point in points:

            x = round(point.x() / self.grid_size) * self.grid_size
            y = round(point.y() / self.grid_size) * self.grid_size

            if remove_duplicates and len(snapped_points) > 0:
                prev_point = snapped_points[len(snapped_points)-1]
                if prev_point.x() == x and prev_point.y() == y:
                    continue

            snapped_points.append(QgsPoint(x, y))

        return snapped_points
