% representing the preference relation between cr-rules, failed

:- not a, not b.
a :- apply(r1).
b :- apply(r2).
:- a, b.
:- napply(p1), apply(r1).
:- napply(p1), apply(r2).
apply(r1) :- not &c{napply(p1)}, &c{apply(r1)}.
apply(r2) :- not &c{napply(p1)}, not &c{apply(r1)}, &c{apply(r2)}.