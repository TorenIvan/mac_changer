import sys
import getopt
import re
import commands
import random
import subprocess
import os
from itertools import imap
from random import randint

#find the mac address of the device you want to change
def checkifvalid(device):
    mac1 = commands.getoutput("ifconfig " + device + "| grep ether | awk '{ print $2 }'")
    mac2 = commands.getoutput("ifconfig " + device + "| grep HWaddr | awk '{ print $5 }'")
    if len(mac1)==17:
        return mac1
    elif len(mac2)==17:
        return mac2
    else:
        return 0

#generate a random mac address
def rand_mac():
    while True:
        mac = commands.getoutput("od -An -N6 -tx1 /dev/urandom | sed -e 's/^  *//' -e 's/  */:/g' -e 's/:$//' -e 's/^\(.\)[13579bdf]/\10/'")
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
            break
        else:
            continue
    return mac

def change_the_mac(device,random):
    subprocess.call(['ifconfig ' +device+ ' down'], shell=True)
    subprocess.call('service network-manager stop', shell=True)
    subprocess.call(['ifconfig ' +device+ ' hw ether ' +random ], shell=True)
    subprocess.call(['ifconfig ' +device+ ' up'], shell=True)
    subprocess.call('service network-manager start',shell=True)


def main(argv):
    if os.geteuid()!=0:
        exit("You need to have root priviledges to run this script.\nPlease try again, this time using 'sudo python ch_mac.py -h' to see exactly what it needs. Exiting.")
    device=''
    if len(sys.argv)==1:
        print 'sudo python ch_mac.py -i <device>'
        sys.exit()
    try:
        opts, args=getopt.getopt(argv,"hi:",["idevice="])
    except getopt.GetoptError:
        print 'sudo python ch_mac.py -i <device>'
        sys.exit(2)
    for opt, arg in opts:
        if opt=='-h' or opt=='--help':
            print 'sudo python ch_mac.py -i <device>'
            sys.exit()
        elif opt in ("-i", "--idevice"):
            device=arg
    print 'Device =', device
    mac=checkifvalid(device)
    if mac==0:
        print 'device is not valid'
    else:
        print 'old mac =', mac

    random=rand_mac()
    print 'new mac =', random

    #change the mac address
    change_the_mac(device,random)
    exit()

if __name__ == '__main__':
    main(sys.argv[1:])

