from problem3 import lambda_expression_helper, LambdaCalculusExpression


def do_substitution(left_expression: str, right_expression: str) -> LambdaCalculusExpression:
    left_expression = lambda_expression_helper(left_expression)
    right_expression = lambda_expression_helper(right_expression)

    if left_expression.type == 'Variable':
        return LambdaCalculusExpression(
            expression=f'({left_expression.expression} {right_expression.expression})',
            type='Application')


def main():
    expr_list = [
        # 'x',
        # '!a.a',
        # '!x.!y.y'
        # '(e i)',
        '(!b.b i)',
        # '((!z.z b) !x.(b c))',
        # '(!z.!y.(y z) (v f))',
        # '(!j.!v.(v j) (v f))',
        # '(!x.(x !x.x) y)',
    ]

    for exp in expr_list:
        print('================')
        expression = lambda_expression_helper(exp)
        print(vars(expression))
        print(exp == expression.expression)
        if expression.type == 'Application':
            substitute = do_substitution(
                left_expression=expression.left_hand_side,
                right_expression=expression.right_hand_side)
            print('Substitute:', substitute)


if __name__ == "__main__":
    main()
