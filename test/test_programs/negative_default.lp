% This program is an example of how to implement DI-semantics in cdlp.

a | b.
a :- not &c{- a}, b.
b :- not &c{- b}, a.
a :- b.
:- not b.