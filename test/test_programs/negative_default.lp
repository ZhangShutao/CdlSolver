a | b.
a :- not &c{not a}, b.
b :- not &c{not b}, a.
a :- b.
:- not b.