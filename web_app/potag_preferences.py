from flask import request, redirect, session, Flask, render_template
import sqlite3

# Fonctions de outils.py
from outils import recup_infos,corrige_espace

# Variables utiles

DATABASE = 'database/potag_main.db'
UPLOAD_FOLDER = 'static/images/'

# Paramètres

def parametres():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session["infos_perso"]
    if info[4]=='':
        info[4]= 'Non renseignée'
    return render_template("parametres.html", compte=info)

def profile_picture():
    active=recup_infos()
    if not active:
        return redirect('/')
    if request.method == "POST":
        file = request.files['file']
        filename=file.filename # On note le nom du fichier envoyé par l'utilisateur
        if filename=='': # Si le nom est vide c'est qu'aucun fichier n'a été envoyé
            error="Veuillez sélectionner une image"
            return render_template("profilepicture.html", error=error)
        file.save(UPLOAD_FOLDER+ 'profils/' + 'pp' + session["name"] + '.png') # On enregistre le fichier en le renommant
        db = sqlite3.connect(DATABASE)
        cursor= db.cursor()
        chemin= UPLOAD_FOLDER + 'profils/' + 'pp' +session["name"]+'.png'
        if session["compte"]=='acheteur':
            cursor.execute("UPDATE acheteur SET profile = ? WHERE id_acheteur = ?", (chemin, session["name"]))
        else:
            cursor.execute("UPDATE producteur SET profile = ? WHERE id_producteur = ?", (chemin, session["name"]))
        db.commit() # On insére dans la base de données le chemin du fichier
        db.close()
        return redirect("/profil")
    info=session["infos_perso"]
    return render_template("profilepicture.html",compte=info)
    
def changeadress():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session["infos_perso"]
    if request.method=="POST":
        adresse=corrige_espace(request.form.get("adresse"))
        ville=corrige_espace(request.form.get("ville"))
        if adresse=="" or ville=="":
            error="Veuillez renseigner tous les champs"
            return render_template("changeadress.html", error=error)
        db=sqlite3.connect(DATABASE)
        cursor=db.cursor()
        cursor.execute("UPDATE acheteur SET adresse_acheteur = ? WHERE id_acheteur = ?", (adresse, info[2])) # on ajoute le mdp à la db
        cursor.execute("UPDATE acheteur SET ville_acheteur = ? WHERE id_acheteur = ?", (ville, info[2])) # on ajoute le mdp à la db
        cursor.execute("UPDATE producteur SET adresse_producteur = ? WHERE id_producteur = ?", (adresse, info[2])) # on ajoute le mdp à la db
        cursor.execute("UPDATE producteur SET ville_producteur = ? WHERE id_producteur = ?", (ville, info[2])) # on ajoute le mdp à la db
        db.commit()
        db.close()
        return redirect("/parametres")
    return render_template("changeadress.html", compte=info)

def changepassword():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session["infos_perso"]
    if request.method=="POST":
        un=session["name"]
        password1=corrige_espace(request.form.get("mdp1"))
        password2=corrige_espace(request.form.get("mdp2"))
        if password1!= password2: # les deux mots de passe doivent être identiques
            error="Veuillez entrer le même mot de passe !"
            return render_template("changepassword.html", error=error)
        if len(password1)<8 or not any(map(str.isdigit, password1)) or not any(map(str.islower, password1)) or not any(map(str.isupper, password1)) : # L'utilisateur doit renseigner un mot de passe vérifiant les conditions
            error = 'Votre mot de passe ne rempli pas toutes les conditions !'
            return render_template("changepassword.html", error=error)
        db=sqlite3.connect(DATABASE)
        cursor=db.cursor()
        cursor.execute("UPDATE acheteur SET password = ? WHERE id_acheteur = ?", (password1, un)) # on ajoute le mdp à la db
        cursor.execute("UPDATE producteur SET password = ? WHERE id_producteur = ?", (password1, un)) # on ajoute le mdp à la db
        db.commit()
        db.close()
        session["create"] = None # on indique que l'utilisateur n'est plus en train de créer un compte
        session["statut"]='active' # on indique que l'utilisateur est désormais connecté
        return redirect("/") # on le renvoie vers la page principale
    return render_template("changepassword.html", compte=info)

def deleteaccount():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session["infos_perso"]
    if request.method=="POST":
        attempt=corrige_espace(request.form.get("mdp")) # On demande le mdp pour sécuriser la suppression du compte
        db=sqlite3.connect(DATABASE)
        cursor=db.cursor()
        if session["compte"]=="acheteur":
                query="SELECT password FROM acheteur WHERE id_acheteur = ?"
        else:
                query="SELECT password FROM producteur WHERE id_producteur = ?"
        value = (session["name"], )
        cursor.execute(query, value)
        password=cursor.fetchall() # on récupère dans la db le mdp lié au nom d'utilisateur
        if password[0][0]!=attempt: # si le mot de passe enregistré dans la db est différent de la tentative
            error="Mot de passe incorrect"
            return render_template("deleteaccount.html", error=error, compte=info)
        else:
            if session["compte"]=="acheteur":
                cursor.execute("DELETE FROM acheteur WHERE id_acheteur= ?", value)
            else:
                cursor.execute("DELETE FROM producteur WHERE id_producteur= ?", value)
        cursor.execute("SELECT id_post FROM social WHERE id_auteur = ?", value)
        liste_posts=cursor.fetchall()
        liste_posts=[post[0] for post in liste_posts]
        for post in liste_posts:
            cursor.execute("DELETE FROM like WHERE id_post = ?", (post, ))
        cursor.execute("DELETE FROM like WHERE id_liker = ?", value)
        cursor.execute("DELETE FROM social WHERE id_auteur = ?", value)
        cursor.execute("DELETE FROM follow WHERE follower = ?", value)
        cursor.execute("DELETE FROM follow WHERE followed = ?", value)
        cursor.execute("DELETE FROM transactions WHERE id_producteur = ?", value)
        cursor.execute("DELETE FROM file_attente WHERE acheteur = ?", value)
        cursor.execute("DELETE FROM file_attente WHERE vendeur = ?", value)
        db.commit() # On supprime la ligne correspondante
        db.close()
        return redirect("/login")
    return render_template("deleteaccount.html", compte=info)