# coding=UTF-8
__author__="Alex Korovyansky"
__date__ ="$15.04.2010 12:15:36$"

from beaver.signals import SignalMaker

class PacketsModel(SignalMaker):

    signal_set = "set"
    signal_change = "change"
    signal_add = "add"
    signal_remove = "remove"    
    def __init__(self, packets = None):
        SignalMaker.__init__(self)
        self.handlers = {
            PacketsModel.signal_set:[], PacketsModel.signal_change:[], 
            PacketsModel.signal_remove:[], PacketsModel.signal_add: []
            }    
        self.packets = packets

    def set_packets(self, packets):
        self.packets = packets
        self.notify(PacketsModel.signal_set)
    
    def change(self, pos, packet):
        self.packets[pos] = packet
        self.notify(PacketsModel.signal_change, pos)
                 
    def remove(self, positions):
        positions.sort()
        positions.reverse()
        for p in positions:
            self.packets.pop(p)
        self.notify(PacketsModel.signal_remove, positions)

    def add(self, pos, packet):
        self.packets.insert(pos, packet)
        self.notify(PacketsModel.signal_add, pos)
