fly(X):- bird(X), &c{fly(X)}.
-fly(X) :- penguin(X).

bird(tweety).
penguin(tweety).

#show fly/1.