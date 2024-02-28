from typing import BinaryIO
import time
import socket
import struct
import binascii
import hashlib
import pdb

def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    
    
    if iface is None:
        iface=''
    ack_encoded=None
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((iface,port))
        s.settimeout(.06)
        seq=0
        while True:
            try:
                #print("receiving packets")
                data,conn=s.recvfrom(1024)
                if data is not None:
                    #print(data)
                    if data == b'end':
                        end=True
                        end_hash=hashlib.md5("end".encode()).hexdigest()
                        end_packet="1 "+str(seq)+" 3 "+end_hash
                        for i in range(100):
                            s.sendto(end_packet.encode(),conn)
                        s.close()
                        fp.close()
                        return

                    #print(str(conn[0])+" "+str(conn[1]))
                    #print("packet received")
                    #data_decoded=data.decode()
                    packet=data[0:len(data)-33]
                    checksum=hashlib.md5(data[:len(data)-33]).hexdigest()
                    packet_split=data.split(b' ')
                    
                    """
                    for i in packet_split:
                        print(i)
                    if data[2:10] != seq.to_bytes(8,"big"):
                        print("seq's not equal")
                    """
                    if packet_split[len(packet_split)-1] == checksum.encode() and int.from_bytes(data[2:10],"big") == seq:
                        #print("packet valid")
                        ack="1 "+str(seq)+" 0 "+checksum
                        if int.from_bytes(data[2:10],"big") < seq:
                            ack="1 "+data[2:10]+" 0 "+checksum
                        ack_encoded=ack.encode()
                        #print(data[13:len(data)-33])
                        fp.write(data[13:len(data)-33])
                        s.sendto(ack_encoded,conn)
                        seq+=1
                    else:
                        #print(data)
                        #print(seq)
                        #print(b"seq="+data[2:10]+b" ackseq="+seq.to_bytes(8,"big")+b" checksum="+packet_split[len(packet_split)-1]+b" ack checksum="+checksum.encode())
                        #print(int.from_bytes(packet_split[1],"big"))
                        print("invalid")
            except socket.timeout:
                if seq!=0:
                    s.sendto(ack_encoded,conn)
                    print("dropped ack")
                

        
        
            

            

            



def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:

    if host is None:
        host=''
    
    received=True
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(.06)
        seq=0
        end=False
        while True:
            if received==True:
                received=False
                buff=fp.read(178)
                buff_size=len(buff)
                if buff_size <= 0:
                    s.sendto(b'end',(host,port))
                    end=True
                    #print("end")
                    break
                #print("signing packet")
                values=(0).to_bytes(1,"big")+b" "+seq.to_bytes(8,"big")+b" "+(buff_size).to_bytes(1,"big")+b" "+buff
                
                #encoded_vals=values.encode()
                encoded_vals=values
                checksum=hashlib.md5(encoded_vals).hexdigest()
                values+=b" "+checksum.encode()
            #print("sending packet")
            s.sendto(values,(host,port))
            #start_time=time.perf_counter()
            #print("receiving ack")
            try:
                data,conn=s.recvfrom(1024)
                #print("receiving ack")

                if data is not None:
                    split_data=data.decode().split()
                    #print("received ack")
                    #print(data.decode()[len(data.decode())-32:len(data.decode())])
                    #if split_data[len(split_data)-1]==checksum:
                        #print("test")
                        #print(int(split_data[1]))
                        #print(int(split_data[0]))
                        #print(seq)
                        #print(split_data[len(split_data)-1])
                    if int(split_data[0]) == 1 and int(split_data[1]) == seq:
                        ack_checksum=split_data[len(split_data)-1]
                        if end==True:
                                if ack_checksum==hashlib.md5("end".encode()).hexdigest():
                                    s.close()
                                    fp.close()
                                    return
                                received=True
                        if ack_checksum==checksum:
                            #print("checksum matches")
                            received=True
                            seq+=1
            except socket.timeout:
                print("timeout")
                #continue
            
            
        
        