#!/usr/bin/python
# -*- coding: utf8 -*-

import threading
import time
import os
import string
import sys
import requests
import re
import datetime

# encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')


class bcolors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    GREY = '\033[97m'
    BLACK = '\033[30m'

try:
    print "####################################################"
    print "####################   WILLANI   ###################"
    print "####################################################"


    # Get version nmap
    cmd = "nmap -V"
    result = os.system(cmd)
    print result

    # Get Ip addresses
    with open('IP.txt') as f:
        lines = f.read().splitlines()
        print lines


except KeyboardInterrupt:
    # quit
    print(" ")
    print(bcolors.RED + "Процесс прерван пользователем" + bcolors.BLACK)
    print(" ")
    sys.exit()
