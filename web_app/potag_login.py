from flask import request, redirect, session, Flask, render_template
import sqlite3
import re

# Fonctions de outils.py
from outils import corrige_espace

# Variables utiles

DATABASE = 'database/potag_main.db'
UPLOAD_FOLDER = 'static/images/'

def signup():
    if request.method=="POST":
        fn=corrige_espace(request.form.get("fn"))
        ln=corrige_espace(request.form.get("ln"))
        un=corrige_espace(request.form.get("un"))
        mail=corrige_espace(request.form.get("mail"))
        compte=request.form.get("compte")
        if fn=="" or ln=="" or un=="" or mail=="" or compte=="": # empty fields
            error="Vous devez remplir tous les champs !"
            return render_template("signup.html", error=error)
        if re.match(r"(.)+@(.)+.(.)+",mail)==None or mail!= mail.replace(" ",""): # on matche les adresses mail valides
            error="Vous devez entrer une adresse mail valide !"
            return render_template("signup.html", error=error)
        if un != un.replace(" ",""): # on vérifie que le nom d'utilisateur ne contient pas d'espace
            error="Votre nom d'utilisateur ne peut pas contenir d'espace !"
            return render_template("signup.html", error=error)
        db=sqlite3.connect(DATABASE)
        cursor=db.cursor()
        if compte=="acheteur": # On ajoute les données dans la table correspondante
            cursor.execute("SELECT id_acheteur FROM acheteur WHERE id_acheteur =?", (un, ))
            id=cursor.fetchall()
            if id!=[]: # on vérifie si le nom d'utilisateur est déja pris
                db.close()
                error="Ce nom d'utilisateur est déja pris ! Veuillez en choisir un autre."
                return render_template("signup.html", error=error)
            cursor.execute("INSERT INTO acheteur (id_acheteur,nom,prenom,mail) VALUES (?,?,?,?)",(un,ln,fn,mail)) # on ajoute les infos dans la bd
            db.commit()
            db.close()
        if compte=="producteur": # On ajoute les données dans la table correspondante
            cursor.execute("SELECT id_producteur FROM producteur WHERE id_producteur =?", (un, ))
            id=cursor.fetchall()
            if id!=[]: # on vérifie si le nom d'utilisateur est déja pris
                db.close()
                error="Ce nom d'utilisateur est déja pris ! Veuillez en choisir un autre."
                return render_template("signup.html", error=error)
            cursor.execute("INSERT INTO producteur (id_producteur,nom,prenom,mail) VALUES (?,?,?,?)",(un,ln,fn,mail)) # on ajoute les infos dans la bd
            db.commit()
            db.close()
        
        session["name_temp"] = un
        session["compte_temp"] = compte
        return redirect("/passwordchoice") # on renvoie vers la page de choix de mdp

    return render_template("signup.html")

# Choix du mot de passe après l'inscription 

def passwordchoice():
    if not "name_temp" in session : # page accessible seulement si un utilisateur est en train de créer un compte
        return redirect("/")
    if request.method=="POST":
        un=session["name_temp"]
        password1=corrige_espace(request.form.get("mdp1"))
        password2=corrige_espace(request.form.get("mdp2"))
        if password1!= password2: # les deux mots de passe doivent être identiques
            error="Veuillez entrer le même mot de passe !"
            return render_template("passwordchoice.html", error=error)
        if len(password1)<8 or not any(map(str.isdigit, password1)) or not any(map(str.islower, password1)) or not any(map(str.isupper, password1)) : # L'utilisateur doit renseigner un mot de passe vérifiant les conditions
            error = 'Votre mot de passe ne rempli pas toutes les conditions !'
            return render_template("passwordchoice.html", error=error)
        db=sqlite3.connect(DATABASE)
        cursor=db.cursor()
        cursor.execute("UPDATE acheteur SET password = ? WHERE id_acheteur = ?", (password1, un)) # on ajoute le mdp à la db
        cursor.execute("UPDATE producteur SET password = ? WHERE id_producteur = ?", (password1, un)) # on ajoute le mdp à la db
        db.commit()
        db.close()
        session["compte"] = session["compte_temp"]
        session["compte_temp"] = None
        session["name"]=un # on indique que l'utilisateur est désormais connecté
        session["name_temp"] = None # on indique que l'utilisateur n'est plus en train de créer un compte
        return redirect("/") # on le renvoie vers la page principale

    return render_template("passwordchoice.html")

# Connexion (login)

def login():
# if form is submited
    session.clear()
    if request.method == "POST":
        session["name_temp"] = corrige_espace(request.form.get("name")) # on ouvre une session au nom du login entré
        db=sqlite3.connect(DATABASE)
        cursor=db.cursor()
        cursor.execute("SELECT id_acheteur FROM acheteur WHERE id_acheteur= ?", (session["name_temp"], ))
        login=cursor.fetchall()
        if login==[]:
            cursor.execute("SELECT id_producteur FROM producteur WHERE id_producteur= ?", (session["name_temp"], ))
            session["compte"]="producteur"
        else:
            session["compte"]="acheteur"
        db.close()
        # redirect to the password page
        return redirect("/password") # on renvoie vers la page de mot de passe même si le nom d'utilisateur n'existe pas pour éviter le brute force
    return render_template("login.html")

# Mot de passe (Login password)

def password():
    if not "name_temp" in session:
        return redirect('/')
    if request.method == "POST":
        attempt=corrige_espace(request.form.get("password")) # on récupère le mdp utilisé pour se connecter (pas forcément le bon)
        db = sqlite3.connect(DATABASE)
        cursor= db.cursor()
        if session["compte"]=="acheteur":
            query="SELECT password FROM acheteur WHERE id_acheteur = ?"
        else:
            query="SELECT password FROM producteur WHERE id_producteur = ?"
        value = (session["name_temp"], )
        cursor.execute(query, value)
        password=cursor.fetchall() # on récupère dans la db le mdp lié au nom d'utilisateur
        db.close()
        if password==[]: # il s'agit du cas où le nom d'utilisateur n'existe pas
            error="Mot de passe incorrect"
            return render_template("password.html", error=error)
        if password[0][0]!=attempt: # si le mot de passe enregistré dans la db est différent de la tentative
            error="Mot de passe incorrect"
            return render_template("password.html", error=error)
        session["name"]=session["name_temp"] # on active la session de l'utilisateur
        session.pop('name_temp', None)
        return redirect("/profil") # on le redirige vers la page principale

    return render_template("password.html")
def forgot():
    return render_template("forgot.html")
# Deconnexion (logout)

def logout():
    session.clear()
    return redirect("/login") # on le redirige vers la page principale