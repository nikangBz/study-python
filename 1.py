#!/usr/bin/python
#by Kuhn 2014-03-29
#Updata by Derek.s && Jason 2018-04-09

import sys
import os
import telnetlib
import getpass
import datetime
import pexpect
import re

host = ""
user = "123"
password = "123"
#password = "123"
enpw = "123"
h3cpw = "123"
tftpserver = "8.8.8.8"
now = datetime.datetime.now()

def main():
    for host in open("sw.txt", "r").readlines(): 
        dsthost = host.strip('\n')
        try:
            tn = telnetlib.Telnet(dsthost,port=23,timeout=10)
        except:
            print "Can't connection %s"%dsthost
            continue
        #tn.read_until("Username:")
        #tn.write(user+"\n")
        try:
            tn.read_until("Password:")
            tn.write(password+"\n")
            result = tn.read_some()
            rex_h3c_bin_1 = r'%Wrong password'
            login_Failed_H3C_1 = re.search(rex_h3c_bin_1, result)
            rex_h3c_bin_2 = r'%Username or password is invalid.'
            login_Failed_H3C_2 = re.search(rex_h3c_bin_2, result)
        except:
            print "Connection error %s"%dsthost
            continue
        #print(login_Failed_H3C_1, login_Failed_H3C_2)
        if((login_Failed_H3C_1 is None) and (login_Failed_H3C_2 is None)):
            #print("cisco")
            try:
                tn.write("en\n")
                tn.read_until("Password:")
                tn.write(enpw+"\n")
                tn.read_until("#")
                tn.write("copy running-config tftp:\n")
                tn.write(tftpserver+"\n")
                tn.write(now.strftime("%Y/%m/%d")+"/"+host+"\n")
                tn.read_until("#")
                tn.close
                print now.strftime("%Y/%m/%d") + " " + dsthost + " Backup successful."
            except:
                print "Connection error %s"%dsthost
                continue
        else:
            #print("H3c")
            try:
                tn.write(h3cpw+"\n")
                tn.read_until(">")
                tn.write("tftp "+tftpserver+" put flash:/startup.cfg"+" "+now.strftime("%Y/%m/%d")+"/"+host+"\n")
                tn.read_until(">")
                tn.close
                print now.strftime("%Y/%m/%d") + " " + dsthost + " Backup successful(h3c)."
            except:
                print "Connection error %s"%dsthost
                continue

if __name__=="__main__":
    main()