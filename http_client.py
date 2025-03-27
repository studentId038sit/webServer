import socket

def send_request(method, path, body=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8080
    client_socket.connect((host, port))

    headers = (
        f"{method} {path} HTTP/1.1/\r\n"
        f"Host:{host}\r\n"
        f"Connection: keep-alive\r\n"
    )

    if method == "POST":
        headers += f"Content-Length: {len(body)}\r\n"
    headers += '\r\n'
    request = headers.encode()

    if body:
        request += body.encode()

    client_socket.send(request)

    response = b" "
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        response += data

    print(f"\n{method} {path} Response:\n", response.decode(errors='ignore'))
    client_socket.close()


send_request("GET", "/")