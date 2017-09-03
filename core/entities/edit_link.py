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

from ..QtModules import *
from ..graphics.color import colorName, colorIcons
from .Ui_edit_link import Ui_Dialog as edit_link_Dialog

class edit_link_show(QDialog, edit_link_Dialog):
    def __init__(self, Points, Links, pos=False, parent=None):
        super(edit_link_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.Points = Points
        self.Links = Links
        icon = self.windowIcon()
        self.PointIcon = QIcon(QPixmap(":/icons/bearing.png"))
        for i, e in enumerate(colorName()):
            self.Color.insertItem(i, colorIcons(e), e)
        for i in range(len(self.Points)):
            self.noSelected.addItem(QListWidgetItem(self.PointIcon, 'Point{}'.format(i)))
        if pos is False:
            self.Link.addItem(icon, "New link")
            self.Link.setEnabled(False)
            self.Color.setCurrentIndex(self.Color.findText('Blue'))
        else:
            for vlink in self.Links[1:]:
                self.Link.insertItem(i, icon, vlink.name)
            self.Link.setCurrentIndex(pos-1)
        self.name_edit.textChanged.connect(self.isOk)
        self.isOk()
    
    @pyqtSlot(str)
    def isOk(self, p0=None):
        name = self.name_edit.text()
        names = [vlink.name for i, vlink in enumerate(self.Links) if i!=self.Link.currentIndex()+1]
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(name.isidentifier() and not name in names)
    
    @pyqtSlot(int)
    def on_Link_currentIndexChanged(self, index):
        index += 1
        if len(self.Links)>index:
            vlink = self.Links[index]
            self.name_edit.setText(vlink.name)
            self.Color.setCurrentIndex(self.Color.findText(vlink.colorSTR))
            self.noSelected.clear()
            self.selected.clear()
            for pointIndex in vlink.Points:
                self.selected.addItem(QListWidgetItem(self.PointIcon, 'Point{}'.format(pointIndex)))
            for pointIndex in sorted(set(range(len(self.Points)))-set(vlink.Points)):
                self.noSelected.addItem(QListWidgetItem(self.PointIcon, 'Point{}'.format(pointIndex)))
