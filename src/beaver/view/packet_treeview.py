#encoding=UTF-8

from beaver.model.packet import PacketModel

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

class PacketTreeView(gtk.TreeView):
    color_auto_field = gtk.gdk.Color(170*256, 232*256, 255*256)
    default_color_field = None
        
    def __init__(self, pm = None):
        gtk.TreeView.__init__(self)        
        self.packet_model = pm
        if(self.packet_model is not None):
            self.make_treestore()
            self.packet_model.add_handler(PacketModel.signal_update, self.packet_updated)
        self.set_headers_visible(False)        
        tvcolumn = gtk.TreeViewColumn('Редактируемый пакет', )
        self.append_column(tvcolumn)

        self.cell = gtk.CellRendererText()
        self.cell.set_property('editable', True)
        #self.cell.connect('edited', self.edited_cb)
        
        tvcolumn.pack_start(self.cell, True)
        tvcolumn.set_cell_data_func(self.cell, self.view_str)
    
    def set_packet_model(self, pm):
        #при назначении новой модели вид отписывает от сообщений текущей модели    
        if(self.packet_model is not None):
            self.packet_model.remove_handler(PacketModel.update, self.packet_updated)
        self.packet_model = pm      
        self.make_treestore()
        self.packet_model.add_handler(PacketModel.signal_update, self.packet_updated)          

    def save_expanded_lines(self):
        expanded_lines = []
        model = self.get_model()
        def check_line(model, path, iter, data):
            view, expanded_lines = data
            if(view.row_expanded(path)):
                expanded_lines.append(path)
        if(model is not None):
            model.foreach(check_line, (self, expanded_lines))
        return expanded_lines

    def restore_expanded_lines(self, saved_lines):
        model = self.get_model()
        def restore_line(model, path, iter, data):
            view, saved_lines = data
            if path in saved_lines:
                view.expand_row(path, False) 
        if(model is not None):         
            model.foreach(restore_line, (self, saved_lines))

    def packet_updated(self, event):
        expanded_lines = self.save_expanded_lines()
        self.make_treestore()
        try:
            self.restore_expanded_lines(expanded_lines)
        except Exception, e:
            print e
            logger.debug("cannot restore expanded lines")
        
    def make_treestore(self):
        """make treestore from scapy packet"""
        def r_make_treestore(treestore, packet, top_packet = None, top_treenode = None):
            if(not packet or packet is None):
                return
            packet_treenode = treestore.append(top_treenode, [(packet, top_packet)])
            for f in packet.fields_desc:
                if isinstance(f, ConditionalField) and not f._evalcond(packet):
                    continue
                fvalue = packet.getfieldval(f.name)
                if isinstance(fvalue, Packet) or (f.islist and f.holds_packets and type(fvalue) is list):
                    sub_packet_treenode = treestore.append(packet_treenode, [(f, packet)])
                    fvalue_gen = SetGen(fvalue,_iterpacket=0)
                    for fv in fvalue_gen:
                        #fvalue становится top_packet
                        r_make_treestore(treestore, fv, fvalue, sub_packet_treenode)
                else:
                    treestore.append(packet_treenode, [(f, packet)])    
            r_make_treestore(treestore, packet.payload)   
            
        if(self.packet_model.packet is None):
            self.set_model(None)
        else:
            tree = gtk.TreeStore(object)
            r_make_treestore(tree, self.packet_model.packet)
            self.set_model(tree)   
        
    def __scapy_object_view(self, scapy_object):
        color = self.default_color_field
        text = "?"
        f, pack = scapy_object
        try:      
            if(isinstance(f, Packet)):
                text = f.name
            else:
                fname = f.name
                fvalue = pack.getfieldval(fname)
                if isinstance(fvalue, Packet) or (f.islist and f.holds_packets and type(fvalue) is list):
                    text = fname
                else:
                    #print pack.name, pack.underlayer.name
                    if fvalue is None:
                        #автоматическое поле                        
                        try:        
                            bp = pack.firstlayer()#пакет верхнего уровня    
                            bpack = bp.__class__(str(bp))#заполнение всех полей
                            pack = bpack.getlayer(pack.name)#получение нужного загловка
                            fvalue = pack.getfieldval(fname)#пересчитанное значний
                        except:
                            pass
                        color = self.color_auto_field
                    try:
                        text = "%s = %s" %(fname,f.i2repr(pack,fvalue))
                    except:
                        text = "%s = ?" %fname
        except Exception, e:
            print e
        return text,color      

    def view_str(self, treeviewcolumn, cell_renderer, treestore, iter):
        scapy_object = treestore.get_value(iter, 0)        
        text,color = self.__scapy_object_view(scapy_object)
        self.cell.set_property('cell-background-gdk', color)  
        self.cell.set_property('text', text)
