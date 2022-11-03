import itertools

floors = [0, 1, 2, 3, 4] # 5 verdiepingen

# itertools.permutations() provides us with all the possible arrangements that can be there for an iterator 
# and all elements are assumed to be unique on the basis of their position and not by their value or category
for (L, M, N, E, J) in list(itertools.permutations(floors)):

    # Marja niet op begane grond
    if M == 0:
        continue
    
    # Niels niet boven en op begane grond
    # Niels woont niet 1 hoger of lager dan Marja
    if N == 0 or N == 4 or N == M - 1 or N == M + 1:
        continue

    # Loes niet boven
    if L == 4:
        continue

    # Erik tenminste 1 hoger dan Marja
    if E <= M:
        continue

    # Joep niet 1 hoger of lager dan Niels
    if J == N - 1 or J == N + 1:
        continue

    # Answers
    print("Loes " + str(L), "Marja " + str(M), "Niels " + str(N), "Erik " + str(E), "Joep " + str(J))
