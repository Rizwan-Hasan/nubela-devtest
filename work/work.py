from lambda_calculus import Variable, Abstraction, Application
from lambda_calculus.visitors.normalisation import BetaNormalisingVisitor
from typing import Union
from dataclasses import dataclass
from enum import Enum


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
    expr_list = [
        # 'x',
        # '!a.a',
        # '!x.!y.y'
        # '(x y)',
        # '(!b.b i)',
        # '((!z.z b) !x.(b c))',
        # '(!z.!y.(y z) (v f))',
        # '(!j.!v.(v j) (v f))',
        '(!x.(x !x.x) y)',
    ]

    for exp in expr_list:
        print('================')
        info = lambda_expression_helper(exp)
        print(vars(info))
        print(exp == info.expression)


if __name__ == "__main__":
    main()
