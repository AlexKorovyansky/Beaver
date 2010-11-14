# coding=UTF-8
__author__="Alex Korovyansky"
__date__ ="$15.04.2010 12:15:36$"

from beaver.signals import SignalMaker

class PacketModel(SignalMaker):
    signal_update = "update"
    signal_change = "change"
    
    def __init__(self, packet = None):
        SignalMaker.__init__(self)
        self.handlers = {PacketModel.signal_update:[]}        
        self.packet = packet

    def set_packet(self, packet):
        self.packet = packet
        self.notify(PacketModel.signal_update)

    def update(self):
        self.notify(PacketModel.signal_update)
