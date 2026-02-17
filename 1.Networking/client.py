import os
import socket

HOST = os.getenv("ECHO_HOST", "127.0.0.1")
PORT = int(os.getenv("ECHO_PORT", 9000))

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected. Type messages. Type 'quit' type exit.")

        while True:
            message = input("> ")
            if message.lower() == "quit":
                break

            s.sendall((message + "\n").encode("utf-8"))
            data = s.recv(1024)

            print("Received: ", data.decode("utf-8").strip())

if __name__ == "__main__":
    main()

