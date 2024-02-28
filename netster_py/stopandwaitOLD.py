from typing import BinaryIO
import time
import socket
import struct
import binascii
import hashlib
import pdb

def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    breakpoint()
    f = open(fp.name,"wb")
    if iface is None:
        iface=''
    
    seq=0
    unpacker=struct.Struct('? I I 462s 32s') #ack (1 bit) seq (4 bytes) size (4 bytes) data(231 bytes) checksum (16 bytes) = 255 bytes and 1 bit < 256 bytes
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((iface,port))
        seq=0
        while True:
            print("receiving packet")
            data,addr=s.recvfrom(1024)
            print("received packet")
            packet=unpacker.unpack(data)
            packet_values=(packet[0],packet[1],packet[2])
            data=struct.Struct('? I I 462s')
            checksum=hashlib.md5(data.pack(*packet_values)).hexdigest().encode()
            if checksum==packet[4] and seq==packet[1]:
                print("constructing ack")
                packer=struct.Struct('? I I 462s')
                empty_hex_string=binascii.hexlify("")
                packer_values=(True,seq,0,empty_hex_string)
                packed_no_checksum=packer.pack(*packer_values)
                ack_checksum=hashlib.md5(packed_no_checksum).hexdigest()
                final_ack_values=(True,seq,0,empty_hex_string,ack_checksum)
                ack_packer=struct.Struct('? I I 462s 32s')
                ack=ack_packer.pack(*final_ack_values)
                print("sending ack")
                s.sendto(ack,(iface,port))
                if binascii.unhexlify(packet[3]) is None:
                    f.close()
                    s.close()
                    return
                f.write(binascii.unhexlify(packet[3]))
                seq+=1





            

            



def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    breakpoint()
    f = open(fp.name,"rb")
    if host is None:
        host=''
    
    unpacker=struct.Struct('? I I 462s 32s') #ack (1 bit) seq (4 bytes) size (4 bytes) data(231 bytes) checksum (16 bytes) = 255 bytes and 1 bit < 256 bytes
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        

        seq=0
        while True:
            buff=f.read(231)
            buff_length=len(buff)
            data=struct.Struct('? I I 462s')
            hexBuff=binascii.hexlify(buff)
            values=(False,seq,buff_length,hexBuff)
            packed_data=data.pack(*values)
            checksum=hashlib.md5(packed_data).hexdigest().encode()

            values=(False,seq,len(buff),hexBuff,checksum)
            packet_struct=struct.Struct('? I I 462s 32s')
            packet_data=packet_struct.pack(*values)
            packet_data=packet_data
            print("packed and signed")
            
            while True:
                
                s.sendto(packet_data,(host,port))
                print("sent to server")
                sendtime=time.perf_counter()
                while time.perf_counter()-sendtime<.06:
                    data,addr=s.recvfrom(1024)
                if data is not None:
                    print("awaiting ack")
                    ack_packet=unpacker.unpack(data)
                    ack_values=(ack_packet[0],ack_packet[1],ack_packet[2])
                    ack_packer=struct.Struct('? I I 462s')
                    packed_ack=ack_packer.pack(*ack_values)
                    if ack_packet[0]==True and ack_packet[4]==hashlib.md5(packed_ack).hexdigest and ack_packet[1]==seq:
                        if not buff:
                            f.close()
                            s.close()
                            return
                        seq+=1
                        break

                


        
    
                
    
