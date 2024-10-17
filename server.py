import os
import sys
import json
import re
from typing import Optional
import socket
import socketserver


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


def response_for_problem_1_and_2(text: str) -> Optional[bytes]:
    """ Handling Message - Problem 1 and 2 """

    if '"message":' not in text:
        return None

    text: dict = json.loads(text)

    msg = {
        'id': text['id'],
        'result': {
            'message': text['params']['message']
        }
    }
    msg = json.dumps(msg).encode("utf-8")
    msg = msg + b'\n'
    return msg


def response_for_problem_3(text: str) -> Optional[bytes]:
    """ Handling Expression - Problem 3 """

    if '"expression":' not in text:
        return None

    text: dict = json.loads(text)
    expression = text['params']['expression']
    msg = {
        'id': text['id'],
        'result': {
            'expression': None
        }
    }

    # Evaluating Variable
    if len(expression) == 1:
        msg['result']['expression'] = expression
        msg = json.dumps(msg).encode("utf-8") + b'\n'
        return msg

    # Evaluating Abstraction
    if expression[0] == '!':
        abstraction_test_passed: bool = True
        tmp_expression: list = expression.split('.')

        for i in tmp_expression:
            if i.find(' ') != -1:
                abstraction_test_passed = False
                break
            if i[-1] == '!':
                abstraction_test_passed = False
                break

        if abstraction_test_passed:
            msg['result']['expression'] = expression
            msg = json.dumps(msg).encode("utf-8") + b'\n'
            return msg

    # Evaluating Application
    if [expression[0], expression[-1]] == ['(', ')']:

        # If left is NOT an Abstraction, return (<left> <right>).
        if expression[1] != '!':
            msg['result']['expression'] = expression
            msg = json.dumps(msg).encode("utf-8") + b'\n'
            return msg

        # Left is an Abstraction


# def response_for_problem_3(text: str) -> Optional[bytes]:
#     """ Handling Expression - Problem 3 """
#
#     if '"expression":' not in text:
#         return None
#
#     text: dict = json.loads(text)
#     expression = text['params']['expression']
#     msg = {
#         'id': text['id'],
#         'result': {
#             'expression': None
#         }
#     }
#
#     # Evaluating Variable
#     if len(expression) == 1:
#         msg['result']['expression'] = expression
#         msg = json.dumps(msg).encode("utf-8") + b'\n'
#         return msg
#
#     # Evaluating Abstraction
#     if expression[0] == '!':
#         abstraction_test_passed: bool = True
#         tmp_expression: list = expression.split('.')
#
#         for i in tmp_expression:
#             if i.find(' ') != -1:
#                 abstraction_test_passed = False
#                 break
#             if i[-1] == '!':
#                 abstraction_test_passed = False
#                 break
#
#         if abstraction_test_passed:
#             msg['result']['expression'] = expression
#             msg = json.dumps(msg).encode("utf-8") + b'\n'
#             return msg
#
#     # Evaluating Application
#     if expression[0] == '(' and expression[-1] == ')':
#         case1 = re.compile(r'^(\(!\w\.\w \w\))')
#         if case1.findall(expression):
#             msg['result']['expression'] = expression[-2]
#             msg = json.dumps(msg).encode("utf-8") + b'\n'
#             return msg
#
#         msg['result']['expression'] = expression
#         msg = json.dumps(msg).encode("utf-8") + b'\n'
#         return msg
#
#     return None


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
    # print(response_for_problem_3('{"id":1,"method":"evaluate","params":{"expression":"!t.t"}}'))
    # print(response_for_problem_3('{"id":3,"method":"evaluate","params":{"expression":"(!y.y m)"}}'))
    # print(response_for_problem_3('{"id":3,"method":"evaluate","params":{"expression":"(z e)"}}'))
    main()
