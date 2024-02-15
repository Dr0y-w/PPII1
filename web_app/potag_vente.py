from flask import request, redirect, session, Flask, render_template
import sqlite3
from datetime import datetime
from gmaps import Geocoding
import gmaps.directions as d 
# Fonctions de outils.py
from outils import recup_infos

from algo import ajout_file_attente

# Variable utiles
DATABASE = 'database/potag_main.db'
UPLOAD_FOLDER = 'static/images/'

def ventes():
    active=recup_infos()
    if not active:
        return redirect('/')
    if request.method=="POST" and session["compte"]=="acheteur":
        idpost=request.form.get("idpost")
        db = sqlite3.connect(DATABASE)
        cursor= db.cursor()
        cursor.execute("SELECT adresse_acheteur FROM acheteur WHERE id_acheteur = ?", (session["name"], ))
        res=cursor.fetchall()
        print(res)
        if res==[(None,)]:
            error="Vous devez avoir renseigné une adresse pour acheter un produit !"
            db.close()
            info=session['infos_perso']
            info[4]="Non renseignée"
            return render_template("parametres.html", compte=info, error=error)
        cursor.execute("UPDATE transactions SET vendu=? WHERE id_transaction = ?;", (session["name"],idpost))
        db.commit()
        cursor.execute("select id_producteur from transactions where id_transaction=?;", [idpost])
        producteur = cursor.fetchall()[0][0]
        ajout_file_attente(session["name"],producteur)
        db.close()
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    cursor.execute("SELECT id_transaction, id_producteur, lien_image, description, date_offre, prix_produit FROM transactions where vendu is null")
    posts=cursor.fetchall()
    cursor.execute("select count(*) from file_attente")
    taille_file=cursor.fetchall()[0][0]
    cursor.execute("select casier from acheteur where id_acheteur=?",[session["name"]])
    casier=cursor.fetchall()
    if casier==[]:
        casier="Aucun"
    else:
        casier=casier[0][0]
    cursor.execute("select count(*) from file_attente where acheteur=?",[session["name"]])
    nbr_achats=cursor.fetchall()[0][0]
    res=[]
    
    for post in posts:
        deb=list(post)
        cursor.execute("select vendu from transactions where id_transaction=?",[post[0]])
        vendu=cursor.fetchall()[0][0]
        if vendu==None:
            res.append(deb+["false"])
        else:
            res.append(deb+["true"])
    posts=res[:]
    db.close
    info=session["infos_perso"]
    if request.method=="POST" and session["compte"]=="producteur":
        return redirect("/addventes")
    
    return render_template("ventes.html", compte=info,posts=posts,type=session["compte"],taille_file=taille_file,casier=casier,nbr_achats=nbr_achats)

def achats():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session['infos_perso']
    if request.method=="POST" and session["compte"]=="acheteur":
        idpost=request.form.get("idpost")
        db = sqlite3.connect(DATABASE)
        cursor= db.cursor()
        cursor.execute("UPDATE transactions SET vendu=? WHERE id_transaction = ?;", (None,idpost))
        db.commit()
        cursor.execute("select id_producteur from transactions where id_transaction=?;", [idpost])
        producteur = cursor.fetchall()[0][0]
        cursor.execute("delete from file_attente where acheteur=? and vendeur=?;",[session["name"],producteur])
        db.commit()
        db.close()
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    cursor.execute("SELECT id_transaction,id_producteur,description FROM transactions WHERE vendu = ?", (session["name"], ))
    achats_temp=cursor.fetchall()
    achats=[]
    for achat in achats_temp:
        donnees=list(achat)
        cursor.execute("select profile from producteur where id_producteur=?",[achat[1]])
        photo=cursor.fetchall()
        if photo[0][0]==None:
                donnees.append("/static/images/profils/default_profil_img.jpg")
        else:
                donnees.append(photo[0][0])
        achats.append(donnees)
    return render_template("achat.html",compte=info, achats=achats)

def addventes():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session['infos_perso']
    if request.method=="POST":
        file = request.files['file']
        description=request.form.get("description")
        prix=float(request.form.get("prix"))
        filename=file.filename # On note le nom du fichier envoyé par l'utilisateur
        if filename=='': # Si le nom est vide c'est qu'aucun fichier n'a été envoyé
            error="Veuillez sélectionner une image"
            return render_template("addventes.html", error=error)
        db = sqlite3.connect(DATABASE)
        cursor= db.cursor()
        cursor.execute("SELECT COUNT (*) FROM transactions WHERE id_producteur = ?", (session["name"], ))
        num_posts=cursor.fetchall()[0][0]+1
        chemin= UPLOAD_FOLDER + 'ventes/' + session["name"]+ str(num_posts) + '.png'
        file.save(chemin) # On enregistre le fichier en le renommant
        time=str(datetime.now())
        date = time.split()[0]
        cursor.execute("INSERT INTO transactions  (id_producteur, description, lien_image, date_offre, prix_produit) VALUES (?, ?, ?, ?, ?)", (session["name"], description, chemin, date, prix))
        db.commit() # On insére dans la base de données le chemin du fichier
        db.close()
        return redirect("/ventes")
    return render_template("addventes.html", compte=info)

def lockers():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session["infos_perso"]
    #info sur les lockers à afficher sur la gmap
    db=sqlite3.connect(DATABASE)
    cursor=db.cursor()
    data = cursor.execute("SELECT DISTINCT adresse_casier,ville_casier FROM casiers").fetchall()
    key = "AIzaSyDqX66wgJN8ChCV2XZiWWKz0Uxo7SxgYMc"#api_key google maps api
    api = Geocoding(api_key=key)
    adresses = []
    for e in data:#pour chaque casier
        r = api.geocode(e[0]+","+e[1])[0]["geometry"]["location"]#couple lat et lng pour afficher les markers
        adresses.append(r)
    return render_template("lockers.html",adresses=adresses,compte=info)
