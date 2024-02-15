import sqlite3
import gmaps.directions as d
from math import sqrt

## Partie Algo Remplissage de Casier 

def get_distance(a,b):
    """ Recupère la distance entre un point a et b avec l'api de google maps
    
    Parameters
        ----------
        a: string
            L'adresse du point a
        b: string
            L'adresse du point b
    Returns
        -------
        int:
            la distance en m entre les deux points
    """
    key = "AIzaSyDqX66wgJN8ChCV2XZiWWKz0Uxo7SxgYMc"#clé de l'api
    direct = d.Directions(api_key=key)#connexion au service d'itinéraire

    origin = a #l'adresse de départ
    destination = b #l'adresse d'arrivé

    data = direct.directions(origin,destination) #itinéraire entre origin et destination
    
    distance_en_m = data[0]["legs"][0]["distance"]["value"]#1600 par exemple
    
    return distance_en_m

def get_casier():
    """ Interroge la base de donnée pour récupérer les adresses des casiers
    Returns
        -------
        list:
            La liste des adresses de chacun des casiers
    """

    DATABASE = "database/potag_main.db"
    db=sqlite3.connect(DATABASE)
    cursor=db.cursor()
    cursor.execute('Select distinct adresse_casier from casiers')
    adresses_brute = cursor.fetchall()
    adresses = [adresses_brute[i][0] for i in range(len(adresses_brute))]
    return adresses

def get_dispo():
    """ Interroge la base de donnée pour récupérer les disponibilités pour les 18 casiers
    Returns
        -------
        list:
            La liste des disponibilités pour les 18 casiers

            Exemple : [1, 17, 7, 35, 11, 14, 31, 23, 11, 28, 24, 26, 23, 10, 3, 21, 26, 6]
    """
    adresses = get_casier()
    DATABASE = "database/potag_main.db"
    db=sqlite3.connect(DATABASE)
    cursor=db.cursor()
    liste_temp=[]
    for adresse in adresses:
        cursor.execute('Select count(adresse_casier) from casiers where adresse_casier=? and utilise=0',[adresse])
        liste_temp.append(cursor.fetchall())
    liste_dispo_adresse = [liste_temp[i][0][0] for i in range(len(liste_temp))]
    return liste_dispo_adresse

def trie_fusion_liste_distance(liste):
    #liste de couple de reel
    def fusion(tableau1,tableau2):
        indice_tableau1 = 0
        indice_tableau2 = 0    
        taille_tableau1 = len(tableau1)
        taille_tableau2 = len(tableau2)
        tableau_fusionne = []
        while indice_tableau1<taille_tableau1 and indice_tableau2<taille_tableau2:
            val1 = sqrt(tableau1[indice_tableau1][0]**2 + tableau1[indice_tableau1][1]**2)
            val2 = sqrt(tableau2[indice_tableau2][0]**2 + tableau2[indice_tableau2][1]**2)
            if val1 < val2:
                tableau_fusionne.append(tableau1[indice_tableau1])
                indice_tableau1 += 1
            else:
                tableau_fusionne.append(tableau2[indice_tableau2])
                indice_tableau2 += 1
        while indice_tableau1<taille_tableau1:
            tableau_fusionne.append(tableau1[indice_tableau1])
            indice_tableau1+=1
        while indice_tableau2<taille_tableau2:
            tableau_fusionne.append(tableau2[indice_tableau2])
            indice_tableau2+=1
        return tableau_fusionne

    def tri_fusion(tableau):
        if  len(tableau) <= 1: 
            return tableau
        pivot = len(tableau)//2
        gauche = tri_fusion(tableau[:pivot])
        droite = tri_fusion(tableau[pivot:])
        return fusion(gauche,droite)
    
    return tri_fusion(liste)
    
def backtrack_meilleur(liste,dispo):
    """ 
    Parameters
    ----------
        liste : list[list[int]]
            La liste qui contient, pour chaque couple de la file d'attente, 
            la liste trié (par trie_fusion) des distances pour l'acheteur et le vendeur à chaque casier.

            Exemple : pour 4 couples et 3 casiers 
                [ [ [1,2,1], [3,1,0], [4,8,2] ], [[2,3,0], [1,4,1], [2,8,2]], [[1,2,1], [3,1,0], [4,8,2] ] ]
            
        dispo : list[int]
            La liste des disponibilités pour les 18 casiers

            Exemple : [1, 17, 7, 35, 11, 14, 31, 23, 11, 28, 24, 26, 23, 10, 3, 21, 26, 6]
        

    Returns
    -------
        list[int]:
            Pour chaque couple la liste des casiers à attribuer
        
        Exemple:
            [1,0,3,2]
    """


    def premier_meme(liste,i):
        """ Permet de déterminer l'indice de la première apparence de liste[i] (autre que lui même) dans une liste
        Parameters
        ----------
            liste: list
            i: int
                L'indice voulu
        Returns
        -------
            Bool,int:
                True et l'indice de la première apparition si il y en a une
                False et 0 sinon
        """

        for j in range(len(liste)):
            if liste[i]==liste[j] and j!=i:
                return True,j
        return False,0

    def rec_aux(liste,dispo,choix,fin):
        dispo_cop = dispo[:]
        for couple in range(len(liste)):
            testeur = premier_meme(liste,couple) #On regarde si il y a un autre couple qui a le même casier
            if dispo_cop[fin[couple]]>0: #Si il reste de la place alors on la place lui est attribué et il garde ce casier
                dispo_cop[fin[couple]]-=1
            elif testeur[0]: #Si il n'y a plus de place, alors c'est le meilleur entre lui et l'autre ayant le meme casier qui garde ce casier 
                ach1 = liste[couple][choix[couple]][0]
                vend1 = liste[couple][choix[couple]][1]
                ach2 = liste[testeur[1]][choix[testeur[1]]][0]
                vend2 = liste[testeur[1]][choix[testeur[1]]][1]
                val1 = sqrt( ach1**2 + vend1**2)
                val2 = sqrt( ach2**2 + vend2**2)
                if val1>val2:
                    choix[couple]+=1
                    fin[couple] = liste[couple][choix[couple]][2]
                else: 
                    choix[testeur[1]]+=1
                    fin[testeur[1]] = liste[testeur[1]][choix[testeur[1]]][2]
                return rec_aux(liste,dispo,choix,fin) 
            else: # sinon c'est qu'il n'y a plus de place et que personne n'a ce casier donc on passe au choix suivant
                choix[couple]+=1
                fin[couple] = liste[couple][choix[couple]][2]
                return rec_aux(liste,dispo,choix,fin)
        return fin #On a finit quand les choix de tous rentre dans la disponibilité des casiers
    
    return rec_aux(liste,dispo,[0 for i in range(len(liste))],[liste[i][0][2] for i in range(len(liste))])
    
def traite_file(file):
    """ Attribue à chaque couple le casier attribué par backtrack_meilleur
    Parameters
        ----------
        file : list[(acheteur,vendeur)]
            La file d'attente contenant les id des acheteurs et vendeur

            Exemple : 
                [ (Maxence,Didier),(Thomas,Paul) ]   
    """
    DATABASE="database/potag_main.db"
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    dispo=get_dispo()
    distance_par_couple = []
    liste_casiers = get_casier()
    for couple in file:
        cursor.execute("select adresse_acheteur,ville_acheteur from acheteur where id_acheteur=?;",[couple[0]])
        adresse_acheteur=cursor.fetchall()
        adresse_acheteur=(adresse_acheteur[0][0])+" "+(adresse_acheteur[0][1])
        cursor.execute("select adresse_producteur,ville_producteur from producteur where id_producteur=?;",[couple[1]])
        adresse_vendeur=cursor.fetchall()
        print(adresse_vendeur)
        adresse_vendeur=adresse_vendeur[0][0]+" "+adresse_vendeur[0][1]
        liste_distance=[]
        for i in range(len(liste_casiers)):
            casier = liste_casiers[i]
            prem = get_distance(adresse_acheteur,casier)
            deux = get_distance(adresse_vendeur,casier)
            liste_distance.append([prem,deux,i])
        liste_distance = trie_fusion_liste_distance(liste_distance)
        distance_par_couple.append(liste_distance)
    casiers=backtrack_meilleur(distance_par_couple,dispo)
    DATABASE="database/potag_main.db"
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    for i in range(len(casiers)):
        cursor.execute("select id_casier from casiers where (id_casier between ? and ?) and utilise=0",[casiers[i]*100,casiers[i]*100+22])
        data=cursor.fetchall()
        data=[casier[0] for casier in data]
        cursor.execute("update acheteur set casier=? where id_acheteur=?",(data[0],file[i][0]))
        db.commit()
        cursor.execute("update producteur set casier=? where id_producteur=?",(data[0],file[i][1]))
        db.commit()
        cursor.execute("update casiers set utilise=1 where id_casier=?;",[data[0]])
        db.commit()
    cursor.execute("delete from file_attente;")
    db.commit()
    cursor.execute("vacuum;")
    db.commit()
    db.close()

def ajout_file_attente(a,b):
    DATABASE="database/potag_main.db"
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    cursor.execute("select * from file_attente")
    file = cursor.fetchall()
    print(file)
    if len(file) >= 10:
        traite_file(file)
    cursor.execute("insert into file_attente values (?,?)",(a,b))
    db.commit()
    db.close()

## Fin de Algo Casier