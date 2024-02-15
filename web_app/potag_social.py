from flask import request, redirect, session, Flask, render_template
import sqlite3
from datetime import datetime

# Fonctions de outils.py

from outils import recup_infos

# Variables utiles 

DATABASE = 'database/potag_main.db'
UPLOAD_FOLDER = 'static/images/'

def publications():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session["infos_perso"]
    if request.method=="POST":
        idpost=request.form.get("idpost")
        db = sqlite3.connect(DATABASE)
        cursor= db.cursor()
        cursor.execute("SELECT id_post FROM like WHERE (id_post, id_liker) = (?, ?)", (idpost, session["name"]))
        res=cursor.fetchall()
        if len(res)>0:
            cursor.execute("DELETE FROM like WHERE (id_post, id_liker) = (?, ?)", (idpost, session["name"]))
        else:
            cursor.execute("INSERT INTO like (id_post, id_liker) VALUES (?, ?)", (idpost, session["name"]))
        db.commit()
        db.close()
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    cursor.execute("SELECT id_post, id_auteur, lien_image, contenu_post, date_post, heure_post FROM social ORDER BY date_post")
    posts_temp=cursor.fetchall()
    posts=[]
    for post in posts_temp:
        post = list(post)
        cursor.execute("SELECT count(id_liker) from like where id_post=?;",[post[0]])
        likes = cursor.fetchall()[0][0]
        post.append(likes)
        cursor.execute("SELECT id_post FROM like WHERE (id_post, id_liker) = (?, ?)", (post[0], session["name"]))
        res=cursor.fetchall()
        if len(res)>0:
            post.append("true")
        else:
            post.append("false")
        posts.append(post)
    db.close
    posts.reverse()
    return render_template("publications.html", compte=info, posts=posts)

def publicationliked():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session["infos_perso"]
    if request.method=="POST":
        idpost=request.form.get("idpost")
        db = sqlite3.connect(DATABASE)
        cursor= db.cursor()
        cursor.execute("SELECT id_post FROM like WHERE (id_post, id_liker) = (?, ?)", (idpost, session["name"]))
        res=cursor.fetchall()
        if len(res)>0:
            cursor.execute("DELETE FROM like WHERE (id_post, id_liker) = (?, ?)", (idpost, session["name"]))
        else:
            cursor.execute("INSERT INTO like (id_post, id_liker) VALUES (?, ?)", (idpost, session["name"]))
        db.commit()
        db.close()
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    cursor.execute("SELECT id_post FROM like WHERE id_liker = ?", (session["name"], ))
    liste_posts=cursor.fetchall()
    liste_posts = [x for elem in liste_posts for x in elem]
    print(liste_posts)
    cursor.execute("SELECT id_post, id_auteur, lien_image, contenu_post, date_post, heure_post FROM social WHERE id_post IN (" + ",".join(["?"] * len(liste_posts)) + " ) ORDER BY date_post", (liste_posts))
    posts_temp=cursor.fetchall()
    posts=[]
    for post in posts_temp:
        post = list(post)
        cursor.execute("SELECT count(id_liker) from like where id_post = ?;",[post[0]])
        likes = cursor.fetchall()[0][0]
        post.append(likes)
        cursor.execute("SELECT id_post FROM like WHERE (id_post, id_liker) = (?, ?)", (post[0], session["name"]))
        res=cursor.fetchall()
        if len(res)>0:
            post.append("true")
        else:
            post.append("false")
        posts.append(post)
    db.close
    posts.reverse()
    return render_template("publications.html", compte=info, posts=posts)

def addpublication():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session['infos_perso']
    if request.method=="POST":
        file = request.files['file']
        description=request.form.get("description")
        filename=file.filename # On note le nom du fichier envoyé par l'utilisateur
        if filename=='': # Si le nom est vide c'est qu'aucun fichier n'a été envoyé
            error="Veuillez sélectionner une image"
            return render_template("addpublication.html", error=error)
        db = sqlite3.connect(DATABASE)
        cursor= db.cursor()
        cursor.execute("SELECT COUNT (*) FROM social WHERE id_auteur = ?", (session["name"], ))
        num_posts=cursor.fetchall()[0][0]+1
        chemin= UPLOAD_FOLDER + 'publications/' + session["name"]+ str(num_posts) + '.png'
        file.save(chemin) # On enregistre le fichier en le renommant
        time=str(datetime.now())
        date = time.split()[0]
        heure= time.split()[1][:5]
        cursor.execute("INSERT INTO social  (id_auteur, contenu_post, lien_image, date_post, heure_post) VALUES (?, ?, ?, ?, ?)", (session["name"], description, chemin, date, heure))
        db.commit() # On insére dans la base de données le chemin du fichier
        db.close()
        return redirect("/publications")
    return render_template("addpublication.html", compte=info)

def profil():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session["infos_perso"]
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    cursor.execute("SELECT id_auteur, lien_image, contenu_post, date_post, heure_post, id_post FROM social WHERE id_auteur = ? ORDER BY date_post", (session["name"], ))
    posts=cursor.fetchall()
    db.close()
    posts.reverse()
    if request.method=="POST":
        return redirect("/addpublication")
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    cursor.execute("SELECT id_post FROM like WHERE id_liker = ?", (session["name"], ))
    nb_posts_like=len(cursor.fetchall())
    db.close()
    return render_template("profil.html", compte=info, posts=posts, nb_posts_like=nb_posts_like, )

def deletepost():
    active=recup_infos()
    if not active:
        return redirect('/')
    if request.method=="POST":
        id_post=request.form.get('idpost')
        db = sqlite3.connect(DATABASE)
        cursor= db.cursor()
        cursor.execute("DELETE FROM social WHERE id_post = ?", (id_post, ))
        cursor.execute("DELETE FROM like WHERE id_post = ?", (id_post, ))
        db.commit()
        db.close()
    return redirect('/profil')


def visitprofile(username):
    autres = recup_infos(username)
    data=session["infos_autres"]
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session["infos_perso"]
    if username==session['name']:
        return redirect("/profil")
    if request.method=="POST":
        db = sqlite3.connect(DATABASE)
        cursor= db.cursor()
        cursor.execute("SELECT follower FROM follow WHERE (follower, followed) = (?, ?)", (session["name"], username))
        if len(cursor.fetchall())<1:
            cursor.execute("INSERT INTO follow (follower, followed) VALUES (?, ?)", (session["name"], username))
        else:
            cursor.execute("DELETE FROM follow WHERE (follower, followed) = (?, ?)", (session["name"], username))
        db.commit()
        db.close()
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    cursor.execute("SELECT follower FROM follow WHERE (follower, followed) = (?, ?)", (session["name"], username))
    if len(cursor.fetchall())==1:
        button_value="Ne plus suivre ce profil"
    else: 
        button_value="Suivre ce profil"
    cursor.execute("SELECT id_auteur, lien_image, contenu_post, date_post, heure_post FROM social WHERE id_auteur = ? ORDER BY date_post", (username, ))
    posts=cursor.fetchall()
    cursor.execute("SELECT id_post FROM like WHERE id_liker = ?", (username, ))
    nb_posts_like=len(cursor.fetchall())
    db.close()
    posts.reverse()
    return render_template("visitprofile.html", compte=info, compte_visite=data, posts=posts, button_value=button_value, nb_posts_like=nb_posts_like)

def profilsfollowed():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session['infos_perso']
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    cursor.execute("SELECT followed FROM follow WHERE follower = ?", (session["name"], ))
    comptes_followed_temp=cursor.fetchall()
    comptes_followed=[]
    for user in comptes_followed_temp:
        donnees_users=[]
        donnees_users.append(user[0])
        cursor.execute("SELECT profile FROM acheteur WHERE id_acheteur = ?", (user[0], ))
        photo=cursor.fetchall()
        print(photo)
        if len(photo)>=1:
            if photo[0][0]==None:
                donnees_users.append("/static/images/profils/default_profil_img.jpg")
            else:
                donnees_users.append(photo[0][0])
        else:
            cursor.execute("SELECT profile FROM producteur WHERE id_producteur = ?", (user[0], ))
            photo=cursor.fetchall()
            print(photo)
            if photo[0][0]==None:
                donnees_users.append("/static/images/profils/default_profil_img.jpg")
            else:
                donnees_users.append(photo[0][0])
        cursor.execute("SELECT COUNT (*) FROM social WHERE id_auteur = ?", (user[0], ))
        donnees_users.append(cursor.fetchall()[0][0])
        comptes_followed.append(donnees_users)
    return render_template("profilsfollowed.html", compte=info, comptes_followed=comptes_followed)

def followers():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session['infos_perso']
    db = sqlite3.connect(DATABASE)
    cursor= db.cursor()
    cursor.execute("SELECT follower FROM follow WHERE followed = ?", (session["name"], ))
    followers_temp=cursor.fetchall()
    followers=[]
    for user in followers_temp:
        donnees_users=[]
        donnees_users.append(user[0])
        cursor.execute("SELECT profile FROM acheteur WHERE id_acheteur = ?", (user[0], ))
        photo=cursor.fetchall()
        if len(photo)>=1:
            if photo[0][0]==None:
                donnees_users.append("/static/images/profils/default_profil_img.jpg")
            else:
                donnees_users.append(photo[0][0])
        else:
            cursor.execute("SELECT profile FROM producteur WHERE id_producteur = ?", (user[0], ))
            photo=cursor.fetchall()
            if photo[0][0]==None:
                donnees_users.append("/static/images/profils/default_profil_img.jpg")
            else:
                donnees_users.append(photo[0][0])
        cursor.execute("SELECT COUNT (*) FROM social WHERE id_auteur = ?", (user[0], ))
        donnees_users.append(cursor.fetchall()[0][0])
        followers.append(donnees_users)
    return render_template("followers.html", compte=info, followers=followers)

def recherche():
    active=recup_infos()
    if not active:
        return redirect('/')
    info=session["infos_perso"]
    if request.method == "POST":
        username=request.form.get("recherche")
        db = sqlite3.connect(DATABASE)
        cursor= db.cursor()
        cursor.execute("SELECT id_acheteur from acheteur")
        noms=cursor.fetchall()
        cursor.execute("SELECT id_producteur from producteur")
        noms+=cursor.fetchall()
        noms=[x for elem in noms for x in elem]
        if username in noms:
            return redirect("/visitprofile"+username)
        else:
            return redirect("/publications")
    return render_template("publications.html", compte=info)

