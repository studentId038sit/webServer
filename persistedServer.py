import socket
import os

PERSISTENT = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 40)

host = '127.0.0.1'
port = 8080
server.bind((host, port))

server.listen(5)
print(f"web server is running on {host}:{port} PERSISTENT: {PERSISTENT}")

html_content = """
<!DOCTYPE html>
<html>
<head><title>My Mini Web Server</title></head>
<body>
<h3>Yo Dude, Check This Out!</h3>
<p>Here’s a cool image:</p>
<img src="spongebob-pictures-bhnz9xwx0n4a4k2t.jpg">
<img src="pic.jpg">
<img src="spongebob-pictures-bhnz9xwx0n4a4k2t.jpg">
<img src="pic.jpg">
<img src="spongebob-pictures-bhnz9xwx0n4a4k2t.jpg">
<img src="pic.jpg">
<img src="spongebob-pictures-bhnz9xwx0n4a4k2t.jpg">
<img src="pic.jpg">
</body>
</html>
"""

while True:
    try: 
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address}")

        while True: 
            request = client_socket.recv(1024).decode()
            if not request:
                break
            print(f"Request:\n {request}")

            request_lines = request.split('\n')[0]
            path = request_lines.split(' ')[1]

            print(request_lines)
            print(path)
            print("hello")
            

            if path == '/':
                response_body = html_content
                content_type = "text/html"
                status = "200 OK"
            elif path == f'{path}':
                file_name = path.split('/')[1]
                print(file_name)
                if os.path.exists(f"{file_name}"):
                    with open(f"{file_name}", 'rb') as f:
                        response_body = f.read()
                    content_type = "image/jpeg"
                    status = "200 OK"
                else:
                    response_body = b"File not found"
                    content_type = "text/plain"
                    status = "404 Not Found"
            else:
                response_body = b"File not found"
                content_type = "text/plain"
                status = "404 Not Found"
            
            if isinstance(response_body, str):
                response_body = response_body.encode()

            headers = (
                    f"HTTP/1.1 {status}\r\n"
                    f"Content-Type: {content_type}\r\n"
                    f"Content-Length: {len(response_body)}\r\n"

            )
            
            if not PERSISTENT:
                headers += "Connection: close\r\n"
            headers += "\r\n"
            response = headers.encode() + response_body

            # Send the response
            client_socket.send(response)

            # Non-persistent: close after each response
            if not PERSISTENT:
                client_socket.close()
                break

    
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()


server.close()