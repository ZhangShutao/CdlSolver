time(0..3).
occur(on(1), 0).
occur(on(2), 2).

:- occur(X1, T), occur(X2, T), time(T), X1 != X2.
occur(X, T+1) :- time(T), time(T+1), occur(X, T), &c{occur(X, T+1)}.