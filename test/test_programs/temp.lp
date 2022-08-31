p(1..2).
a(X) :- p(X), apply(r1,X).
guess_not_apply(r1,X) | not guess_not_apply(r1,X) :- p(X).
 :- guess_not_apply(r1,X), apply(r1,X).
 :- guess_apply(r1,X), guess_not_apply(r1,X).
 :- guess_apply(r1,X), guess_sn_apply(r1,X).
apply(r1,X) :- p(X), not guess_not_apply(r1,X).
ok :- a(X).
 :- not ok.
 :- apply(r1,1), apply(r1,2).
 :- napply(p1), apply(r1,1).
 :- napply(p1), apply(r1,2).
guess_napply(p1) | not guess_napply(p1).
 :- guess_not_napply(p1), napply(p1).
 :- guess_napply(p1), guess_not_napply(p1).
 :- guess_napply(p1), guess_sn_napply(p1).
