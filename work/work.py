from lambda_calculus import Variable, Abstraction, Application
from lambda_calculus.visitors.normalisation import BetaNormalisingVisitor


def main():
    # Randomized problem: (!b.b i) -> i
    # Randomized problem: (λj.λv.(v j) (v f)) -> !z.(z (v f))
    # expression = '(!z.!y.(y z) (v f))'
    expression = '((!z.z b) !x.(b c))'
    # expression = expression.removeprefix('(').removesuffix(')')


if __name__ == "__main__":
    main()
