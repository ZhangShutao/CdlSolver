#const n=7.
time(0..n).

block(a).
block(b).
block(c).
block(d).

location(X) :- block(X).
location(t).

action(move(B, L)) :- block(B), location(L).

moved(B, T) :- occurs(move(B, L), T).
holds(on(B, L), T+1) :- occurs(move(B, L), T).
holds(on(B, L), T+1) :- holds(on(B, L), T), not moved(B, T), time(T+1).

:- occurs(move(B, L), T), holds(on(B1, B), T).
:- occurs(move(B, L), T), holds(on(B1, L), T), B != B1, L != t.
:- holds(on(B, L), T), occurs(move(B, L), T).

holds(on(a,d), 0).
holds(on(b,a), 0).
holds(on(c,t), 0).
holds(on(d,t), 0).

goal(T) :- time(T), holds(on(a,t), T), holds(on(b,a), T), holds(on(c,t), T), holds(on(d,c), T).

goal :- goal(T), time(T).
:- not goal.

1{occurs(A, T) : action(A)}1 :- time(T), T < n, not goal(T).

table_allowed(T) :- time(T), T < n, not &c{not table_allowed(T)}.
:- occurs(move(B,t), T), block(B), time(T), not table_allowed(T).

#show table_allowed/1.
#show goal/1.
#show occurs/2.