import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "www.google.com"
port = 80
client_socket.connect((host, port))

request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

client_socket.send(request.encode())

response = ""
while True:
    try:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        response += chunk.decode()
    except Exception as e:
        print(f"Error: {e}")
        break

print("Respose from google:\n", response)