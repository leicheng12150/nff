import socket
from socket import inet_ntoa
from datetime import datetime

log_file=''
nflow=0

myIP=""
netflow_port=2303
backlog = 10

destIP=list()
rsocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dsocket=list()

def read_conf():
#here comes reading a file and setting up all the variables
    global log_file
    global nflow
    global myIP
    log_file = 'nff.log'
    nflow=5
    myIP=socket.gethostname()
    destIP.append('127.0.0.1')
    return

def open_socket():
#here are the sockets open for reading and forwarding
    global rsocket
    global dsocket
    #now lets open the source socket
    try:
        rsocket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as msg:
        log (msg)
    try:
        rsocket.bind(('0.0.0.0', netflow_port))
    except socket.error as msg:
        log(msg)
        s.close()

   #here come the destination sockets
    for item in range(len(destIP)):
        try:
            dsocket.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
        except socket.error as msg:
            log(msg)

    log("sockets are open")
    return

def do_forward():
#receive packets and forward them to other ifaces
    global rsocket

    data, addr = rsocket.recvfrom(1500)
    log ("received data from "+addr)
    for item in range(len(destIP)):
        try:
            dsocket[item].sendto(data,(destIP[item],netflow_port))
        except socket.error as msg:
            log(msg)
    return

def close_socket():
#closing all sockets open
    global rsocket
    global dsocket

    rsocket.close()
    for item in range(len(destIP)):
        dsocket[item].close()
    log("sockets are closed")
    return


def log(msg):
#this way one can do debugging
    flog.write('%s %s\n' % (datetime.now, msg));

#init
read_conf()

#open log
flog=open(log_file,"a")

#do the thing
open_socket()

#infinite loop
while 1:
    do_forward()
    sleep(1)

close_socket()
flog.close()
