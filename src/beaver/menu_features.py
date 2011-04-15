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

def make_item(name, parent, handler = None, *params):
    item = gtk.MenuItem(name)
    if(handler is not None):
        item.connect("activate", handler, *params)
    parent.append(item)
    item.show()
    return item    

def add_submenu(parent, name, submenu):
    if len(submenu) > 0:                
        submenu_item = gtk.MenuItem(name)
        submenu_item.set_submenu(submenu)
        parent.append(submenu_item)
        submenu_item.show()      
               
def make_layers(layers, parent, handler, *params):
    for ul in layers:                           
        make_item(ul.__name__, parent, handler, *(list(params) + [ul]))

def make_separator(parent):
    sep = gtk.SeparatorMenuItem()
    parent.append(sep)
    sep.show()
    return sep
