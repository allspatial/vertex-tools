# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VertexToolsPlugin
                                 A QGIS plugin
 A set of tools to modify vertices
                              -------------------
        begin                : 2015-07-14
        git sha              : $Format:%H$
        copyright            : (C) 2015 by GCI - Dr. Schindler Geo Consult International
        email                : gci@gc-i.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os.path
from PyQt4.QtCore import Qt, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from view.resources_rc import *
from controller.SelectFeatureMapTool import *
from controller.SnapToGridWidget import *


class VertexToolsPlugin:

    def __init__(self, iface):

        self.iface = iface
        self.map_canvas = self.iface.mapCanvas()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(self.plugin_dir, 'i18n', 'vertex_tools_{}.qm'.format(locale))
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.toolbar = None
        self.show_snap_widget = None
        self.edit_vertices = None
        self.map_tool = None
        self.snap_to_grid_widget = None
        self.actions = []

    def tr(self, message):

        return QCoreApplication.translate('VertexToolsPlugin', message)

    def getIcon(self, iconName):

        return QIcon(":vertex_tools/" + iconName)

    def initGui(self):

        self.toolbar = self.iface.addToolBar(self.tr('Vertex Tools'))
        self.toolbar.setObjectName('Vertex Tools')

        self.edit_vertices = QAction(self.getIcon("vertex.png"), self.tr("View / Edit Vertices"), self.iface.mainWindow())
        self.edit_vertices.setCheckable(True)
        self.map_tool = SelectFeatureMapTool(self)
        self.map_tool.setAction(self.edit_vertices)
        self.show_snap_widget = QAction(self.getIcon("grid.png"), self.tr("Show/Hide Widget"), self.iface.mainWindow())
        self.show_snap_widget.setCheckable(True)

        self.iface.addPluginToVectorMenu(self.tr('Vertex Tools'), self.show_snap_widget)
        self.iface.addPluginToVectorMenu(self.tr('Vertex Tools'), self.edit_vertices)
        self.toolbar.addActions([self.show_snap_widget, self.edit_vertices])
        self.actions.append(self.show_snap_widget)
        self.actions.append(self.edit_vertices)

        self.snap_to_grid_widget = SnapToGridWidget(self)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.snap_to_grid_widget)
        self.snap_to_grid_widget.visibilityChanged.connect(self.__snap_widget_visibilityChanged)
        self.snap_to_grid_widget.show()

        self.show_snap_widget.triggered.connect(self.__show_snap_widget)

    def unload(self):

        for action in self.actions:
            self.iface.removePluginVectorMenu(self.tr('Vertex Tools'), action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

        # remove widget
        self.iface.removeDockWidget(self.snap_to_grid_widget)
        del self.snap_to_grid_widget

    def __show_snap_widget(self):

        if self.snap_to_grid_widget.isVisible():
            self.snap_to_grid_widget.hide()
        else:
            self.snap_to_grid_widget.show()

    def __snap_widget_visibilityChanged(self):

        if self.snap_to_grid_widget.isVisible():
            self.show_snap_widget.setChecked(True)
        else:
            self.show_snap_widget.setChecked(False)
