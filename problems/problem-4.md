# Problem 4

Implement a "reduction counter" for the `evaluate` request.
The value of this counter will be returned in the integer field `reductions` as part of the response.
It only counts the number of reductions for that particular expression.

This reduction counter is incremented every time an expression is substituted into the body of an abstraction.
In other words, it is incremented in step 3.2 of "Evaluation of Abstraction revisited" (Problem 3), right after
`exp = {arg => right}[body]` but before `evaluate(exp)`.

Some examples:

* Evaluating `!x.x = !x.x` costs 0 reduction.
* Evaluating `(!x.x y) = y` costs 1 reduction.
* Evaluating `(!x.!y.x y) = !z.y` costs 1 reduction.

If the answer is correct, you will receive a link to the next question.