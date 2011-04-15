#!/usr/bin/env python
# coding=UTF-8

## This file is part of Beaver
## See https://github.com/korovyansk/Beaver for more informations
## Copyright (C) Alex Korovyansky <korovyansk@gmail.com>
## This program is published under a GPLv2 license

__author__="Alex Korovyansky"
__date__ ="$15.04.2010 12:15:36$"

from beaver.config import LOGGER as logger

__all__ = ["SignalMaker"]

class SignalMaker(object):
    
    def __init__(self):
        self.handlers = {}
                
    def add_handler(self, signal, handler, *params):
        self.handlers[signal].append((handler, params))
        logger.debug("packet model add new handler %s, user params: %s for signal: %s" %(handler, params, signal))
    
    def remove_handler(self, signal, handler):
        #удаление не зарегистрированного обработчика это не ошибка!
        try:
            handlers = self.handlers[signal]
            new_handlers = []
            for h in handlers:
                if(h[0] <> handler):
                    new_handlers.append(h)
            self.handlers[signal] = new_handlers
            logger.debug("remove handler %s with all user params" %handler)
        except Exception, e:
            pass

    def remove_handler_concrete(self, signal, handler, *params):
        #удаление не зарегистрированного обработчика это не ошибка!
        try:
            handlers = self.handlers[signal]
            handlers.remove((handler, params))
            logger.debug("remove handler %s with concrete user params: %s" %(handler, params))
        except Exception, e:
            pass

    def notify(self, signal, event = None):        
        for h in self.handlers[signal]:
            try:
                h[0](event, *h[1])
            except Exception, e:
                import traceback
                traceback.print_exc()
                logger.warning("%s sent %s signal to bad handler %s: %s" %(self.__class__.__name__, signal, h[0], e))
                
def main():
    def foo(event, a = None):
        print a
    
    pm = SignalMaker()
    pm.add_handler("update", foo)
    pm.add_handler("update", foo, "A")
    pm.add_handler("update", foo, "B")
    pm.remove_handler("update", foo)
    pm.remove_handler_concrete("update", foo, "A")
    pm.notify("update",None)            
                
