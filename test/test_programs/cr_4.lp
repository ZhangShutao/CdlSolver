% representing the preference relation between cr-rules, failed

:- a, b.
:- not a, not b.
a :- apply(r1).
b :- apply(r2).

apply(r1) :- not &c{-apply(r1)}.
apply(r2) :- not &c{-apply(r2)}, not apply(r1).