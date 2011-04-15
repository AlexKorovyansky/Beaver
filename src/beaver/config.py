# coding=UTF-8

## This file is part of Beaver
## See https://github.com/korovyansk/Beaver for more informations
## Copyright (C) Alex Korovyansky <korovyansk@gmail.com>
## This program is published under a GPLv2 license

__author__="Alex Korovyansky"
__date__ ="$15.04.2010 12:15:36$"

import logging
import random

def make_logger():
    logger = logging.getLogger("tcpip-logger")
    logger.setLevel(LOGGER_LEVEL)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(LOGGER_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

#настройки для консоли
CONSOLE_KEYS_FOLDER = "keys"
CONSOLE_SCRIPTS_FOLDER = "scripts"
CONSOLE_MACROSCRIPT_FOLDER = "macroscripts"
CONSOLE_KEYS_FILETYPE = ".tu-keys"
CONSOLE_LANG_FOLDER = "lang"
CONSOLE_LANG = "default"
CONSOLE_VERSION = "1.0.1"

#настройки для оконечной точки
ENDPOINT_PARAMERT1 = "parametr1"
ENDPOINT_SCRIPTS_FOLDER = "scripts"

#настройки редактора
import os.path
EDITOR_PLUGINS_FOLDER = os.path.join("plugins", "editor")

#общие настройки
LOGGER_LEVEL = logging.INFO
LOGGER_FORMAT = "%(levelname)s : %(message)s"
LOGGER = make_logger()

ENDPOINT_MANAGMENT_PORT = 2011
CONSOLE_PUBLIC_CERTIFICATE_FILETYPE = ".tu-cpc"
TCPIP_MACRO_SCRIPT_FILETYPE = ".tu-mscript"
TCPIP_SCRIPT_FILETYPE = ".tu-script"
