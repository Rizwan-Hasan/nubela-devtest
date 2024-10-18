import os
import socket
import socketserver
import sys

from problem1and2 import response_for_problem_1_and_2
from problem3 import response_for_problem_3


class ThreadedStreamRequestHandler(socketserver.StreamRequestHandler):

    def handle(self):
        while True:
            # Read message from the client
            data = self.rfile.readline().strip()

            if not data:
                print(f"Client disconnected")
                break

            text: str = data.decode("utf-8")
            print('Received:', text)

            # Handling Message - Problem 1 and 2
            msg = response_for_problem_1_and_2(text)
            if msg is not None:
                self.wfile.write(msg)
                print('Sent:', msg)
                continue

            # Handling Expression - Problem 3
            msg = response_for_problem_3(text)
            if msg is not None:
                self.wfile.write(msg)
                print('Sent:', msg)
                continue


class ThreadedUnixStreamServer(socketserver.ThreadingMixIn,
                               socketserver.UnixStreamServer):
    address_family = socket.AF_UNIX
    socket_type = socket.SOCK_STREAM
    daemon_threads = True

    pass


def main():
    server_address = "./sock"

    if os.path.exists(server_address):
        os.remove(server_address)

    server = ThreadedUnixStreamServer(server_address, ThreadedStreamRequestHandler)  # noqa
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
