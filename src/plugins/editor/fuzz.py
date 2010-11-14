#encoding: UTF-8
import pygtk
pygtk.require('2.0')
import gtk

from scapy.all import *

def neighbor_file_path(filename):
    p, f = os.path.split(__file__)
    return os.path.join(p, filename)

def fz(widget):
    global environment
    pclass = type(environment.packetmodel.packet)
    environment.packetmodel.packet = pclass(str(fuzz(environment.packetmodel.packet)))
    environment.packetmodel.update()

environment = None
sep = gtk.SeparatorMenuItem()
sep.show()
fz_item = gtk.MenuItem("Случайное заполнение выбранного пакета")
fz_item.connect("activate", fz)
fz_item.show()

def init(env):
    global environment
    environment = env    
    global sep
    environment.service_menu.append(sep)    
    global fz_item
    environment.service_menu.append(fz_item)    

def destroy():
    global environment
    global sep
    environment.service_menu.remove(sep)    
    global fz_item
    environment.service_menu.remove(fz_item)    

