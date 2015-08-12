from qgis.core import QgsFeatureRequest, QgsRectangle, QGis
from qgis.gui import QgsRubberBand, QgsMapTool
from PyQt4.QtCore import QSettings, SIGNAL
from PyQt4.QtGui import QColor


class SelectFeatureMapTool(QgsMapTool):

    def __init__(self, plugin):

        QgsMapTool.__init__(self, plugin.mapCanvas)

        self.plugin = plugin
        self.doubleclick = False
        self.__pluginUnloaded = False

        settings = QSettings()
        qgsLineWidth = 2  # use fixed width
        qgsLineRed = settings.value("/qgis/digitizing/line_color_red", 255, type=int)
        qgsLineGreen = settings.value("/qgis/digitizing/line_color_green", 0, type=int)
        qgsLineBlue = settings.value("/qgis/digitizing/line_color_blue", 0, type=int)

        self.rubBandPol = QgsRubberBand(plugin.mapCanvas, QGis.Line)
        self.rubBandPol.setColor(QColor(qgsLineRed, qgsLineGreen, qgsLineBlue))
        self.rubBandPol.setWidth(qgsLineWidth)

    def activate(self):

        super(SelectFeatureMapTool, self).activate()

        self.plugin.iface.mainWindow().statusBar().showMessage(self.tr("Click on a parcel!"))
        self.currentDialog = None
        self.dialogPosition = None
        self.currentPossessionType = "INDIVIDUAL"
#        self.plugin.mapCanvas.setCursor(QCursor(Qt.ArrowCursor))
        
    def canvasDoubleClickEvent(self, event):
        
        self.doubleclick = True
            
    def canvasReleaseEvent(self, event):

        if self.doubleclick:
            self.doubleclick = False
            return

        if event.button() <> Qt.LeftButton:
            return

        layer = self.plugin.getLayerByTableName('ca_parcel')

        if not layer:
            return
            
        # find out map coordinates from mouse click
        mapPoint = self.toLayerCoordinates(layer, event.pos())
        tolerance = self.plugin.getTolerance(layer)
        area = QgsRectangle(mapPoint.x() - tolerance, mapPoint.y() - tolerance, mapPoint.x() + tolerance, mapPoint.y() + tolerance)

        request = QgsFeatureRequest()
        request.setFilterRect(area).setFlags(QgsFeatureRequest.ExactIntersect)
        request.setSubsetOfAttributes([0])

        result = False

        for feature in layer.getFeatures(request):

            self.rubBandPol.reset(True)
            self.rubBandPol.addGeometry(feature.geometry(), layer)

            parcel_no = int(feature[0])

            possession_type = self.__possessionType(parcel_no)

            if not self.currentDialog or possession_type != self.currentPossessionType:

                if self.currentDialog:
                    self.dialogPosition = self.currentDialog.pos()
                    self.currentDialog.reject()

                # if possession_type == "INDIVIDUAL":
                #     self.currentDialog = PossessionDetailsDialog(self.plugin, self.plugin.iface.mainWindow())
                # else:
                #     self.currentDialog = CooperativePossessionDetailsDialog(self.plugin, self.plugin.iface.mainWindow())

                self.currentPossessionType = possession_type
                self.connect(self.currentDialog, SIGNAL("rejected()"), self.__dialogClosed)

            if self.dialogPosition:
                self.currentDialog.move(self.dialogPosition)

            self.currentDialog.setParcelNo(parcel_no)

            if self.currentDialog.isHidden():
                self.currentDialog.show()

            result = True
            break
                
        if not result:
            self.__resetTool()

    def __resetTool(self):

        if self.currentDialog:
            self.currentDialog.hide()
            self.dialogPosition = self.currentDialog.pos()

        self.rubBandPol.reset(True)

    def deactivate(self):

        if self.__pluginUnloaded:
            return

        self.plugin.iface.mainWindow().statusBar().showMessage("")
        self.doubleclick = False
        self.rubBandPol.reset(True)
        if self.currentDialog:
            self.currentDialog.reject()

        super(SelectFeatureMapTool, self).deactivate()

    def __dialogClosed(self):

        self.currentDialog = None
        #self.dialogPosition = None

    def setPluginUnloaded(self):

        self.__pluginUnloaded = True