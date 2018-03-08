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
from time import gmtime, strftime
import subprocess
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--scan", default='fast', help="Режим сканирования full или fast")
args = parser.parse_args()

# encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')
dir_path = os.path.dirname(os.path.realpath(__file__))


timezone = subprocess.check_output('date +"%Z"', shell=True)
#print timezone

if timezone.strip() != 'MSK':
    try:
        if raw_input('Часовой пояс не московский! Продолжить? [y/n]').lower()[0]!='y':
            print("Попробуйте запустить: dpkg-reconfigure tzdata")
            exit(1)
    except:
        print("Попробуйте запустить: dpkg-reconfigure tzdata")
        exit(1)

class bcolors:
    RED = '\033[91m' # ошибки
    GREEN = '\033[92m' # уведомление
    YELLOW = '\033[93m' # предупреждение
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    GREY = '\033[97m'
    BLACK = '\033[30m' # обычный

def check_service(ip, port):
    global bcolors
    global directory
    global subprocess
    port = re.findall('(\d+)', port)
    cmd = "nmap -sS -sV " + str(ip) + " -p " + str(port) + " -oN " + directory + '/nmap_check_service_' + str(ip) + '_' + str(port) + '.txt'
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ports = re.findall(".*tcp", output.stdout.read(), re.MULTILINE)
    return ports

def progress(count, total, status=''):
    global bcolors
    bar_len = 50
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write(bcolors.BLACK + '[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

try:
    print "####################################################"
    print "####################   WILLANI   ###################"
    print "####################################################"

    if args.scan == 'fast':
        print(bcolors.GREEN + "Режим быстрого сканирования" + bcolors.BLACK)
        nmapscan = ''
    if args.scan == 'full':
        print(bcolors.GREEN + "Режим полного сканирования" + bcolors.BLACK)
        nmapscan = ' -p- '

    # Get version nmap
    cmd = "nmap -V"
    output = subprocess.check_output(cmd, shell=True)
    #print output

    # Run speed SYN scan nmap for IP
    with open(dir_path+'/scope/IP.txt') as f:
        lines = f.read().splitlines()
        total = len(lines)
        count = 0
        #print total
        i = 0
        while i <= 1000:
            i = i + 1
            directory = os.path.dirname(dir_path + '/logs/report' + str(i) + '/file')
            try:
                os.stat(directory)
            except:
                os.mkdir(directory)
                break
        print(bcolors.GREEN + "Отчет будет сохранен в каталоге: " + str(directory) + bcolors.BLACK)

        with open(directory + '/summary.csv', 'a+') as f:
            f.write('IP;Ports \n')

        for line in lines:
            #
            ip = line
            stime = strftime("%d-%m-%Y_%H:%M:%S", gmtime())
            try:
                # check ip
                socket.inet_aton(ip)
                #
                print(bcolors.GREEN + "Сканирование хоста: " + ip + bcolors.BLACK)
                sstatus = 'total:' + format(total) + ' count:' + format(count)
                progress(count, total, status=sstatus)
                cmd = "nmap -sS -T4 " + ' ' + nmapscan + ' ' + ip + " --open -oN " + directory + '/nmap_syn_' + ip + '_' + stime + '.txt'
                #result = os.system(cmd)
                start = time.time()
                output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                while output.poll() is None:
                    sleep(0.5)
                    # Подсчет времени выполнения
                    elapsed = time.time()
                    elapsed = int(elapsed - start)
                    out = " | Время задачи: " + str(elapsed) + " сек."
                    sstatus = 'Всего:' + format(total) + ' Выполнено:' + format(count) + out
                    # Выводим прогрессбар
                    progress(count, total, status=sstatus)
                #print output
                items = re.findall(".*tcp", output.stdout.read(), re.MULTILINE)
                if len(items) > 0:
                    print("Найдены следующие порты:                                                                                                ")
                    for x in items:
                        print x
                        ports = check_service(ip, x)
                        for port in ports:
                            print port
                    with open(directory + '/summary.csv', 'a+') as f:
                        f.write(ip + ";" + ', '.join(items) + '\n')
                else:
                    print("Открытых портов не обнаружено.                                                                                          ")
                    with open(directory + '/summary.csv', 'a+') as f:
                        f.write(ip + ";Открытых портов не обнаружено.\n")
                #

            except socket.error:
                # error
                print(bcolors.RED + "Неверный IP адрес: "  + ip + bcolors.BLACK)
            # Обновление счетчика
            count += 1


except KeyboardInterrupt:
    # quit
    print(" ")
    print(bcolors.RED + "Процесс прерван пользователем" + bcolors.BLACK)
    print(" ")
    sys.exit()
