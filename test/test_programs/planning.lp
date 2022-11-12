#const n=4.
time(0..n).

block(a).
block(b).
block(c).
block(d).

location(X) :- block(X).
location(t).

action(move(B, L)) :- block(B), location(L).

-holds(on(B, L2), T) :- block(B), time(T), location(L1), location(L2), L1 != L2, holds(on(B, L1), T).
holds(on(B, L), T+1) :- block(B), location(L), time(T), occurs(move(B, L), T).
holds(on(B, L), T+1) :- block(B), location(L), time(T), holds(on(B, L), T), not -holds(on(B, L), T+1).

:- block(B), block(B1), B != B1, location(L), time(T), occurs(move(B, L), T), holds(on(B1, B), T).
:- block(B), block(B1), B != B1, location(L), time(T), occurs(move(B, L), T), holds(on(B1, L), T), L != t.
:- block(B), time(T), occurs(move(B, B), T).

holds(on(a,d), 0).
holds(on(b,a), 0).
holds(on(c,t), 0).
holds(on(d,t), 0).

goal(T) :- time(T), holds(on(a,t), T), holds(on(b,a), T), holds(on(c,t), T), holds(on(d,c), T).

goal :- time(T), goal(T).
:- not goal.

1{occurs(A, T) : action(A)}1 :- time(T), T < n, not goal(T).

table_allowed(T) :- time(T), not &c{-table_allowed(T)}.
:- occurs(move(B,t), T), block(B), time(T), not table_allowed(T).

%#show table_allowed/1.
#show goal/1.
#show occurs/2.