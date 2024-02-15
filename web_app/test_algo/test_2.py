from test_algo import *
"""
test de tri fusion dans le cas général
"""

# test de l'algo sur des tailles plus importante
t = [None for x in range(2000)]
temps_exec_2 = [None for x in range(2000)]
correction = True
for i in range(0,2000):
    # génération de la liste aléatoire de taille i, de réel entre 0 et 100k
    t[i] = gen_liste_aleat(i*10,100000)
    temp_correction =(tri(t[i])==trie_fusion_liste_distance(t[i]))
    if temp_correction==False:
        correction = False


def test_cas_general():
    assert correction