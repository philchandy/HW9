# Client program to send data to a server via a socket, and then have that same data echoed back.
import socket
import sys

if len(sys.argv) < 4:
    print(f"Usage: python {sys.argv[0]} <server_ip> <port> <html_filename>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
PORT = int(sys.argv[2])
filename = sys.argv[3]

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        request = f"GET /{filename} HTTP/1.1\n"
        s.sendall(request.encode())

        data = b""
        
        chunk = s.recv(1024)
        data += chunk

        if not data:
            print("Error while connecting!")
            sys.exit(1)
        
        print(data.decode())

except Exception as e:
    print("Error while connecting!")