from flask import session
import sqlite3

DATABASE="database/potag_main.db"

def corrige_espace(mot): # Supprime les espaces avant et après une chaine de carractères
    return str.rstrip(str.lstrip(mot))

def recup_infos(username="un"): # Recupere les infos d'un utilisateur et l'indice d'activité de l'utilisateur connecté

    if not "name" in session:  # L'utilisateur n'est pas connecté
        return False
    
    if username=="un": 
        type_infos = "infos_perso" # On écrit les informations de l'utilisateur actuellement connecté
        username=session["name"]
    else:
        type_infos = "infos_autres" # On écrit les informations d'un autre utilisateur

    db=sqlite3.connect(DATABASE)
    cursor=db.cursor()

    cursor.execute("SELECT id_acheteur FROM acheteur WHERE id_acheteur =?", (username, ))
    if cursor.fetchall() == []:
        type_de_compte = "producteur" 
        cursor.execute("SELECT nom, prenom, id_producteur, profile , adresse_producteur, ville_producteur FROM producteur WHERE id_producteur =?", (username, ))
    else:
        type_de_compte = "acheteur"
        cursor.execute("SELECT nom, prenom, id_acheteur, profile, adresse_acheteur, ville_acheteur FROM acheteur WHERE id_acheteur =?", (username, ))

    infos=cursor.fetchall()
    infos = [x for elem in infos for x in elem] # On obtient [nom,prenom,id,photodeprofile,adresse,ville]
    if infos[3]==None:
        infos[3]="/static/images/profils/default_profil_img.jpg"
    if infos[4]==None:
        infos[4]=''
    if infos[5]==None:
        infos[5]=''
    cursor.execute("SELECT COUNT (*) FROM social WHERE id_auteur = ?", (username, ))  # On ajoute le nombre de publications
    infos.append(cursor.fetchall()[0][0])
    cursor.execute("SELECT Count(followed) from follow where followed =?",(username,)) # Le nombre de followers
    infos.append(cursor.fetchall()[0][0])
    cursor.execute("SELECT Count(follower) from follow where follower =?",(username,)) # Le nombre de suivis
    infos.append(cursor.fetchall()[0][0])
    session[type_infos]=infos #on ajoute la liste dans la session adapté (info_perso ou infos_autres)
    db.close()
    return True # L'utilisateur est connecté et les informations ont été recupérées