import netster
import socket

connections=0

def chat_server(iface:str, port:int, use_udp:bool) -> None:
    print("Hello, I am a server")
    global connections
    if iface is None:
        iface=''
    
    if not use_udp:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((iface,port))
            s.listen(5)
            while True:
                conn, addr=s.accept()
                print(f"Connection {connections} by {addr}")
                connections+=1
                while True:
                    data=conn.recv(1024)
                    decoded=data.decode()
                    print(f'got message from {addr}')
                    if not data:
                        s.close()
                        break
                    if decoded=="hello\n":
                        conn.sendall(b'world\n') 
                    elif decoded=="goodbye\n":
                        conn.sendall(b'farewell\n')
                        conn.sendall(b'')
                        break
                    elif decoded=="exit\n":
                        conn.sendall(b'ok\n')
                        s.close()
                        return
                    else:
                        conn.sendall(data)
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((iface,port))
            while True:
                data,addr=s.recvfrom(1024)
                decoded=data.decode()
                print(f'got message from {addr}')
                if not data:
                    s.close()
                    break
                if decoded=="hello\n":
                    s.sendto(b'world\n',addr) 
                elif decoded=="goodbye\n":
                    s.sendto(b'farewell\n',addr)
                    s.sendto(b'',addr)
                    continue
                elif decoded=="exit\n":
                    s.sendto(b'ok\n',addr)
                    s.close()
                    return
                else:
                    s.sendto(data,addr)
        
    



def chat_client(host:str, port:int, use_udp:bool) -> None:
    print("Hello, I am a client")
    if not use_udp:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.connect((host,port))
            while True:
                message=input()+'\n'
                s.sendall(message.encode())
                data=s.recv(1024)
                print(data.decode(),end="")
                if message=="goodbye\n":
                    s.close()
                    break
                if message=="exit\n":
                    s.sendall(b'')
                    s.close()
                    return
    else:
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
            while True:
                message=input()+'\n'
                s.sendto(message.encode(),(host,port))
                data=s.recv(1024)
                print(data.decode(),end="")
                if message=="goodbye\n":
                    s.close()
                    break
                if message=="exit\n":
                    s.sendto(b'',(host,port))
                    s.close()
                    return
            

if __name__ == "__main__":
    print("Code for netster library")