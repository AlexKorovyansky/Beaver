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
conf.logLevel = 40 #ERROR
conf.verbose = False

from scapy.all import *

from beaver.plugins import EditorPlugin

from beaver.model.packet import PacketModel
from beaver.view.packet_treeview import PacketTreeView
from beaver.view.packet_dumpview import PacketDumpView
from beaver.controller.packet_treeview_controller import PacketTreeViewController

from beaver.model.packets import PacketsModel
from beaver.view.packets_listview import PacketsListView
from beaver.controller.packets_listview_controller import PacketsListViewController

import beaver.config as config
from beaver.config import LOGGER as logger

import os.path

class PacketEditor(object):
    
    def neighbor_file_path(self, filename):
        p, f = os.path.split(__file__)
        return os.path.join(p, filename)
                                
    def new(self, *args):
        self.filename = None
        self.packetsmodel.set_packets(PacketList())
        self.statusbar.push(0, "Create empty set of packets")     
        
    def open_from_file(self, filename = None):
        if(filename is not None):
            self.filename = filename
        packets = PacketList()
        try:
            self.statusbar.push(0, "Openning file %s ..." %self.filename)                    
            packets = rdpcap(self.filename)
        except Exception, e:                
            self.statusbar.push(0, "Cannot open file %s..."%self.filename)
        else:
            self.statusbar.push(0, "Open %s" %self.filename)
        self.packetsmodel.set_packets(packets)
            
    def open(self, *args):        
        response = self.open_dialog.run()
        self.open_dialog.hide()
        if(response == gtk.RESPONSE_OK):
            self.filename = self.open_dialog.get_filename()
            self.open_from_file()

    def save_to_file(self, filename = None):
        if(filename is not None):
            self.filename = filename        
        try:
            self.statusbar.push(0, "Saving file %s ..." %self.filename)                    
            packets = self.packetsmodel.packets
            logger.debug("try save packets to file %s" %self.filename)
            wrpcap(self.filename, packets)          
        except Exception, e:                
            logger.debug("error while saving: %s" %e)
            self.statusbar.push(0, "Error while saving, see console log for details %s..."%self.filename)
        else:
            logger.debug("packets were saved succesfull")
            self.statusbar.push(0, "Saved in %s" %self.filename)                    
    
    def save(self, *args):
        if(self.filename is None):
            response = self.save_dialog.run()
            self.save_dialog.hide()
            if(response == gtk.RESPONSE_OK):
                self.filename = self.save_dialog.get_filename()
                self.save_to_file()
        else:
            self.save_to_file()
        
    def save_as(self, *args):
        response = self.save_dialog.run()
        self.save_dialog.hide()
        if(response == gtk.RESPONSE_OK):
            self.filename = self.save_dialog.get_filename()
            name, ext = os.path.splitext(self.filename)
            if(not ext):
                self.filename += ".pcap"
            self.save_to_file()    
            
    def check_plugin(self, check_item, plugin):
        plugin.set_active(check_item.active)
    
    def check_iface(self, iface_item, iface):
        self.iface = iface
        if iface_item.get_active():
            for i in self.iface_checkitem_list:
                if i <> iface_item:
                    i.set_active(False)
                     
    def undo(self, *args):
        pass
    
    def redo(self, *args):
        pass
    
    def exit(self, *args):
        gtk.main_quit()
        return False
    
    def send(self, *args):
        try:
            logger.debug("try send packets")
            packets = self.packetsmodel.packets
            sendp(packets,iface=self.iface)
        except Exception, e:
            logger.warning("error while sending packets: %s" %e)
            self.statusbar.push(0, "Error while sending packets, see console log for details")
        else:
            logger.debug("packets were sent succesfull")
            self.statusbar.push(0, "Packets were sent successful")
            
    def about(self, *args):
        response = self.about_dialog.run()
        self.about_dialog.hide()
    
    def __init__(self):
        self.dict = {"exit":self.exit, "new":self.new, "open": self.open, 
                    "save":self.save, "save_as":self.save_as,"send": self.send,
                    "undo":self.undo, "redo":self.redo, "about":self.about}
        self.builder = gtk.Builder()      
        
        #загрузка интерфейса
        self.builder.add_from_file(self.neighbor_file_path("editor.glade"))
        self.builder.connect_signals(self.dict)        
                         
        self.init_members()
        self.init_menu()
        self.init_dialogs()
        self.init_MVC()
        self.init_events()
        self.init_components()        
        self.init_plugins()
        self.after_init()
        
    def init_members(self):
        self.filename = None
        self.iface = None
        self.iface_checkitem_list = []        
        self.plugins = []
        self.window = self.builder.get_object("main_window")
        self.about_dialog = self.builder.get_object("aboutdialog1")        
        self.packets_view = self.builder.get_object("packets_view")
        self.packet_view = self.builder.get_object("packet_view")        
        self.save_action = self.builder.get_object("action_save")
        self.save_as_action = self.builder.get_object("imagemenuitem4")
        self.undo_action = self.builder.get_object("action_undo")
        self.redo_action = self.builder.get_object("action_redo")
        self.send_action = self.builder.get_object("action_send")
        self.view_toolbar_action = self.builder.get_object("checkmenuitem1")
        self.view_statusbar_action = self.builder.get_object("checkmenuitem2")
        self.about_action = self.builder.get_object("imagemenuitem10")
        self.statusbar = self.builder.get_object("statusbar1")
        self.plugins_menuitem = self.builder.get_object("menuitem_plugins")   
        self.ifaces_menuitem = self.builder.get_object("menuitem_ifaces") 
        self.service_menu = self.builder.get_object("menu_service") 

    def init_components(self):
        self.undo_action.set_sensitive(False)
        self.redo_action.set_sensitive(False)
        self.send_action.set_sensitive(False)
        self.save_action.set_sensitive(False)
        self.save_as_action.set_sensitive(False) 
        self.view_toolbar_action.set_sensitive(False)
        self.view_statusbar_action.set_sensitive(False) 
        self.statusbar.push(0, "Welcome to Beaver, Visual TCP/IP Packet Editor!")
        self.window.maximize()
        self.window.show_all()
    
    def init_menu(self):
        ifaces = get_if_list()
        ifaces_menu = gtk.Menu()        
        for i in ifaces:            
            iface_checkitem = gtk.CheckMenuItem(i)
            self.iface_checkitem_list.append(iface_checkitem)
            iface_checkitem.set_draw_as_radio(True)
            iface_checkitem.connect("activate", self.check_iface, i)
            iface_checkitem.show()
            ifaces_menu.append(iface_checkitem)            
        if len(ifaces_menu) > 0:
            self.ifaces_menuitem.set_submenu(ifaces_menu)

    def init_dialogs(self):
        #открыть
        self.open_dialog = gtk.FileChooserDialog("Open..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        self.open_dialog.set_default_response(gtk.RESPONSE_OK)              
        filter = gtk.FileFilter()
        filter.set_name("PCAP files")
        filter.add_pattern("*.pcap")
        self.open_dialog.add_filter(filter)   
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        self.open_dialog.add_filter(filter)
        #сохранить
        self.save_dialog = gtk.FileChooserDialog("Save as..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_SAVE,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        self.save_dialog.set_default_response(gtk.RESPONSE_OK)                
        filter = gtk.FileFilter()
        filter.set_name("PCAP files")
        filter.add_pattern("*.pcap")
        self.save_dialog.add_filter(filter)   
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        self.save_dialog.add_filter(filter)

    def init_MVC(self):
        #модель набора пакетов
        self.packetsmodel = PacketsModel(PacketList())
        #вид набора пакетов
        self.packetsview = PacketsListView(self.packetsmodel)        
        PacketsListViewController(self.packetsmodel, self.packetsview)
        
        self.scroll_packetsview = gtk.ScrolledWindow()
        self.scroll_packetsview.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)   
        self.scroll_packetsview.add_with_viewport(self.packetsview)          
        self.packets_view.add(self.scroll_packetsview)
        
        #модель пакета
        self.packetmodel = PacketModel()
        #вид - заголовки и поля
        self.packettreeview = PacketTreeView(self.packetmodel)
        PacketTreeViewController(self.packetmodel, self.packettreeview)        
        #вид - дамп пакета
        self.packetdumpview = PacketDumpView(self.packetmodel)
        
        #компановка видов пакета
        scroll_packetview = gtk.ScrolledWindow()
        scroll_packetview.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)   
        scroll_packetview.add_with_viewport(self.packettreeview)           
        self.packet_view.pack1(scroll_packetview, resize = True, shrink = False)

        scroll_packetview = gtk.ScrolledWindow()
        scroll_packetview.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)   
        scroll_packetview.add_with_viewport(self.packetdumpview)           
        self.packet_view.pack2(scroll_packetview, resize = False, shrink = True)     

    def init_events(self):
        #обработка события MVC
        self.packetmodel.add_handler(PacketModel.signal_update, self.packet_updated)
        self.packetsmodel.add_handler(PacketsModel.signal_set, self.packets_set)
        self.packetsmodel.add_handler(PacketsModel.signal_remove, self.packets_remove)
        self.packetsmodel.add_handler(PacketsModel.signal_add, self.packets_add)
        #события GTK
        self.packetsview.connect("row-activated", self.packet_activated)
    
    def init_plugins(self):
        #инициализирование плагинов
        folder = config.EDITOR_PLUGINS_FOLDER        
        logger.debug("start scanning plugins...")
        import sys
        import os.path
        full_folder = os.path.abspath(folder)
        try:
            sys.path.index(full_folder)
        except:
            sys.path.append(full_folder)
        import glob
        files = glob.glob(os.path.join(folder, "*.py"))
        if(not files):
            logger.debug("directory " + folder + " doesn't contain plugin-files")
        else:            
            plugins_menu = gtk.Menu()
            for f in files:
                logger.debug("discover file: " + f)
                try:
                    plugin = EditorPlugin(f, self)
                except Exception,e:
                    logger.warning("file %s is corrupted: %s" %(f,e))
                else:
                    plugin_checkitem = gtk.CheckMenuItem(plugin.name)
                    plugin_checkitem.connect("activate", self.check_plugin, plugin)
                    plugin_checkitem.show()
                    logger.debug("plugin %s was successful install"%plugin.name)
                    plugins_menu.append(plugin_checkitem)
                    self.plugins.append(plugin)
            if len(plugins_menu) > 0:
                self.plugins_menuitem.set_submenu(plugins_menu)
        logger.debug("end scanning plugins") 

    
    def after_init(self):
        self.packettreeview.set_sensitive(False)
        self.packetdumpview.set_sensitive(False)
        #self.open_from_file("100.pcap")
        
    def set_active(self, pos):
        self.active_pos = pos
        packet = None
        packets = self.packetsmodel.packets
        if(packets is not None):            
            try:
                packet = packets[pos]
            except IndexError:
                logger.debug("cannot active packet at position %s" %pos)
            else:
                self.packetmodel.set_packet(packet)
        self.packettreeview.set_sensitive(packet is not None)
        self.packetdumpview.set_sensitive(packet is not None)        

    def check_controls(self):
        packets = self.packetsmodel.packets
        ne_flag = packets is not None and len(packets) > 0                 
        logger.debug("save, save as, send buttons must be enable: %s" %ne_flag)  
        #сохранить, сохранить как
        self.save_action.set_sensitive(ne_flag)
        self.save_as_action.set_sensitive(ne_flag)                 
        #кнопка отправки набора    
        self.send_action.set_sensitive(ne_flag)
        
    def packet_activated(self, view, path, column):
        self.set_active(path[0])  
    
    def packet_updated(self, event):
        if(self.active_pos >= 0):
            self.packetsmodel.change(self.active_pos, self.packetmodel.packet)         

    def packets_set(self, event):
        self.check_controls()
        self.set_active(0)

    def packets_remove(self, event):
        positions = event
        if(self.active_pos in positions):
            #текущий отображаемый пакет удаляется из списка
            self.packettreeview.set_sensitive(False)
            self.packetdumpview.set_sensitive(False)
        self.check_controls()
    
    def packets_add(self, event):
        self.check_controls()
              
    def main(self):
        gtk.main()
