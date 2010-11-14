# coding=UTF-8
__author__="Alex Korovyansky"
__date__ ="$15.04.2010 12:15:36$"

import pygtk
pygtk.require('2.0')
import gtk

from scapy.config import conf
from scapy.layers.all import *
from scapy.packet import *
from scapy.fields import *
from scapy.base_classes import SetGen

from beaver.func import subclasses
from beaver.config import LOGGER as logger
from beaver.menu_features import *    

class PacketDumpViewController(object):
    
    def __init__(self, model, view):
        pass
