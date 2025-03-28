import socket
import os
from datetime import datetime
import uuid  # For generating unique IDs

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to localhost:8080
host = '127.0.0.1'
port = 8080
server_socket.bind((host, port))

# Listen for connections
server_socket.listen(5)
print(f"Web server running at http://{host}:{port}...")

# Simple "database" to track user visits (in memory)
user_visits = {}

# HTML page with a form
html_content = """
<!DOCTYPE html>
<html>
<head><title>My Mini Web Server</title></head>
<body>
<h1>{greeting}</h1>
<p>Number of visits: {visit_count}</p>
<p>Here’s a cool image:</p>
<img src="pic.jpg">
<form method="POST" action="/submit">
  <label>Enter your name:</label>
  <input type="text" name="username">
  <input type="submit" value="Submit">
</form>
</body>
</html>
"""

while True:
    try:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Receive the HTTP request
        request = client_socket.recv(4096).decode(errors='ignore')
        if not request:
            client_socket.close()
            continue

        print(f"Request:\n{request}")

        # Parse the request
        lines = request.split('\r\n')
        request_line = lines[0]
        method, path, version = request_line.split(' ', 2)

        # Extract headers
        headers = {}
        body = ""
        header_done = False
        for line in lines[1:]:
            if line == "":
                header_done = True
                continue
            if header_done:
                body += line
            else:
                key_value = line.split(':', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    headers[key.strip()] = value.strip()

        # Handle cookies
        user_id = None
        visit_count = 0
        greeting = "Yo Dude, Welcome!"

        if 'Cookie' in headers:
            cookie_parts = headers['Cookie'].split('=')
            if len(cookie_parts) == 2:
                user_id = cookie_parts[1]
                if user_id in user_visits:
                    visit_count = user_visits[user_id]['visits']
                    username = user_visits[user_id].get('username', 'Dude')
                    greeting = f"Welcome Back, {username}!"
                visit_count += 1
        else:
            user_id = str(uuid.uuid4())
            visit_count = 1
            user_visits[user_id] = {'visits': visit_count, 'username': 'Dude'}

        user_visits[user_id]['visits'] = visit_count

        # Decide what to send
        status = "200 OK"
        content_type = "text/html"
        response_body = b""
        set_cookie = f"Set-Cookie: user_id={user_id}\r\n" if 'Cookie' not in headers else ""

        if path == '/':
            if method == "GET":
                response_body = html_content.format(greeting=greeting, visit_count=visit_count).encode()
            elif method == "POST":
                form_data = dict(item.split('=') for item in body.split('&') if '=' in item)
                username = form_data.get('username', 'Unknown')
                user_visits[user_id]['username'] = username
                greeting = f"Yo {username}, Nice to Meet You!"
                response_body = html_content.format(greeting=greeting, visit_count=visit_count).encode()
            else:
                status = "405 Method Not Allowed"
                response_body = b"Method not allowed"
        elif path == '/pic.jpg' and method == "GET":
            if os.path.exists('pic.jpg'):
                with open('pic.jpg', 'rb') as f:
                    response_body = f.read()
                content_type = "image/jpeg"
            else:
                status = "404 Not Found"
                response_body = b"File not found"
                content_type = "text/plain"
        elif path == '/submit' and method == "POST":
            form_data = dict(item.split('=') for item in body.split('&') if '=' in item)
            username = form_data.get('username', 'Unknown')
            user_visits[user_id]['username'] = username
            greeting = f"Yo {username}, Nice to Meet You!"
            response_body = html_content.format(greeting=greeting, visit_count=visit_count).encode()
        else:
            status = "404 Not Found"
            response_body = b"File not found"
            content_type = "text/plain"

        # Craft the HTTP response
        date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        response_headers = (
            f"HTTP/1.1 {status}\r\n"
            f"Date: {date}\r\n"
            "Server: MyMiniServer/1.0\r\n"
            f"Last-Modified: {date}\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"{set_cookie}"
            "Connection: close\r\n"
            "\r\n"
        ).encode()
        response = response_headers + response_body

        # Send the response
        client_socket.send(response)
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

server_socket.close()
