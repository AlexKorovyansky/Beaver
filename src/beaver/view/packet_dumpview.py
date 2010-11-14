#encoding=UTF-8

from beaver.model.packet import PacketModel

import pygtk
pygtk.require('2.0')
import gtk
import pango

from scapy.config import conf
from scapy.layers.all import *
from scapy.packet import *
from scapy.fields import *
from scapy.base_classes import SetGen

from beaver.func import subclasses
from beaver.config import LOGGER as logger

class PacketDumpView(gtk.TextView):
    default_color_field = None
        
    def __init__(self, pm = None):        
        gtk.TextView.__init__(self)
        #fontdesc = pango.FontDescription("Luxi Mono")       
        fontdesc = pango.FontDescription("Lucida Console")
	self.modify_font(fontdesc)       
        self.set_editable(False)  
        self.packet_model = pm
        if(self.packet_model is not None):
            self.packet_model.add_handler(PacketModel.signal_update, self.packet_updated)
    
    def set_packet_model(self, pm):
        #при назначении новой модели вид отписывает от сообщений текущей модели    
        if(self.packet_model is not None):
            self.packet_model.remove_handler(PacketModel.update, self.packet_updated)
        self.packet_model = pm      
        self.packet_model.add_handler(PacketModel.signal_update, self.packet_updated)   

    def sane_color(self, x):
        r=""
        for i in x:
            j = ord(i)
            if (j < 32) or (j >= 127):
                r=r+"."
            else:
                r=r+i
        return r

    def hexdump(self, x):
        result = ""
        x=str(x)
        l = len(x)
        i = 0
        while i < l:
            result += "%04x   " % i
            for j in range(16):
                if i+j < l:
                    result += "%02X " % ord(x[i+j])
                else:
                    result += "   "
                if j%16 == 7:
                    result += " "
            result += "  "
            result += self.sane_color(x[i:i+16]) + "\r\n"
            i += 16
        return result

    def packet_updated(self, *args):
        s = self.hexdump(self.packet_model.packet)
        tbuffer = gtk.TextBuffer()
        tbuffer.set_text(s)
        self.set_buffer(tbuffer)
