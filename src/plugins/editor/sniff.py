#encoding: UTF-8
import pygtk
pygtk.require('2.0')
import gtk

from scapy.all import *
import threading

def tsn():
    global environment
    sniff(iface=environment.iface, timeout=10, prn=lambda packet: environment.packetsmodel.add(0, packet))  

def sn(widget):
    tsn()        
    
    
environment = None
sep = gtk.SeparatorMenuItem()
sep.show()
sn_item = gtk.MenuItem("начать захват трафика")
sn_item.connect("activate", sn)
sn_item.show()
t = threading.Thread(target=tsn)

def init(env):
    global environment
    environment = env    
    global sep
    environment.service_menu.append(sep)    
    global sn_item
    environment.service_menu.append(sn_item)    

def destroy():
    global environment
    global sep
    environment.service_menu.remove(sep)    
    global sn_item
    environment.service_menu.remove(sn_item)
