# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VertexToolsPlugin
                                 A QGIS plugin
 A set of tools to modify vertices
                             -------------------
        begin                : 2015-07-14
        copyright            : (C) 2015 by GCI - Dr. Schindler Geo Consult International
        email                : gci@gc-i.de
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load VertexToolsPlugin class from file VertexToolsPlugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .vertex_tools import VertexToolsPlugin
    return VertexToolsPlugin(iface)
