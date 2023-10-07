fly(X) :- bird(X), &c{fly(X)}.
-fly(X) :- penguin(X).
:- fly(X), ostrich(X).
bird(tweety). penguin(tweety).
bird(plucky). ostrich(plucky).
bird(ringo).

#show fly/1.