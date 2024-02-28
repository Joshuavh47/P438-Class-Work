from typing import BinaryIO
import socket
import time

def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    print("Hello, I am a server")
    if fp==None:
        fp=''
    if iface is None:
        iface=''
    
    f = open(fp.name,"wb")
    

    if not use_udp:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((iface,port))
            s.listen(1)
            while True:
                conn, addr=s.accept()
                while True:
                    data=conn.recv(1024)
                    f.write(data)
                    if not data:
                        f.close()
                        s.close()
                        return
                    
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((iface,port))
            while True:
                data,addr=s.recvfrom(1024)
                f.write(data)
                if not data:
                    f.close()
                    s.close()
                    return
        






def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    print("Hello, I am a client")
    f=open(fp.name,"rb")
    print(fp)

    
    
    if not use_udp:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.connect((host,port))
            s.sendall(f.read())
            s.sendall(b'')
            f.close()
            s.close()
            return
                
                
                
    else:
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
            while True:
                buff=f.read(1024)
                if not buff:
                    
                    s.sendto(b'',(host,port))
                    f.close()
                    s.close()
                    return
                s.sendto(buff,(host,port))
                
                
                
                
                

                
