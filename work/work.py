from problem3 import lambda_expression_helper, LambdaCalculusExpression
import re
import string


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


def main():
    expr_list = [
        # 'x',
        # '!a.a',
        # '!x.!y.y',
        # '(e i)',
        # '(!b.b i)',
        # '((!z.z b) !x.(b c))',
        # '(!x.!y.(y x) (y w))',
        '(!j.!y.(y j) (y p))',  # !z.(z (y p))
        # '(!x.(x !x.x) y)',
    ]

    for exp in expr_list:
        print('================')
        expression = lambda_expression_helper(exp)
        # print(vars(expression))
        # print(exp == expression.expression)
        if expression.type == 'Application':
            substitute = do_substitution(
                left_expression=expression.left_hand_side,
                right_expression=expression.right_hand_side)
            print('Substitute:', substitute)
        else:
            print(expression.expression)


if __name__ == "__main__":
    main()
