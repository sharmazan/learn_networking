import socket
import threading

HOST = "0.0.0.0"
PORT = 9000

def handle_client(conn, addr):
    print(f"Connected by { addr }")
    buf = b""
    with conn:
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                print(f"Client disconnected: { addr }")
                return
            buf += chunk

            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)  # take one line
                conn.sendall(line + b"\n")       # echo one line back


def main():
    # AF_INET = IPv4, SOCK_STREAM = TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allows quick restart (re-use the port)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Threaded echo server listening on {HOST}:{PORT} ...")

        while True:
            conn, addr = s.accept()  # blocks until a client connects
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    main()

