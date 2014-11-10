#!/usr/bin/env python
#
# !!! Needs psutil & netifaces installing:
#
#    $ sudo pip install psutil netifaces
#

import os
import sys
from time import sleep
if os.name != 'posix':
    sys.exit('platform not supported')

from datetime import datetime
import psutil
import lcdSOM as lcd
import netifaces as ni

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n
    
def cpu_usage():
    # load average, uptime
    av1 = psutil.cpu_percent(interval=None)
    #av1, av2, av3 = os.getloadavg()
    return "Load:      %.1f%%" \
            % (av1 )

def uptime():
    # uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.BOOT_TIME)
    return "Up:     %sh" \
            % (str(uptime).split('.')[0])
    
def mem_usage():
    usage = psutil.phymem_usage()
    return "Mem Used:   %s" \
            % (bytes2human(usage.used))  

    
def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SDCard:   %s %.0f%%" \
            % (bytes2human(usage.used), usage.percent)  

def network(iface):
    stat = psutil.network_io_counters(pernic=True)[iface]
    return "%s:Tx%s,Rx%s"% \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))

def ipaddr(iface):
    ip = ni.ifaddresses(iface)[2][0]['addr']
    return " %s" % \
           (ip)

def battinfo():
    bat = "/sys/class/power_supply/battery/uevent"
    for line in open(bat):
        if 'STATUS' in line:
	    status = line.split('=')[1]
	if 'CAPACITY' in line:
	    capacity = line.split('=')[1]
    fmt = "%s:%.0f%%" % (status.rstrip(),float(capacity.rstrip()))
    n = 16 - len(fmt)
    space = ""
    for i in range(n):
       space+= " "
    return "%s:%s%.0f%%" % (status.rstrip(),space,float(capacity.rstrip()))	
    
def stats():

    #lcd.str(0,"Olimexino:")
    lcd.longstr(0,"   Olinuxino:   ",1)
    lcd.str(1,cpu_usage())
    lcd.str(2,uptime())
    lcd.str(3,mem_usage())
    #lcd.str(4,disk_usage('/'))
    lcd.str(4,battinfo())
    try:
    	lcd.str(5,ipaddr('wlan7'))
    except:
    	lcd.str(5,"    no ip yet   ")

    lcd.update()    
    
def main():
    try:
	    lcd.init()
	    lcd.clear()
	    while True:
	        stats()
	        sleep(1)
    except:
	    lcd.init()
	    lcd.clear()

if __name__ == "__main__":
    main()
