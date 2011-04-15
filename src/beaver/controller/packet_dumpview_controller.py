# coding=UTF-8

## This file is part of Beaver
## See https://github.com/korovyansk/Beaver for more informations
## Copyright (C) Alex Korovyansky <korovyansk@gmail.com>
## This program is published under a GPLv2 license

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
