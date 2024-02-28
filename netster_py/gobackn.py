from typing import BinaryIO
import time
import socket
import struct
import binascii
import hashlib
import pdb

def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
    if iface is None:
        iface=''
    seq=0
    baseSeq=0
    N=10000
    signed_ack=None
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(.06)
        s.bind((iface,port))
        while True:
            try:
                for i in range(N):
                    data,addr=s.recvfrom(1024)
                    if data == b'end':
                        fp.close()
                        s.close()
                        print("success")
                        return
                    data_split=data.split(b' ')
                
                    if verify_packet(data) == True:
                        #print("valid")
                        
                        if int.from_bytes(data[2:10],"big") == seq:
                            #print(int.from_bytes(data[2:10],"big"))
                            #print("test")
                            fp.write(data[13:len(data)-33])
                            seq+=1
                            ack=(0).to_bytes(1,"big")+b" "+data[2:10]+b" "+(0).to_bytes(1,"big")
                            signed_ack=ack+b" "+hashlib.md5(ack).hexdigest().encode()

                    
                    s.sendto(signed_ack, addr)
                    if seq != baseSeq:
                        baseSeq=seq
                
                
            
                
            except socket.timeout:
                if seq!=0:
                    s.sendto(signed_ack,addr)
                print("timeout")



def verify_packet(data:bytes):
    split_packet=data.split(b' ')
    values=data[0:len(data)-33]
    checksum=split_packet[len(split_packet)-1]
    if hashlib.md5(values).hexdigest() == checksum.decode():
        return True
    return False
    

def sign_packet(ack:int, seq:int, length:int, data:bytes):
    unsigned_packet=ack.to_bytes(1,"big")+b" "+seq.to_bytes(8,"big")+b" "+length.to_bytes(1,"big")+b" "+data
    checksum=hashlib.md5(unsigned_packet).hexdigest()
    signed_packet=unsigned_packet+b" "+checksum.encode()
    return signed_packet


def gbn_client(host:str, port:int, fp:BinaryIO) -> None:
    seq=0
    base=0
    N=10000
    max=base+N-1
    window=[None]*N
    for i in range(N):
        temp=fp.read(178)
        if len(temp) != 0:
            window[i]=sign_packet(0,i,len(temp),temp)
            max=i
        N=max-base+1
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(.06)
        while True:
            if N == 0:
                while data != b'end':
                    try:
                        s.sendto(b'end',(host,port))
                        data,addr=s.recvfrom(1024)
                    except socket.timeout:
                        continue
                fp.close()
                s.close()
                print("success")
                return
            for i in range(N):
                s.sendto(window[i],(host,port))
                
            try:
                
                data,addr=s.recvfrom(1024)
                data_split=data.split(b' ')
                print(int.from_bytes(data[2:10],"big"))
                if verify_packet(data) == True:
                    print("valid")
                    print(int.from_bytes(data[2:10],"big"))
                    if int.from_bytes(data[2:10],"big")-seq < 0:
                        continue
                    for i in range(int.from_bytes(data[2:10],"big")-seq+1):
                        for i in range(N-1):
                            window[i+1]=window[i]
                        seq+=1
                        base=seq
                        temp=fp.read(178)
                        if len(temp)==0:
                            N=N-1
                        max=base+N-1

                        if len(temp) != 0:
                            window[max-base]=sign_packet(0,max-1,len(temp),temp)
                        else:
                            window[max-base]=None
            except socket.timeout:
                for i in range(N):
                    s.sendto(window[i],(host,port))
