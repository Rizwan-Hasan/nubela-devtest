import json
import re
import string
from dataclasses import dataclass
from typing import Optional
from typing import Union


@dataclass
class LambdaCalculusExpression:
    type: str
    expression: str
    left_hand_side: Union[str, None] = None
    right_hand_side: Union[str, None] = None


def response_for_problem_3(text: str) -> Optional[bytes]:
    """ Handling Expression - Problem 3 """

    if '"expression":' not in text:
        return None

    text: dict = json.loads(text)
    expression = text['params']['expression']
    msg = {
        'id': text['id'],
        'result': {'expression': ''}
    }
    expression_obj = lambda_expression_helper(expression)

    if expression_obj.type != 'Application':
        msg['result']['expression'] = expression_obj.expression
        msg = json.dumps(msg).encode("utf-8") + b'\n'
        return msg

    # Handling Application
    og_right_used: bool = False
    expr_type: str = expression_obj.type
    list_of_substitution = [lambda_expression_helper(expression_obj.left_hand_side)]
    while expr_type and expr_type == 'Application':
        expression = list_of_substitution.pop()

        if not expression.left_hand_side and not expression.right_hand_side:
            list_of_substitution.clear()
            substitute = do_substitution(
                left_expression=expression_obj.left_hand_side,
                right_expression=expression_obj.right_hand_side)
            msg['result']['expression'] = substitute.expression
            og_right_used = True
            expr_type = ''
            break

        substitute = do_substitution(
            left_expression=expression.left_hand_side,
            right_expression=expression.right_hand_side)

        if substitute.left_hand_side and len(substitute.left_hand_side) > 1:
            list_of_substitution.append(substitute)
        elif og_right_used:
            msg['result']['expression'] = substitute.expression
            break
        else:
            expr_type = 'Application'
            list_of_substitution.append(
                lambda_expression_helper(f'({substitute.expression} {expression_obj.right_hand_side})'))
            og_right_used = True

    msg = json.dumps(msg).encode("utf-8") + b'\n'
    return msg


def get_lowercase_letters(input_string: str) -> set:
    my_set: set = set()
    for char in input_string:
        if char.islower():
            my_set.add(char)
    return my_set


def do_substitution(left_expression: str, right_expression: str) -> LambdaCalculusExpression:
    if lambda_expression_helper(left_expression).type == 'Variable':
        return lambda_expression_helper(f'({left_expression} {right_expression})')

    first_argument: str = re.findall(r'\!\w', left_expression)[0]
    expression = left_expression.replace(first_argument, '', 1).removeprefix('.').removeprefix(' ')

    # Naively replace for unique argument variable
    if expression.find(first_argument) == -1:
        right_expression_placeholder: str = 'R'
        new_expression: str = expression.replace(first_argument.removeprefix('!'), right_expression_placeholder)

        variables_of_new_expression: set = get_lowercase_letters(new_expression)
        variables_of_right_expression: set = get_lowercase_letters(right_expression)
        common_variables: set = variables_of_new_expression.intersection(variables_of_right_expression)
        all_variables: set = get_lowercase_letters(f'{left_expression}{right_expression}')
        unused_alphabets: set = set(string.ascii_lowercase).difference(all_variables)

        for char in common_variables:
            new_expression = new_expression.replace(char, unused_alphabets.pop())

        new_expression = new_expression.replace(right_expression_placeholder, right_expression)
        return lambda_expression_helper(new_expression)


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
