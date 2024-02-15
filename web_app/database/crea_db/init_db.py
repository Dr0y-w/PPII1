import sqlite3

con = sqlite3.connect("../potag_main.db")
cur = con.cursor()

cur.execute("CREATE TABLE producteur ( \
    id_producteur VARCHAR(100) PRIMARY KEY, \
    nom VARCHAR(40), \
    prenom VARCHAR(40), \
    mail VARCHAR(100), \
    password VARCHAR(100), \
    profile VARCHAR(100), \
    adresse_producteur VARCHAR(40), \
    ville_producteur VARCHAR(40), \
    casier INT );")

cur.execute("CREATE TABLE acheteur ( \
    id_acheteur VARCHAR(100) PRIMARY KEY, \
    nom VARCHAR(40), \
    prenom VARCHAR(40), \
    mail VARCHAR(100), \
    password VARCHAR(100), \
    profile VARCHAR(100), \
    adresse_acheteur VARCHAR(40), \
    ville_acheteur VARCHAR(40), \
    casier INT );")

cur.execute("CREATE TABLE transactions ( \
    id_transaction INTEGER PRIMARY KEY AUTOINCREMENT, \
    id_producteur VARCHAR(20) REFERENCES Producteur(id_producteur), \
    lien_image VARCHAR(100), \
    date_offre DATE, \
    prix_produit FLOAT(7), \
    description VARCHAR(200), \
    vendu VARCHAR(100) );")

cur.execute("CREATE TABLE casiers ( \
    id_casier INTEGER PRIMARY KEY, \
    adresse_casier VARCHAR(40), \
    ville_casier VARCHAR(20), \
    no_casier INT, \
    utilise INT);")

cur.execute("CREATE TABLE social ( \
    id_post INTEGER PRIMARY KEY AUTOINCREMENT, \
    id_auteur VARCHAR(20), \
    date_post DATE, \
    heure_post TIME, \
    contenu_post VARCHAR(300), \
    lien_image VARCHAR(40) );")

cur.execute("CREATE TABLE follow ( \
    follower VARCHAR(100), \
    followed VARCHAR(100));")

cur.execute("CREATE TABLE like ( \
    id_post INTEGER, \
    id_liker VARCHAR(100) );")

cur.execute("CREATE TABLE file_attente ( \
    acheteur VARCHAR(100),\
    vendeur VARCHAR(100) );")

con.commit()
con.close()