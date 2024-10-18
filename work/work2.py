from lambda_calculus import Variable, Abstraction, Application
from lambda_calculus.visitors.normalisation import BetaNormalisingVisitor

# (!j.!v.(v j) (v f)) -> (!z.!y.(y z) (v f))

j = Variable('j')
v = Variable('v')
f = Variable('f')

term = Abstraction(j, Abstraction(v, Application(v, j)))
term_rhs = Application(v, f)

print(term)
print(term_rhs)