import json
from dataclasses import dataclass
from typing import Optional
from typing import Union


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


@dataclass
class LambdaCalculusExpression:
    type: str
    expression: str
    left_hand_side: Union[str, None] = None
    right_hand_side: Union[str, None] = None


def lambda_expression_helper(expression: str) -> LambdaCalculusExpression:
    """ Finding middle point of LHS and RHS for Problem 3 """

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
