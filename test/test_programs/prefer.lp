action(1..3).
1{occur(X):action(X)}1.
safe :- occur(1).
comfort :- occur(2).

% question: how to represent "if and only if?"
-ideal :- not safe.
-ideal :- not comfort.

:- not &c{ideal}, not safe.

#show occur/1.