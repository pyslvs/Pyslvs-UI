# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from .QtModules import *
from .graphics.canvas import DynamicCanvas
from .Ui_custom_table import PointTableWidget, LinkTableWidget
from .info.info import VERSION
tr = QCoreApplication.translate

def init_Widgets(self):
    #Splitter stretch factor.
    self.MainSplitter.setStretchFactor(0, 2)
    self.MainSplitter.setStretchFactor(1, 5)
    self.ToolPanelSplitter.setStretchFactor(0, 4)
    self.ToolPanelSplitter.setStretchFactor(1, 5)
    self.panels_splitter.setSizes([100, 500])
    #Version text
    self.menuBar.setCornerWidget(QLabel("Version {}.{}.{} ({})".format(*VERSION)))
    #Entiteis tables
    self.Entiteis_Point = PointTableWidget(self.Entiteis_Point_Widget)
    self.Entiteis_Point.cellDoubleClicked.connect(self.on_Entiteis_Point_cellDoubleClicked)
    self.Entiteis_Point.itemSelectionChanged.connect(self.pointSelection)
    self.Entiteis_Point.deleteRequest.connect(self.on_action_Delete_Point_triggered)
    self.Entiteis_Point_Layout.addWidget(self.Entiteis_Point)
    self.Entiteis_Link = LinkTableWidget(self.Entiteis_Link_Widget)
    self.Entiteis_Link.cellDoubleClicked.connect(self.on_Entiteis_Link_cellDoubleClicked)
    self.Entiteis_Link.dragIn.connect(self.addLinkGroup)
    self.Entiteis_Link.deleteRequest.connect(self.on_action_Delete_Linkage_triggered)
    self.Entiteis_Link_Layout.addWidget(self.Entiteis_Link)
    #QPainter Window
    self.DynamicCanvasView = DynamicCanvas()
    self.DynamicCanvasView.mouse_getSelection.connect(self.Entiteis_Point.setSelections)
    self.DynamicCanvasView.mouse_noSelection.connect(self.Entiteis_Point.clearSelection)
    cleanAction = QAction("Clean selection", self)
    cleanAction.triggered.connect(self.Entiteis_Point.clearSelection)
    cleanAction.setShortcut(Qt.Key_Escape)
    cleanAction.setShortcutContext(Qt.WindowShortcut)
    self.addAction(cleanAction)
    self.DynamicCanvasView.mouse_getDoubleClickAdd.connect(self.addPointGroup)
    self.DynamicCanvasView.mouse_getDoubleClickEdit.connect(self.on_Entiteis_Point_cellDoubleClicked)
    self.DynamicCanvasView.zoom_change.connect(self.setZoomBar)
    self.canvasSplitter.insertWidget(0, self.DynamicCanvasView)
    #Panel widget will hide when not using.
    self.panelWidget.hide()
    #Console dock will hide when startup.
    self.ConsoleWidget.hide()
    #Connect to GUI button switching.
    self.disconnectConsoleButton.setEnabled(not self.args.debug_mode)
    self.connectConsoleButton.setEnabled(self.args.debug_mode)
    #Properties button on the Point tab widget.
    propertiesButton = QPushButton()
    propertiesButton.setIcon(self.action_Property.icon())
    propertiesButton.setToolTip('Properties')
    propertiesButton.setStatusTip("Properties of this workbook.")
    propertiesButton.clicked.connect(self.on_action_Property_triggered)
    self.PointTab.setCornerWidget(propertiesButton)
    #While value change, update the canvas widget.
    self.ZoomBar.valueChanged.connect(self.DynamicCanvasView.setZoom)
    self.LineWidth.valueChanged.connect(self.DynamicCanvasView.setLinkWidth)
    self.PathWidth.valueChanged.connect(self.DynamicCanvasView.setPathWidth)
    self.Font_size.valueChanged.connect(self.DynamicCanvasView.setFontSize)
    self.rotateAngle.valueChanged.connect(self.DynamicCanvasView.setRotateAngle)
    self.action_Display_Point_Mark.toggled.connect(self.DynamicCanvasView.setPointMark)
    self.action_Display_Dimensions.toggled.connect(self.DynamicCanvasView.setShowDimension)
    #DynamicCanvasView Right-click menu
    self.DynamicCanvasView.setContextMenuPolicy(Qt.CustomContextMenu)
    self.DynamicCanvasView.customContextMenuRequested.connect(self.on_painter_context_menu)
    self.popMenu_painter = QMenu(self)
    self.action_painter_right_click_menu_add = QAction("Add a Point", self)
    self.popMenu_painter.addAction(self.action_painter_right_click_menu_add)
    self.action_painter_right_click_menu_fix_add = QAction("Add a fixed Point", self)
    self.popMenu_painter.addAction(self.action_painter_right_click_menu_fix_add)
    self.action_painter_right_click_menu_path = QAction("Add a Path Point [Path Solving]", self)
    self.popMenu_painter.addAction(self.action_painter_right_click_menu_path)
    self.DynamicCanvasView.mouse_track.connect(self.context_menu_mouse_pos)
    #Entiteis_Point Right-click menu
    self.Entiteis_Point_Widget.customContextMenuRequested.connect(self.on_point_context_menu)
    self.popMenu_point = QMenu(self)
    self.action_point_right_click_menu_add = QAction("&Add", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_add)
    self.action_point_right_click_menu_edit = QAction("&Edit", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_edit)
    self.action_point_right_click_menu_lock = QAction("&Fix / Unfix", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_lock)
    self.action_point_right_click_menu_copy = QAction("&Copy table data", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_copy)
    self.action_point_right_click_menu_copyPoint = QAction("Copy point", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_copyPoint)
    self.popMenu_point.addSeparator()
    self.action_point_right_click_menu_delete = QAction("&Delete", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_delete)
    #Entiteis_Link Right-click menu
    self.Entiteis_Link_Widget.customContextMenuRequested.connect(self.on_link_context_menu)
    self.popMenu_link = QMenu(self)
    self.action_link_right_click_menu_add = QAction("&Add", self)
    self.popMenu_link.addAction(self.action_link_right_click_menu_add)
    self.action_link_right_click_menu_edit = QAction("&Edit", self)
    self.popMenu_link.addAction(self.action_link_right_click_menu_edit)
    self.action_link_right_click_menu_copy = QAction("&Copy table data", self)
    self.popMenu_link.addAction(self.action_link_right_click_menu_copy)
    self.popMenu_link.addSeparator()
    self.action_link_right_click_menu_delete = QAction("&Delete", self)
    self.popMenu_link.addAction(self.action_link_right_click_menu_delete) 

def action_Enabled(self):
    ONE_POINT = self.Entiteis_Point.rowCount()>0
    ONE_LINK = self.Entiteis_Link.rowCount()>1
    types = [self.Entiteis_Point.item(row, 2).text() for row in range(self.Entiteis_Point.rowCount())]
    ONE_POINT_R = 'R' in types
    ONE_POINT_P = 'P' in types
    ONE_POINT_RP = 'RP' in types
    #Edit
    self.action_Edit_Point.setEnabled(ONE_POINT)
    self.action_Edit_Linkage.setEnabled(ONE_LINK)
    #Delete
    self.action_Delete_Point.setEnabled(ONE_POINT)
    self.action_Delete_Linkage.setEnabled(ONE_LINK)
    self.action_point_right_click_menu_delete.setEnabled(ONE_POINT)
    self.action_link_right_click_menu_delete.setEnabled(ONE_LINK)
    #Path
    self.action_Path_Track.setEnabled(ONE_POINT)
    for action in [self.action_Path_coordinate, self.action_Save_path_only, self.action_Path_Clear]:
        action.setEnabled(bool(self.File.pathData))
    #Panel
    self.Measurement.setEnabled(ONE_POINT)
    self.Drive_shaft.setEnabled(ONE_POINT_R)
    self.Drive_rod.setEnabled(ONE_POINT_P and ONE_POINT_RP)
    #Others
    self.action_Output_to_Solvespace.setEnabled(ONE_LINK)
    self.action_DXF_2D_models.setEnabled(ONE_LINK)
    self.action_Batch_moving.setEnabled(ONE_POINT)

def showUndoWindow(self, FileState):
    self.undoView = QUndoView(FileState)
    self.undoView.setEmptyLabel("~ Start Pyslvs")
    self.UndoRedoLayout.addWidget(self.undoView)
    separator = QAction(self)
    separator.setSeparator(True)
    self.menu_Edit.insertAction(self.action_Search_Points, separator)
    self.action_Redo = FileState.createRedoAction(self, 'Redo')
    self.action_Undo = FileState.createUndoAction(self, 'Undo')
    self.action_Redo.setShortcut("Ctrl+Shift+Z")
    self.action_Redo.setStatusTip("Backtracking undo action.")
    self.action_Redo.setIcon(QIcon(QPixmap(":/icons/redo.png")))
    self.action_Undo.setShortcut("Ctrl+Z")
    self.action_Undo.setStatusTip("Recover last action.")
    self.action_Undo.setIcon(QIcon(QPixmap(":/icons/undo.png")))
    self.menu_Edit.insertAction(separator, self.action_Undo)
    self.menu_Edit.insertAction(separator, self.action_Redo)
