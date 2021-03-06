#encoding: UTF-8
import pygtk
pygtk.require('2.0')
import gtk

from scapy.all import *

def neighbor_file_path(filename):
    p, f = os.path.split(__file__)
    return os.path.join(p, filename)

def pm(widget):
    global label
    label.set_label("Enter macros for selected packet:")
    global last_pm
    global entry_macros   
    entry_macros.set_text(last_pm)     
    global dialog
    response = dialog.run()
    dialog.hide()
    macros = entry_macros.get_text()
    last_pm = macros    
    if(response == 1):
        #apply     
        try:
            result = eval(macros, globals())
            if not isinstance(result, Packet):
                raise Exception, "not Packet object"               
        except Exception, e:
            print e
        else:
            global environment               
            environment.packetmodel.set_packet(result)
    else:
        #close
        pass
    
def psm(widget):
    global label
    label.set_label("Enter macros for set of packets:")
    global last_psm
    global entry_macros   
    entry_macros.set_text(last_psm)        
    global dialog
    response = dialog.run()
    dialog.hide()
    macros = entry_macros.get_text()
    last_psm = macros     
    if(response == 1):
        #apply             
        try:
            result = eval(macros, globals())
            if not isinstance(result, PacketList):
                raise Exception, "not PacketList object"       
        except Exception, e:
            print e
        else: 
            global environment                  
            environment.packetsmodel.set_packets(result)
    else:
        #close
        pass

environment = None
last_pm = ""
last_psm = ""
sep = gtk.SeparatorMenuItem()
sep.show()
pm_item = gtk.MenuItem("Macros for selected packet")
pm_item.connect("activate", pm)
pm_item.show()
psm_item = gtk.MenuItem("Macros for set of packets")
psm_item.connect("activate", psm)
psm_item.show()

#импорт интерфейса
builder = gtk.Builder() 
builder.add_from_file(neighbor_file_path("macro.glade"))    
dialog = builder.get_object("macros_dialog")
label = builder.get_object("label")
entry_macros = builder.get_object("entry_macros")

def init(env):
    global environment
    environment = env    
    global sep
    environment.service_menu.append(sep)    
    global pm_item
    environment.service_menu.append(pm_item)    
    global psm_item
    environment.service_menu.append(psm_item)    

def destroy():
    global environment
    global sep
    environment.service_menu.remove(sep)    
    global pm_item
    environment.service_menu.remove(pm_item)    
    global psm_item
    environment.service_menu.remove(psm_item)    

