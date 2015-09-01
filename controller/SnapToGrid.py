__author__ = 'mwagner'

from qgis.core import QgsVectorLayer, QgsGeometry, QgsMapLayerRegistry, QgsPoint, QgsFeatureRequest,\
    QgsMessageLog, QGis, QgsVectorFileWriter
from PyQt4.Qt import QThread, pyqtSignal, QMutex, QMutexLocker, QDir


class SnapToGrid(QThread):

    run_finished = pyqtSignal(str, bool)
    run_progressed = pyqtSignal(str, int, int)
    report_message = pyqtSignal(str, str)

    def __init__(self, plugin, grid_size, create_backup, backup_path, parent=None):

        super(SnapToGrid, self).__init__(parent)
        self.plugin = plugin
        self.stopped = False
        self.mutex = QMutex()
        self.completed = False
        self.layer_id = None
        self.snap_extent = None
        self.grid_size = grid_size
        self.create_backup = create_backup
        self.backup_path = backup_path

    def initialize(self, layer_id, snap_extent):

        self.layer_id = layer_id
        self.snap_extent = snap_extent

        self.stopped = False
        self.completed = False

    def run(self):

        self.__snap()
        self.stop()
        self.run_finished.emit(self.layer_id, self.completed)

    def stop(self):

        with QMutexLocker(self.mutex):
            self.stopped = True

    def __snap(self):

        self.report_message.emit(self.layer_id, 'preparing ...')
        orig_layer = QgsMapLayerRegistry.instance().mapLayer(self.layer_id)
        # create a copy of the layer just for editing
        layer = QgsVectorLayer(orig_layer.source(), orig_layer.name(), orig_layer.providerType())
        geom_type = layer.geometryType()
        # layer.wkbType() does not return reliable results
        wkb_type = layer.wkbType()

        if self.create_backup:
            self.report_message.emit(self.layer_id, 'creating backup ...')
            self.__create_backup_file(orig_layer)

        self.report_message.emit(self.layer_id, 'preparing ...')
        layer.startEditing()
        request = QgsFeatureRequest().setFilterRect(self.snap_extent)
        total_features = 0
        for feature in layer.getFeatures(request):
            total_features += 1

        QgsMessageLog.logMessage(self.plugin.tr('Features to be snapped in layer <{0}>: {1}').
                                 format(orig_layer.name(), total_features), self.plugin.tr('Vertex Tools'),
                                 QgsMessageLog.INFO)
        if total_features == 0:
            self.report_message.emit(self.layer_id, 'no features')

        count = 0
        for feature in layer.getFeatures(request):
            with QMutexLocker(self.mutex):
                if self.stopped:
                    layer.rollBack()
                    return

            if geom_type == QGis.Point:
                snapped_geom = self.__point_grid(feature, wkb_type)
            elif geom_type == QGis.Line:
                snapped_geom = self.__line_grid(feature, wkb_type)
            elif geom_type == QGis.Polygon:
                snapped_geom = self.__polygon_grid(feature, wkb_type)

            layer.changeGeometry(feature.id(), snapped_geom)

            count += 1
            self.run_progressed.emit(self.layer_id, count, total_features)

        layer.commitChanges()

        self.completed = True

    def __point_grid(self, feature, wkb_type):

        if feature.geometry().isMultipart():
            points = feature.geometry().asMultiPoint()
        else:
            points = list()
            points.append(feature.geometry().asPoint())

        snapped_points = self.__points_to_grid(points)

        if feature.geometry().isMultipart():
            geom = QgsGeometry.fromMultiPoint(snapped_points)
        else:
            geom = QgsGeometry.fromPoint(snapped_points[0])

        return geom

    def __line_grid(self, feature, wkb_type):

        if feature.geometry().isMultipart():
            polylines = feature.geometry().asMultiPolyline()
            cleaned_polylines = list()
            for polyline in polylines:
                snapped_points = self.__points_to_grid(polyline)
                if len(snapped_points) < 2:
                    continue
                cleaned_polyline = snapped_points
                cleaned_polylines.append(cleaned_polyline)
            geom = QgsGeometry.fromMultiPolyline([x for x in cleaned_polylines])
        else:
            points = feature.geometry().asPolyline()
            snapped_points = self.__points_to_grid(points)
            geom = QgsGeometry.fromPolyline(snapped_points)

        return geom

    def __polygon_grid(self, feature, wkb_type):

        if feature.geometry().isMultipart():
            polygons = feature.geometry().asMultiPolygon()
            cleaned_polygons = list()
            for polygon in polygons:
                cleaned_polylines = list()
                for polyline in polygon:
                    snapped_points = self.__points_to_grid(polyline)
                    cleaned_polyline = snapped_points
                    cleaned_polylines.append(cleaned_polyline)
                cleaned_polygons.append(cleaned_polylines)
            geom = QgsGeometry.fromMultiPolygon([x for x in cleaned_polygons])
        else:
            polygon = feature.geometry().asPolygon()
            cleaned_polylines = list()
            for polyline in polygon:
                snapped_points = self.__points_to_grid(polyline)
                cleaned_polyline = snapped_points
                cleaned_polylines.append(cleaned_polyline)
            geom = QgsGeometry.fromPolyline(x for x in cleaned_polylines)

        return geom

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

    def __create_backup_file(self, orig_layer):

        file_name = self.backup_path + QDir.separator() + self.layer_id
        error = QgsVectorFileWriter.writeAsVectorFormat(orig_layer, file_name, "utf-8", None, "ESRI Shapefile",
                                                        False, None, list(), list(), True)
        if error == QgsVectorFileWriter.NoError:
            QgsMessageLog.logMessage(self.plugin.tr('Backup created.'), self.plugin.tr('Vertex Tools'),
                                    QgsMessageLog.INFO)
