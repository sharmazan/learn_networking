import socket

HOST = "0.0.0.0"
PORT = 9000

def handle_client(conn, addr):
    print(f"Connected by { addr }")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Client disconnected: { addr }")
                return
            conn.sendall(data)


def main():
    # AF_INET = IPv4, SOCK_STREAM = TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allows quick restart (re-use the port)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((HOST, PORT))
        s.listen()
        print(f"Echo server listening on {HOST}:{PORT} ...")

        while True:
            conn, addr = s.accept()  # blocks until a client connects
            handle_client(conn, addr)

if __name__ == "__main__":
    main()

