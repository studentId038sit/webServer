import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 12345
server.bind((host, port))

server.listen(1)
print(f"web server is running on {host}:{port}")

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Web Server</title>
</head>
<body>  
    <h1>this is me deep</h1>
</body>
</html> """

while True:
    try: 
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address}")
        request = client_socket.recv(1024).decode()
        print(f"Request: {request}")

        response_body = html_content
        response = (
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/html\n"
            f"Content-Length: {len(response_body)}\n"
            "\n"
            f"{response_body}"
        )

        client_socket.send(response.encode())
        client_socket.close()
    
    except Exception as e:
        print(f"Error: {e}")
        break


server.close()