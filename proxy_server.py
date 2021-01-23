import socket
import time
from multiprocessing import Process 

#define address & buffer size
HOST = "www.google.com"
PORT = 80
BUFFER_SIZE = 1024

PROXYHOST = ""
PROXYPORT = 8001

def handleProxy(conn, addr):
    while True:
        client_data = conn.recv(BUFFER_SIZE)
        print("THIS IS CLIENT DATA", client_data)

        if not client_data:
            break

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as googleSocket:
            googleSocket.connect((HOST, PORT))
            googleSocket.sendall(client_data)
            google_data = googleSocket.recv(BUFFER_SIZE)
            if not google_data:
                break
            conn.sendall(google_data)         

def main():
    #create server socket and bind it
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxyServer:
        proxyServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxyServer.bind((PROXYHOST,PROXYPORT)) 
        proxyServer.listen(1)
    
        while True:
            conn, addr = proxyServer.accept()
            print("Connected by", addr)

            # forking so multiple programs can use 
            p = Process(target=handleProxy, args=(conn, addr))
            p.daemon = True
            p.start()
            conn.close()

        
if __name__ == "__main__":
    main()
