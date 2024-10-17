import json
import os
import socket
import socketserver
import sys
from dataclasses import dataclass
from typing import Optional
from typing import Union


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

    expression_obj = lambda_expression_helper(expression)

    if expression_obj.type in ['Variable', 'Abstraction']:
        msg['result']['expression'] = expression
        msg = json.dumps(msg).encode("utf-8") + b'\n'
        return msg

    msg['result']['expression'] = 'rizwan'
    msg = json.dumps(msg).encode("utf-8") + b'\n'
    return msg


def lambda_expression_helper(expression: str):
    """ Finding middle point of LHS and RHS """

    @dataclass
    class LambdaCalculusExpression:
        type: str
        expression: str
        left_hand_side: Union[str, None] = None
        right_hand_side: Union[str, None] = None

    # Checking if the expression is a Variable
    if len(expression) == 1:
        return LambdaCalculusExpression(
            type='Variable',
            expression=expression)

    # Checking if the expression is an Abstraction
    if expression.startswith('!'):
        return LambdaCalculusExpression(
            type='Abstraction',
            expression=expression)

    bracket_stack: list = []
    middle_of_lhs_rhs: int = -1
    probably_middle: bool = False

    for i in range(len(expression)):
        char: str = expression[i]

        if char == '(':
            bracket_stack.append('(')
            continue

        if char == ')':
            bracket_stack.pop()
            if len(bracket_stack) == 1 and bracket_stack[-1] == '(':
                probably_middle = True
            continue

        if probably_middle and char == ' ':
            middle_of_lhs_rhs = i + 1
            break

    if middle_of_lhs_rhs == -1:
        middle_of_lhs_rhs = expression.find(' ')

    LHS: str = expression[:middle_of_lhs_rhs].strip(' ').removeprefix('(')
    RHS: str = expression[middle_of_lhs_rhs:].strip(' ').removesuffix(')')

    return LambdaCalculusExpression(
        left_hand_side=LHS,
        right_hand_side=RHS,
        type='Application',
        expression=f'({LHS} {RHS})')


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
