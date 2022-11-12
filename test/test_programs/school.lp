day(d1). day(d2).
schoolday(X) :- &c{schoolday(X)}, day(X).
open_school(X) :- schoolday(X), &c{open_school(X)}.
-snowday(X) :- open_school(X).
snowday(d1).