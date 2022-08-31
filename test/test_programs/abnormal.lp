-fly(X) :- animal(X), &c{not ab(X, d1)}. %, &c{-fly(X)}.
fly(X) :- bird(X), &c{not ab(X, d2)}. %, &c{fly(X)}.
-fly(X) :- penguin(X), &c{not ab(X, d3)}. %, &c{-fly(X)}.

% :- animal(X), not fly(X), not -fly(X).
%:- animal(X), not fly(X), &c{fly(X)}.
%:- animal(X), not -fly(X), &c{-fly(X)}.

ab(X, d1) :- bird(X).
ab(X, d2) :- penguin(X).

animal(a). bird(a). penguin(a). fly(a).

animal(b). bird(b).

animal(c).

#show fly/1.
#show ab/2.