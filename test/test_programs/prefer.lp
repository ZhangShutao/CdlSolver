action(1..3).
1{occur(X):action(X)}1.
safe :- occur(1).
comfort :- occur(2).

ideal :- safe, comfort.

:- not &c{ideal}, not safe.