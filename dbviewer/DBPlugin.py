# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QMenu, QToolBar, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from qgis.core import QgsProject, QgsMessageLog
from .dbviewer import dbviewer

class DBPlugin:
    """Main class for the plugin"""

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        # Get plugin path
        self.pluginPath = os.path.dirname(__file__)

    def initGui(self):
        """Creates the menu entries and toolbar icons inside the QGIS GUI when plugin is loaded."""

        # Add main menu if it doesnt exist

        self.mainMenu = QMenu(self.iface.mainWindow())
        self.mainMenu.setObjectName('Database Viewer')
        self.mainMenu.setTitle('&Database Viewer')
        self.menuBar = self.iface.mainWindow().menuBar()
        self.menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.mainMenu)

        # Add toolbar
        self.toolbar = self.iface.addToolBar('3DCity DB Viewer')
        self.toolbar.setObjectName('3DCity DB Viewer')

        # Add action
        self.action = QAction('3DCity DB Viewer', self.iface.mainWindow())
        self.action.setIcon(QIcon(os.path.join(self.pluginPath, 'icons', 'dbicon.png')))
        self.action.setObjectName('3DCity DB Viewer')
        self.mainMenu.addAction(self.action) #self.menuTool.addAction(self.action)
        self.toolbar.addAction(self.action)

        self.action.triggered.connect(self.start)

    def unload(self):
        """Removes the plugin menu and toolbar from QGIS GUI when plugin is deactivated."""

        # Remove toolbar
        self.toolbar.deleteLater()

        # Remove main menu
        self.mainMenu.deleteLater()

    def start(self):
        self.dlg = dbviewer(self.iface)
        self.dlg.exec()
