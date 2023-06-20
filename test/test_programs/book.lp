book(R) :- pullman(R), not reserved(R), not book(R1), R != R1, ticket(R1).
book(R) :- seat(R), not reserved(R), not book(R1), R != R1, ticket(R1), not &c{-book(R)}.
ticket(R) :- pullman(R).
ticket(R) :- seat(R).

pullman(b11).
seat(a11).
seat(a12).

reserved(b11).

goal :- 1{book(R)}1.
:- not goal.

#show book/1.
