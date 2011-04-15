# coding=UTF-8

## This file is part of Beaver
## See https://github.com/korovyansk/Beaver for more informations
## Copyright (C) Alex Korovyansky <korovyansk@gmail.com>
## This program is published under a GPLv2 license

__author__="Alex Korovyansky"
__date__ ="$15.04.2010 12:15:36$"

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

class PacketsListViewController(object):

    def __init__(self, model, view):
        self.view = view 
        self.model = model 
        self.all_layers = sorted(conf.layers, key=lambda x:x.__name__)
        #FIX ME: если какой то модуль не подгружен след строка вызовет ошибку
        self.common_layers = [Ether, ARP, IP, IPv6, ICMP, TCP, UDP, DNS, Raw]          
        self.view.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.view.set_search_column(0)                       
        self.view.connect('button_press_event', self.button_press)
        self.view.set_search_column(0)    
  
    def get_selected_paths(self, view):
        def foreach_add_pos_to_list(model, path, iter, list):
            list.append(path)
        list = []
        view.get_selection().selected_foreach(foreach_add_pos_to_list, list)
        return list
    
    def popup_add_packet(self, popup, path, packet_class):
        logger.debug("add packet %s to position: %s" %(packet_class.name, path))
        if(path is None):
            pos = len(self.model.packets)
        else:
            pos = path[0] + 1
        self.model.add(pos, packet_class())        
    
    def popup_remove_packets(self, popup, paths):
        logger.debug("remove packets : %s" %paths)
        pp = [p[0] for p in paths]
        self.model.remove(pp)
    
    def make_popup(self, selected):
        popup = gtk.Menu()
        #добавить
        if len(selected) < 2:
            if len(selected) == 0:
                path = None
            else:
                path = selected[0]
            add_items = gtk.Menu()
            #наиболее часто используемые слои
            make_layers(self.common_layers, add_items, self.popup_add_packet, path)
            #все     
            add_all_items = gtk.Menu()
            make_layers(self.all_layers, add_all_items, self.popup_add_packet, path)                                                                         
            add_submenu(add_items, "all", add_all_items)
            add_submenu(popup, "add", add_items)                          
        #удалить
        if len(selected) > 0:
            make_item("remove", popup, self.popup_remove_packets, selected)
        return popup  
    
    def button_press(self, view, event):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = view.get_path_at_pos(x, y)
            selection =  view.get_selection()
            selected = self.get_selected_paths(view)
            if(pthinfo):
                path = pthinfo[0]
                if(not path in selected):
                    selected = [path]
                    selection.unselect_all()
                    selection.select_path(path)
            else:
                selection.unselect_all()                
                selected = []
            popup = self.make_popup(selected)
            if len(popup) > 0:
                popup.popup(None, None, None, event.button, time)
            return True    

