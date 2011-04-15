# coding=UTF-8

## This file is part of Beaver
## See https://github.com/korovyansk/Beaver for more informations
## Copyright (C) Alex Korovyansky <korovyansk@gmail.com>
## This program is published under a GPLv2 license

__author__="Alex Korovyansky"
__date__ ="$25.04.2010 12:15:36$"

from beaver.model.packets import PacketsModel

import pygtk
pygtk.require('2.0')
import gtk

from scapy.config import conf
from scapy.layers.all import *
from scapy.packet import *
from scapy.fields import *
from scapy.base_classes import SetGen

from beaver.config import LOGGER as logger
from beaver.menu_features import *

class PacketsListView(gtk.TreeView):
    color_auto_field = gtk.gdk.Color(170*256, 232*256, 255*256)
    default_color_field = None
    
    def __init__(self, pm = None):
        gtk.TreeView.__init__(self)
        self.packets_model = None
        self.set_packets_model(pm)
        self.set_headers_visible(False)
        tvcolumn = gtk.TreeViewColumn('Набор пакетов', )
        self.append_column(tvcolumn)

        self.cell = gtk.CellRendererText()
        
        tvcolumn.pack_start(self.cell, True)
        tvcolumn.set_cell_data_func(self.cell, self.view_str)
        self.set_rules_hint(True)
        
    def make_liststore(self):
        """make treestore from scapy packets list"""
        if(self.packets_model.packets is None):
            self.set_model(None)
        else:
            tree = gtk.TreeStore(object)  
            for p in self.packets_model.packets:
                tree.append(None, [p])        
            self.set_model(tree)

    def set_packets_model(self, pm):
        if(pm is None):
            return

        #при назначении новой модели вид отписывает от сообщений текущей модели
        if(self.packets_model is not None):
            self.packets_model.remove_handler(PacketsModel.signal_changed, self.packets_changed)
            self.packets_model.remove_handler(PacketsModel.signal_set, self.packets_set)
            self.packets_model.remove_handler(PacketsModel.signal_add, self.packets_add)            
            self.packets_model.remove_handler(PacketsModel.signal_remove, self.packets_remove)
        self.packets_model = pm
        self.make_liststore()
        self.packets_model.add_handler(PacketsModel.signal_change, self.packets_changed)  
        self.packets_model.add_handler(PacketsModel.signal_set, self.packets_set)
        self.packets_model.add_handler(PacketsModel.signal_add, self.packets_add)        
        self.packets_model.add_handler(PacketsModel.signal_remove, self.packets_remove)
    
    def packets_changed(self, event):
        pos = event
        liststore = self.get_model()
        liststore[(pos,)][0] = self.packets_model.packets[pos]
        #self.queue_draw()
    
    def packets_set(self, event):
        self.make_liststore()
    
    
    def packets_add(self, event):
        pos = event
        liststore = self.get_model()
        packet = self.packets_model.packets[pos]
        liststore.insert(None,pos,[packet])
    
    def packets_remove(self, event):
        positions = event
        liststore = self.get_model()
        for p in positions:
            iter = liststore.get_iter((p,))
            liststore.remove(iter)
    
        
    def view_str(self, treeviewcolumn, cell_renderer, treestore, iter):
        packet = treestore.get_value(iter, 0)        
        #self.cell.set_property('cell-background-gdk', color)  
        text = self.cell_text(packet)
        if(text is not None):            
            self.cell.set_property('text', text)
        colors = self.cell_colors(packet)
        if(colors is not None):
            self.cell.set_property('foreground-gdk', colors[0])        
            self.cell.set_property('background-gdk', colors[1])
        else:
            self.cell.set_property('foreground-gdk', None)        
            self.cell.set_property('background-gdk', None)                         
    
    def cell_text(self, packet):
        return packet.summary()
    
    def cell_colors(self, packet):
        return None
