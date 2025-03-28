import socket

def send_request(method, path, body=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"  # Fixed IP Address
    port = 12345
    client_socket.connect((host, port))

    headers = (
        f"{method} {path} HTTP/1.1\r\n"  # Fixed request line
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
    )

    if method == "POST" and body:
        headers += f"Content-Length: {len(body)}\r\n"
        headers += "Content-Type: application/x-www-form-urlencoded\r\n"

    headers += "\r\n"

    request = headers.encode()

    if body:
        request += body.encode()

    client_socket.sendall(request)  # Use sendall to ensure full data transmission

    response = b""
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        response += data

    print(f"\n{method} {path} Response:\n", response.decode(errors='ignore'))
    client_socket.close()


send_request("GET", "/")
