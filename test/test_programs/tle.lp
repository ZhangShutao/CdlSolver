
holds(on(X,L1),T+1) :- holds(on(X,L1),T),&c{-occurs(moveto(X,L2),T+1)},location(L1),location(L2),time(T),time(T+1).
holds(on(X,L2),T+1) :- holds(on(X,L1),T),occurs(moveto(X,L2),T+1),location(L1),location(L2),time(T),time(T+1).
-holds(on(X,L1),T+1) :- holds(on(X,L1),T),occurs(moveto(X,L2),T+1),location(L1),location(L2),time(T),time(T+1).

time(0..3).

location(a1). location(a2). location(a3). location(a4).
location(b1). location(b2). location(b3). location(b4).
location(c1). location(c2). location(c3). location(c4).
location(d1). location(d2). location(d3). location(d4).
location(null).

piece(b_k).
piece(w_k).
piece(w_p_2).
piece(b_n_1).

holds(on(b_k, b1), 0).
holds(on(w_p_2, c2), 0).
holds(on(w_k, d4), 0).
holds(on(b_n_1, c3), 0).

occurs(moveto(b_k, c2), 1).
occurs(moveto(w_k, d3), 2).
occurs(moveto(b_n_1, b2), 3).

holds(on(P1, null), T) :- occurs(moveto(P2, L), T), holds(on(P1, L), T-1),
	piece(P1), piece(P2), P1 != P2,
	time(T), time(T-1), location(L).

#show holds/2.