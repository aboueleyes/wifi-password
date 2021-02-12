#!/usr/bin/env python3 

import os 
import argparse
from rich import print as printf 
import sys 
import qrcode 
import subprocess


def run_command(command):
    ''' return the stdout od command'''
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

def generate_qr(ssid, password):
    ''' generate qr code'''
    
    qr_text = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=8,
                       border=4)
    qr.add_data(qr_text)
    qr.make()
    qr.print_tty()
   
def main():
    ssid = get_ssid()
    password = get_password(ssid)
    generate_qr(ssid,password)


main()    

   
