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
import socket


# encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')
dir_path = os.path.dirname(os.path.realpath(__file__))

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
    #print result

    # Run speed SYN scan nmap for IP
    with open(dir_path+'/scope/IP.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            ip = line
            try:
                # check ip
                socket.inet_aton(ip)
                #
                print(bcolors.GREEN + "Быстрое сканирование хоста: " + ip + bcolors.BLACK)
                cmd = "nmap -sS -T4 " + ip + " -oN " + dir_path + '/logs/nmap_syn_' + ip + '.txt'
                result = os.system(cmd)
                print result
                #
            except socket.error:
                # error
                print(bcolors.RED + "Неверный IP адрес: "  + ip + bcolors.BLACK)

    # Run speed UDP scan nmap for IP
    #with open(dir_path + '/scope/IP.txt') as f:
    #    lines = f.read().splitlines()
    #    cmd = "nmap -sU " + lines[0] + " -oN " + dir_path+'/logs/nmap_udp_' + lines[0] + '.txt'
    #    result = os.system(cmd)
    #    print result

    # Run full SYN scan nmap for IP
    #with open(dir_path + '/scope/IP.txt') as f:
    #    lines = f.read().splitlines()
    #    cmd = "nmap -sS -T4 -p- " + lines[0] + " -oN " + dir_path+'/logs/nmap_full_' + lines[0] + '.txt'
    #    result = os.system(cmd)
    #    print result



except KeyboardInterrupt:
    # quit
    print(" ")
    print(bcolors.RED + "Процесс прерван пользователем" + bcolors.BLACK)
    print(" ")
    sys.exit()
