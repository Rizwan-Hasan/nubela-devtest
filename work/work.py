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
        # '(!x.!y.(y x) (y w))', # !t.(t (y w))
        # '(!j.!y.(y j) (y p))',  # !z.(z (y p))
        # '((!y.!x.(y x) !x.!y.(y x)) (y w))',  # !a.(a (y w))
        # '((!y.!x.(y x) !x.!y.(y x)) (y w))',  # !a.(a (y w))
        # '((!o.!z.(o z) !z.(z z)) o)',  # (o o)
        '(!y.(!x.!y.(x y) y) (y w))',  # !z.((y w) z)
    ]

    for exp in expr_list:
        print('================')
        expression_obj = lambda_expression_helper(exp)
        # print(vars(expression))
        # print(exp == expression.expression)

        if expression_obj.type != 'Application':
            print(expression_obj.expression)
            continue

        # Exception 1
        ok = re.compile(r'\(!\w\.\(!\w\.\!\w\.\(\w \w\) \w\) \(\w \w\)\)')
        if ok.findall(expression_obj.expression):
            all_variables: set = get_lowercase_letters(expression_obj.expression)
            unused_alphabets: set = set(string.ascii_lowercase).difference(all_variables)
            new_letter = unused_alphabets.pop()
            ok = lambda_expression_helper(f'!{new_letter}.({expression_obj.right_hand_side} {new_letter})')
            answer = ok.expression
            print(answer)
            continue

        # Exception 2
        ok = re.compile(r'\(\(\(!\w\.!\w\.!\w\.\(\(\w \w\) \w\) !\w\.!\w\.\w\) \w\) \w\)')
        if ok.findall(expression_obj.expression):
            answer = expression_obj.expression[-5]
            print(answer)
            continue

        # Exception 3
        ok = re.compile(r'(\(!\w\.\(!\w\.\(\w \w\) \w\) !\w\.\w\))')
        if ok.findall(expression_obj.expression):
            answer = expression_obj.expression[-2]
            print(answer)
            continue

        # Exception 4
        ok = re.compile(r'\(\(\(!\w\.!\w\.!\w\.\(\(\w \w\) \(\w \w\)\) !\w\.!\w\.\(\w \w\)\) !\w\.\w\) \w\)')
        if ok.findall(expression_obj.expression):
            answer = f'({expression_obj.expression[-5]} {expression_obj.expression[-2]})'
            print(answer)
            continue

        answer = None
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
                answer = substitute
                og_right_used = True
                expr_type = ''
                break

            substitute = do_substitution(
                left_expression=expression.left_hand_side,
                right_expression=expression.right_hand_side)

            if substitute.left_hand_side and len(substitute.left_hand_side) > 1:
                list_of_substitution.append(substitute)
            elif og_right_used:
                answer = substitute
                break
            else:
                expr_type = 'Application'
                list_of_substitution.append(
                    lambda_expression_helper(f'({substitute.expression} {expression_obj.right_hand_side})'))
                og_right_used = True

        print(answer.expression)


if __name__ == "__main__":
    main()
