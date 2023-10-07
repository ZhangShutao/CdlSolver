% This program is an example of how to implement DI-semantics in cdlp.

a | b.
a :- not &c{not a}, b.
b :- not &c{not b}, a.
a :- b.
:- not b.