from math import sqrt
import random
import time
from algo import *
import matplotlib.pyplot as plt


#module contenant les fonctions utiles pour les différents tests

def norme(couple):
    return sqrt(couple[0]**2+couple[1]**2)
def tri(liste):
    return sorted(liste,key=norme)

def gen_liste_aleat(n,x):
    #liste (taille n) de couple de réel aléatoire entre 0 et x m
    liste = [[random.uniform(0,x),random.uniform(0,x)] for i in range(n)]
    return liste 


# ------------------------- test tri fusion : code pour les différents graph -------------------------
"""
les différents code pour récupérer le temps d'exécution de chaque test (mesurer avec time.process_time)
"""

"""
#affichage du temps d'exec
plt.plot([i for i in range(1,800)],temps_exec,".",markersize=3)
plt.grid()
plt.xlabel("taille de la liste")
plt.ylabel("temps en s")
plt.title("Temps d'exécution dans le cas réel")
plt.savefig("../resultats_algo/cas_reel.png", dpi=600)
plt.close('all')



# test de l'algo sur des tailles plus importante

plt.plot([i*10 for i in range(2000)],temps_exec_2,".",markersize=3)
plt.grid()
plt.xlabel("taille de la liste")
plt.ylabel("temps en s")
plt.title("temps d'exécution dans le cas général")
plt.savefig("../resultats_algo/cas_general.png", dpi=600)
plt.close('all')

#------------------------- fin de test tri fusion -------------------------



#------------------------- test algo casier-------------------------
"""
#addaptation de l'algo pour comparé les distances traite_file
def traite_file_test_distance(file,dispo,liste_casiers):
    #dispo=get_dispo() #en param
    distance_par_couple = []
    #liste_casiers = get_casier() #en param
    distance_min=0
    for couple in file:
        liste_distance=[]
        for i in range(len(liste_casiers)):
            casier = liste_casiers[i]
            prem = get_distance(couple[0],casier)
            deux = get_distance(couple[1],casier)
            liste_distance.append([prem,deux,i])
        liste_distance = trie_fusion_liste_distance(liste_distance)
        distance_min+=liste_distance[0][0]+liste_distance[0][1] #somme des plus petite distances parcouru
        distance_par_couple.append(liste_distance)
    casiers=backtrack_meilleur(distance_par_couple,dispo)
    distance_final = 0
    for i in range(len(casiers)):
        for e in distance_par_couple[i]:#liste des distances pour le couple e
            if e[2]==casiers[i]:
                distance_final+= e[0]+e[1]#distance choisi par l'algo de backtracking
    return distance_min,distance_final

def gen_coordoné_test(n):
    #coordonné du centre
    lat = 48.692054
    lon = 6.184417
    perimetre = 0.05 #distance des utilisateurs au point gps lat,lon
    points_gps=[]#liste de point gps
    k=0
    while k<n:
        a = [lat+perimetre*(2*(random.random()-1)),lon+perimetre*(2*(random.random()-1))]#un point gps à tester
    
        key = "AIzaSyDqX66wgJN8ChCV2XZiWWKz0Uxo7SxgYMc"#clé de l'api
        direct = d.Directions(api_key=key)#connexion au service d'itinéraire

        origin = a #l'adresse de départ
        destination = "Nancy" #Un point qui existe
        #test si l'adresse existe
        try :
            data = direct.directions(origin,destination) #itinéraire entre origin et destination
            k+=1
            exist=True
        except :
            exist=False
        if exist:
            points_gps.append(a)

    #écriture dans le fichier coord_gps_nancy.txt
    string = ""
    for e in points_gps:
        string+=str(e[0])+","+str(e[1])+";"

    with open("coord_gps_nancy.txt","w") as f:
        f.write(string[:-1])

def get_coord_gps():
    #return une liste de points gps valide ()
    with open("coord_gps_nancy.txt","r") as f:
        data = f.readlines()


    data = data[0].split(";")
    for i in range(len(data)):
        data[i]=data[i].split(",")
        for k in range(2):

            data[i][k]=float(data[i][k])
    return data