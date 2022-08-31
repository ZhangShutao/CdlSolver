child(tommy).
ache(tommy).
teething(tommy).
like(X) :- child(X), &c{like(X)}.
-like(X) :- ache(X), not teething(X), &c{-like(X)}.
