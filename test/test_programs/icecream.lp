child(tommy).
ache(tommy).
% ache(tommy) | -ache(tommy).
teething(tommy).

%child(amy).

% the negation as failure in this program is used as a denial of a default rule
like(X) :- child(X), &c{like(X)}.
-like(X) :- ache(X), not teething(X), &c{-like(X)}.
:- not like(X), not -like(X), child(X).
