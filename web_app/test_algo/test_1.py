from test_algo import *
"""
test de tri fusion dans le cas réel

"""
t = [None for x in range(800)]
temps_exec = [None for x in range(800)]
correction = True

for i in range(0,800):
    # génération de la liste aléatoire de taille i, de réel entre 0 et 10k
    t[i] = gen_liste_aleat(i,10000)

    # teste de correction
    temp_correction =(tri(t[i])==trie_fusion_liste_distance(t[i]))
    if temp_correction==False:
        correction = False

#correction de l'algo
def test_cas_reel():
    assert correction