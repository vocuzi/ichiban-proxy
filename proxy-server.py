import socket, sys
from threading import Thread
try:
    listening_port=int(sys.argv[2])
except Exception,e:
    print "Usage : celare --port 8000"
max_conn = 5
buffer_size = 8192
def start():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print "Sockets Initialized ... [OK]"
        s.bind(('',listening_port))
        print "Sockets Binded ... [OK]"
        s.listen(max_conn)
        print "Celare Started on port {0} ... [OK]".format(listening_port)
        while True:
            try:
                conn,addr=s.accept()
                data=conn.recv(buffer_size)
                t=Thread(target=conn_string,args=(conn,data,addr,))
                t.start()
            except Exception,e:
                fp=open("/var/log/celare.log","wb")
                fp.write(str(e))
                fp.close()
                print "Error Occurred ... [LOGGED]"
        s.close()
    except Exception, e:
        print "Celare Started ... [FAILED]"
        print "Error : {0}".format(str(e))
        sys.exit(2)
def conn_string(conn,data,addr):
    try:
        request_server=data.split("Host")[1].split("\n")[0].split(" ")[1]
        request_port=80
        if request_server.find(":")!=-1:
            request_port=int(request_server.split(":")[1])
            request_server=request_server.split(":")[0]
        proxy_server(request_server,request_port,conn,data,addr)
    except Exception,e:
        fp=open("/var/log/celare.log","wb")
        fp.write(str(e))
        fp.close()
        print "Error Occurred ... [LOGGED]"
def proxy_server(server,port,conn,data,addr):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((server,port))
        s.send(data)
        while 1:
            reply=s.recv(buffer_size)
            if len(reply)>0:
                conn.send(reply)
                print "Processed {0} > {1} ... [DONE]".format(str(addr[0]),len(reply))
            else:
                print "Server Sent Nothing back"
                break
        s.close()
        conn.close()
    except Exception, e:
        print e
start()
#Fri-26Jan
