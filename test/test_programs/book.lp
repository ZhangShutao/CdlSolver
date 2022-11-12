may_book(R) :- pullman(R), not reserved(R).
may_book(R) :- seat(R), not reserved(R), not &c{-apply}.

pullman(b11).
seat(a11).

reserved(b11).

1 {book(R):may_book(R)} 1.

#show book/1.
