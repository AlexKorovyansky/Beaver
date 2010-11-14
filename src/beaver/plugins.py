# coding=UTF-8
__author__="Alex Korovyansky"
__date__ ="$15.04.2010 12:15:36$"

import os.path

class EditorPlugin(object):

    def __init__(self, plugin_path, environment = None):
        #инициализирование плагинов
        plugin_file = os.path.basename(plugin_path)
        plugin_name = os.path.splitext(plugin_file)[0]
        plugin = __import__(plugin_name)
        self.init = plugin.init
        self.env = environment
        self.destroy = plugin.destroy
        self.name = plugin_name
        self.active = False
        
    def is_active(self):
        return self.active
    
    def set_active(self, flag):
        if(self.active != flag):
            if flag:
                self.init(self.env)
            else:
                self.destroy()
            self.active = flag
