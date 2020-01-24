# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 14:21:21 2020
@author: Florentin Popescu
"""
# --------------------------------------------

# imports
import socket
import subprocess
import sys
from datetime import datetime

# clear console
subprocess.call('clear', shell=True)
# --------------------------------------------


def get_service_name(protocol, website, lower_bound=0,\
                     upper_bound=65535, scan_step=1):
    print("protocol => {}, website => {}".format(protocol, website))
    print("port range: [{}, {}]".format(lower_bound, upper_bound))
    remoteServerIP  = socket.gethostbyname(website)
    print("CTRL+C to interupt port scan")
    
    if 0 <= lower_bound and upper_bound <= 65535 and lower_bound < upper_bound:  
        print(" ---valid port range---")
                
        try:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except:
                print("Error: can't open socket!\n")    
           
            for port in range(lower_bound, upper_bound, scan_step):
                try: 
                    conn = sock.connect_ex((remoteServerIP, port))
                    print("connecting to port {}".format(port))
                    if conn == 0:
                        print("PORT: {}  => open".format(port))
                    else:
                        print("PORT: {} => closed".format(port))
                except ConnectionRefusedError:
                    print("connection to port {} refused".format(port))
                    continue
                
                try:
                    service = socket.getservbyport(port, protocol)
                except Exception:
                    service = "unknown"
                print("SERVICE: %-15s\t" %service)
  
        except KeyboardInterrupt:
            print("You pressed Ctrl+C")
            sys.exit()
        except socket.gaierror:
            print('hostname could not be resolved; exiting')
            sys.exit()
        except socket.error:
            print("couldn't connect to server; exiting")
            sys.exit()
        sock.close()
      
    elif 0 <= lower_bound and upper_bound <= 65535\
        and lower_bound > upper_bound:
        print("port bounds incorectly indicated")
    
    else:
       print("---invalid port range---")
# --------------------------------------------


if __name__ == '__main__': 
   t1 = datetime.now()
   try:
       proto = str(input("please enter protocol type: (eg. 'tcp', 'udf')\n"))
       web = str(input("please enter website name: (eg. 'www.bp.com')\n"))
       low_port = int(input("please enter ports lower bond as integer\n"))
       high_port = int(input("please enter ports upper bound as integer\n"))
       get_service_name(proto, web, low_port, high_port, 1)
   except Exception as err:
       print("incorect entry")
       print(err)
   t2 = datetime.now()
   print("port/services sanning completed in:", t2 - t1)


# ==============================================
# ============== SAMPLE RUN ====================
# please enter protocol type: (eg. 'tcp', 'udf')
# tcp
# please enter website name: (eg. 'www.bp.com')
# www.bp.com
# please enter ports lower bond as integer
# 20
# please enter ports upper bound as integer
# 30
# protocol => tcp, website => www.bp.com
# port range: [20, 30]
# CTRL+C to interupt port scan
#  ---valid port range---
# connecting to port 20
# PORT: 20 => closed
# SERVICE: ftp-data               
# connecting to port 21
# PORT: 21 => closed
# SERVICE: ftp                    
# connecting to port 22
# PORT: 22 => closed
# SERVICE: ssh                    
# connecting to port 23
# PORT: 23 => closed
# SERVICE: telnet                 
# connecting to port 24
# PORT: 24 => closed
# SERVICE: unknown                
# connecting to port 25
# PORT: 25 => closed
# SERVICE: smtp                   
# connecting to port 26
# PORT: 26 => closed
# SERVICE: unknown                
# connecting to port 27
# PORT: 27 => closed
# SERVICE: unknown                
# connecting to port 28
# PORT: 28 => closed
# SERVICE: unknown                
# connecting to port 29
# PORT: 29 => closed
# SERVICE: unknown                
# port/services sanning completed in: 0:03:37.782812