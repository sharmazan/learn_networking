import socket
import threading

HOST = "0.0.0.0"
PORT = 8000


def recv_until(conn: socket.socket, marker: bytes) -> bytes:
    data = b""
    while marker not in data:
        chunk = conn.recv(1024)
        if not chunk:
            break
        data += chunk
    return data


def parse_headers(header_text: str) -> dict[str, str]:
    headers = {}
    lines = header_text.split("\r\n")
    for line in lines:
        if not line or ":" not in line:
            continue
        k, v = line.split(":", 1)
        headers[k.strip().lower()] = v.strip()
    return headers


def make_response(status: str, body: bytes, content_type: str = "text/plain; cherset=utf-8") -> bytes:
    head = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    ).encode("utf-8")
    return head + body


def handle(conn: socket.socket, addr):
    with conn:
        raw = recv_until(conn, b"\r\n\r\n")
        if not raw:
            return

        header_part, _, rest = raw.partition(b"\r\n\r\n")
        header_text = header_part.decode("iso-8859-1")
        lines = header_text.split("\r\n")
        request_line = lines[0]
        headers = parse_headers("\r\n".join(lines[1:]))

        try:
            method, path, _ = request_line.split(" ", 2)
        except ValueError:
            conn.sendall(make_response("400 Bad Request",  b"Bad request line"))
            return

        # read body if present
        content_length = int(headers.get("content-length", "0"))
        body = rest
        while len(body) < content_length:
            chunk = conn.recv(1024)
            if not chunk:
                break
            body += chunk
        body = body[:content_length]

        # routing
        if method == "GET" and path == "/":
            conn.sendall(make_response("200 OK", b"Hello from toy HTTP server"))
            return

        if method =="GET" and path == "/health":
            conn.sendall(make_response("200 OK", b'{"status":"ok"}\n', "application/json; charset=utf-8"))

        if method == "POST" and path == "/echo":
            conn.sendall(make_response("200 OK", body + b"\n", headers.get("content-type", "text/plain")))
            return

        conn.sendall(make_response("404 Not Found", b"Not found\n"))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Toy HTTP server on http://{HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()





