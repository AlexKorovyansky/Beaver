#encoding: UTF-8
import pygtk
pygtk.require('2.0')
import gtk

from scapy.all import *

def neighbor_file_path(filename):
    p, f = os.path.split(__file__)
    return os.path.join(p, filename)

def fm(widget):
    global label
    label.set_label("Enter fragmentation rule:")
    global dialog
    response = dialog.run()
    dialog.hide()
    if(response == 1):
        #apply     
        try:
            global entry    
            macros = entry.get_text()
            result = eval(macros, globals())
            if not isinstance(result, int):
                raise Exception, "not integer number"               
        except Exception, e:
            print e
        else:
            global environment               
            pp = fragment(environment.packetmodel.packet, result)
            pp.reverse()
            environment.packetsmodel.remove([environment.active_pos])
            for p in pp:
                environment.packetsmodel.add(environment.active_pos, p)    
    else:
        #close
        pass
    

environment = None
sep = gtk.SeparatorMenuItem()
sep.show()
fm_item = gtk.MenuItem("Fragment selected packet")
fm_item.connect("activate", fm)
fm_item.show()

#импорт интерфейса
builder = gtk.Builder() 
builder.add_from_file(neighbor_file_path("fragma.glade"))    
dialog = builder.get_object("fragma_dialog")
label = builder.get_object("label")
entry = builder.get_object("entry_fragma_macros")

def init(env):
    global environment
    environment = env    
    global sep
    environment.service_menu.append(sep)    
    global fm_item
    environment.service_menu.append(fm_item)      

def destroy():
    global environment
    global sep
    environment.service_menu.remove(sep)    
    global fm_item
    environment.service_menu.remove(fm_item)    

