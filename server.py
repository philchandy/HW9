# A simple program that will create a server that would echo a client request back to the client

import socket
import sys

if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <port>")
    sys.exit(1)

#get local ip addr
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(('8.8.8.8', 80))
    HOST = s.getsockname()[0]
except Exception:
    HOST = socket.gethostbyname(socket.gethostname())
s.close()

PORT = int(sys.argv[1])

print(f"\nServer IP address: {HOST}\n")
print(f"Server port number: {PORT}\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print("\nReady to serve...")
    while True:
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                request_text = data.decode()
                filename = request_text.split()[1].lstrip('/')

                try:
                    with open(filename, 'rb') as f:
                        body = f.read()
                    headers = '\nHTTP/1.1 200 OK\n\n'
                except FileNotFoundError:
                    headers = '\nHTTP/1.1 404 Not Found\n\n'
                    body = b''

                success_msg = '\nConnection Successful!\n'
                success_msg += '\n---------------HTTP RESPONSE---------------\n\n'
                end_msg = '\n---------------END OF HTTP RESPONSE---------------\n'

                res = success_msg.encode() + headers.encode() + body
                res += end_msg.encode()
                conn.sendall(res)
