% specificity principle about abnormal situations

-fly(X) :- animal(X), &c{-ab(X, d1)}. %, &c{-fly(X)}.
fly(X) :- bird(X), &c{-ab(X, d2)}. %, &c{fly(X)}.
-fly(X) :- penguin(X), &c{-ab(X, d3)}. %, &c{-fly(X)}.

% :- animal(X), not fly(X), not -fly(X).
%:- animal(X), not fly(X), &c{fly(X)}.
%:- animal(X), not -fly(X), &c{-fly(X)}.

ab(X, d1) :- bird(X).
ab(X, d2) :- penguin(X).

animal(a). bird(a). penguin(a). fly(a).

animal(b). bird(b).

animal(c).

animal(d). bird(d). penguin(d).

#show fly/1.