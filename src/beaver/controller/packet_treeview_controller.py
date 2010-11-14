# coding=UTF-8
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

from beaver.func import subclasses
from beaver.config import LOGGER as logger
from beaver.menu_features import *    

class PacketTreeViewController(object):

    def __init__(self, model, view):
        self.view = view  
        self.model = model
        self.all_layers = sorted(conf.layers, key=lambda x:x.__name__)
        #FIX ME: если какой то модуль не подгружен след строка вызовет ошибку
        self.common_layers = [Ether, ARP, IP, IPv6, ICMP, TCP, UDP, DNS, Raw]         
        self.view.set_headers_clickable(True)
        self.view.cell.connect('edited', self.edited_cb)
        self.view.connect('button_press_event', self.button_press)
        self.view.set_search_column(0)
             
    def get_treestore_object(self, path):
        treestore = self.view.get_model()
        return treestore[path][0]     
               
    def popup_list_add(self, popup, list, field):
        list.append(field())
        self.model.update()
    
    def popup_list_remove(self, popup, list, field):
        list.remove(field)
        self.model.update()

    def popup_field_set_value(self, popup, packet, field, value):
        packet.__setattr__(field.name, value)      
        self.model.update()

    def popup_set_packet(self, popup, packet, packet_class):      
        new_packet = packet_class()
        new_packet.add_payload(packet.payload)
        if(packet == self.model.packet):
            #корневой заголовок
            self.model.set_packet(new_packet)
        else:
            u = packet.underlayer
            if(u is None):
                logger.warning("None underlayer for no root layer!")
            else:
                u.remove_payload()
                u.add_payload(new_packet)
                self.model.update()
    
    def popup_remove_packet(self, popup, packet):
        if(packet == self.model.packet):
            #корневой заголовок
            if(not packet.payload):
                self.model.set_packet(None)
            else:
                self.model.set_packet(packet.payload)
        else:
            u = packet.underlayer
            if(u is None):
                logger.warning("None underlayer for no root layer!")
            else:
                u.remove_payload()
                u.add_payload(packet.payload)
                self.model.update()
    
    def popup_set_packet_underlayer(self, popup, packet, underlayer):
        u = underlayer()
        u.add_payload(packet)
        self.model.set_packet(u)        
    
    def popup_set_packet_payload(self, popup, packet, payload):
        packet.remove_payload()
        packet.add_payload(payload())
        self.model.update()
    
    def popup_remove_packet_underlayer(self, popup, packet):
        packet.remove_underlayer(None)
        self.model.set_packet(packet)
                
    def popup_remove_packet_payload(self, popup, packet):
        packet.remove_payload()
        self.model.update()
    
    def popup_packet_default(self, popup, packet, _all = False):
        def reset_packet(packet, _all):
            if(packet is None or not packet):
                return            
            packet.fields = {}
            #перегрузка полей верхнего уровня
            payload = packet.payload
            for t in packet.aliastypes:
                if payload.overload_fields.has_key(t):
                    packet.overloaded_fields = payload.overload_fields[t]
                    break
            if _all:
                reset_packet(payload, _all)
        reset_packet(packet, _all) 
        #dict = packet.default_fields
        #for name in dict.keys():
            #packet.__setattr__(name, dict[name])
        self.model.update()

    
    def make_popup(self, pth):
        def make_popup_packet(packet, top):        
            popup = gtk.Menu()   
            if(top is None):                      
                popup = gtk.Menu()
                #----under_layer
                u_items = gtk.Menu()
                #remove
                if(packet.underlayer is not None):
                    make_item("remove", u_items, self.popup_remove_packet_underlayer, packet)
                    make_separator(u_items)                                            
                #наиболее часто используемые слои
                make_layers(self.common_layers, u_items, self.popup_set_packet_underlayer, packet)
                #все     
                u_all_items = gtk.Menu()
                make_layers(self.all_layers, u_all_items, self.popup_set_packet_underlayer, packet)                                                                         
                add_submenu(u_items, "all", u_all_items)
                add_submenu(popup, "under layer", u_items)       
                #----this_layer
                u_items = gtk.Menu()         
                #наиболее часто используемые слои
                make_layers(self.common_layers, u_items, self.popup_set_packet, packet)
                #все     
                u_all_items = gtk.Menu()
                make_layers(self.all_layers, u_all_items, self.popup_set_packet, packet)                                                                         
                add_submenu(u_items, "all", u_all_items)
                add_submenu(popup, "this layer", u_items)                             
                #----upper_layer(payload)
                u_items = gtk.Menu()
                #remove
                if(packet.payload is not None and packet.payload):
                    make_item("remove", u_items, self.popup_remove_packet_payload, packet)
                    make_separator(u_items)                                            
                #наиболее часто используемые слои
                make_layers(self.common_layers, u_items, self.popup_set_packet_payload, packet)
                #все     
                u_all_items = gtk.Menu()
                make_layers(self.all_layers, u_all_items, self.popup_set_packet_payload, packet)                                                                         
                add_submenu(u_items, "all", u_all_items)
                add_submenu(popup, "upper layer", u_items)                  
                #----default
                make_item("default", popup, self.popup_packet_default, packet)
            return popup
                        
        def make_popup_list(list, top):
            popup = gtk.Menu()  
            #текущее содержимое(обычый python list)
            value = top.getfieldval(list.name)
            
            #добавление
            add_item = gtk.MenuItem("add")
            add_items = gtk.Menu()
            #возможные варианты
            #DEV: всегда ли у list есть поле cls
            #у PacketListField точно есть
            for sub in subclasses(list.cls):
                sub_item = gtk.MenuItem(sub.__name__)                
                sub_item.connect("activate", self.popup_list_add, value, sub)
                add_items.append(sub_item)
                sub_item.show()     
            if(len(add_items) > 0):
                add_item = gtk.MenuItem("add")
                add_item.set_submenu(add_items)
                popup.append(add_item)
                add_item.show()                                      
            #удаление
            remove_items = gtk.Menu()
            for elem in value:
                sub_item = gtk.MenuItem(elem.name)                
                sub_item.connect("activate", self.popup_list_remove, value, elem)
                remove_items.append(sub_item)
                sub_item.show()
            if(len(remove_items) > 0):
                remove_item = gtk.MenuItem("remove")
                remove_item.set_submenu(remove_items)
                popup.append(remove_item)
                remove_item.show()
            return popup
                
        def make_popup_field(field, top):
            popup = gtk.Menu() 
            if isinstance(field, EnumField):
                if isinstance(field, MultiEnumField):
                    v = field.depends_on(top)
                    if v in field.s2i_multi:
                        s2i = field.s2i_multi[v]
                    else:
                        s2i = {}
                else:
                    s2i = field.s2i
                keys = s2i.keys()
                keys.sort()                    
                #возможные варианты
                var_items = gtk.Menu()
                for var in keys:
                    sub_item = gtk.MenuItem(var)                
                    sub_item.connect("activate", self.popup_field_set_value, top, field, s2i[var])
                    var_items.append(sub_item)
                    sub_item.show()                
                if(len(var_items) > 0):
                    popup = var_items                    
            return popup
    
        def make_popup_empty():
            popup = gtk.Menu()
            #----тип пакета
            p_items = gtk.Menu()
            #наиболее часто используемые слои
            make_layers(self.common_layers, p_items, self.popup_set_packet)
            #все     
            p_all_items = gtk.Menu()
            make_layers(self.all_layers, p_all_items, self.popup_set_packet)                                                                         
            add_submenu(p_items, "all", p_all_items)
            add_submenu(popup, "packet", p_items)                  
            #----default all
            make_item("default all", popup, self.popup_packet_default, self.model.packet, True)            
            return popup
                          
        if pth is not None:            
            #щелчок по ячейке
            path = pth[0]        
            scapy_object = self.get_treestore_object(path)
            elem, top = scapy_object
            if(isinstance(elem, Packet)):
                #пакет
                logger.debug("make popup for packet")
                popup = make_popup_packet(elem, top)
            elif(elem.islist and elem.holds_packets and type(top.getfieldval(elem.name)) is list):
                #список
                logger.debug("make popup for list")
                popup = make_popup_list(elem, top)
            else:
                #поле
                logger.debug("make popup for field")
                popup = make_popup_field(elem, top)                     
        else:
            #пустое место
            popup = None
        return popup    
                    
    def button_press(self, treeview, event):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)
            if(pthinfo):
                treeview.set_cursor(pthinfo[0], pthinfo[1], 0)
                popup = self.make_popup(pthinfo)
                if len(popup) > 0:
                    popup.popup(None, None, None, event.button, time)
            return True


    # редактирование ячейки таблицы       
    def edited_cb(self, cell, path, new_text):       
        scapy_object = self.get_treestore_object(path)
        elem, top = scapy_object
        if(isinstance(elem,Packet)):
            #заголовок пакета
            return    
        try:
            top.__setattr__(elem.name, eval(new_text))
        except Exception, e:
            logger.debug("bad value: %s"%new_text)
        else:
            self.model.update()                          
