#!/usr/bin/env python3 

import os 
import argparse
from rich import print as printf 
import sys 
import qrcode 
import subprocess


def run_command(command):
    output, _ = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True).communicate()
    return output.decode("utf-8").rstrip('\r\n')

def get_ssid():
    '''get ssid of your wifi ssids'''

    try:
        ssid = run_command(f"nmcli -t -f active,ssid dev wifi | grep '^yes:' | sed 's/^yes://'")
    except:
        printf ("[Bold][Red] Error check your Network Manager[/Bold][/Red]")
        sys.exit(1)

    return ssid

def get_password(ssid):
    ''' get the password of your wifi'''
    get_password_command = f"nmcli -s -g 802-11-wireless-security.psk connection show '{ssid}'"

    # check sudo previlage
    password = run_command(f"sudo {get_password_command}") if os.getegid() != 0 else run_command(get_password_command)
    if password =="" :
        printf ("[Bold][Red] Error password not found /Bold][/Red]")
        sys.exit(1)
    return password

