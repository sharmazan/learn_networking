import socket

HOST = "0.0.0.0"
PORT = 9000

def main():
    # AF_INET = IPv4, SOCK_STREAM = TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allows quick restart (re-use the port)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((HOST, PORT))
        s.listen(1)  # wait for up to 1 queued connection

        print(f"Echo server listening on {HOST}:{PORT} ...")

        conn, addr = s.accept()  # blocks until a client connects
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)  # read up to 1024 bytes
                if not data:
                    print("Client disconnected.")
                    break
                print("Received:", data)
                conn.sendall(data)  # echo back exactly what we got

if __name__ == "__main__":
    main()

