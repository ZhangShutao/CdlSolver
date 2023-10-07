book(R) :- business(R), not reserved(R), not book(R1), R != R1, ticket(R1).
book(R) :- economy(R), not reserved(R), not book(R1), R != R1, ticket(R1), not &c{not book(R)}.
ticket(R) :- business(R).
ticket(R) :- economy(R).

business(b11).
economy(a11).
economy(a12).

reserved(b11).

goal :- 1{book(R)}1.
:- not goal.

#show book/1.
#show -book/1.
