#encoding: UTF-8
from scapy.all import *

import pygtk
pygtk.require('2.0')
import gtk
from gtk.gdk import Color

color_rules = [
    (lambda packet: packet[TCP].sport == 80 or packet[TCP].dport == 80, (Color(0,0,0), Color(36107,65535,32590))),
    (lambda packet: packet[TCP].flags & 0x02 or packet[TCP].flags == 1, (Color(0,0,0), Color(41026,41026,41026))),
    (lambda packet: packet.haslayer(TCP), (Color(0,0,0), Color(59345,58980,65534))),
    (lambda packet: packet.haslayer(UDP), (Color(0,0,0), Color(28834,57427,65533))),
    (lambda packet: packet.haslayer(ICMP), (Color(0,0,0), Color(49680,49737,65535))),
    (lambda packet: packet.haslayer(ARP), (Color(0,0,0), Color(55011,59486,65534))),
]

def cell_colors(packet):
    global color_rules
    for rule in color_rules:
        try:
            if rule[0](packet):
                return rule[1]
        except:
            pass
    return None

environment = None
save_cell_colors = None

def init(env):
    global environment
    environment = env  
    global save_cell_colors
    save_cell_colors = environment.packetsview.cell_colors  
    global cell_colors
    environment.packetsview.cell_colors = cell_colors
    environment.packetsview.set_rules_hint(False)
    environment.packetsview.queue_draw()

def destroy():
    global environment
    global save_cell_colors
    environment.packetsview.cell_colors = save_cell_colors    
    environment.packetsview.set_rules_hint(True)
    environment.packetsview.queue_draw()    

