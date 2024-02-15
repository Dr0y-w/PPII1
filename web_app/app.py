from flask import request, redirect, session, Flask, render_template

# Fonctions de outils.py

from outils import recup_infos

# Configuration flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CeciEstUneCléSecrète'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = 'static/images/'

## Base

@app.route("/", methods=["POST", "GET"])
def index():
    active=recup_infos()
    if not active:
        return redirect('/login')
    return redirect("/profil")

# Social

import potag_social

app.add_url_rule('/publications', view_func=potag_social.publications,methods=["POST", "GET"])
app.add_url_rule('/addpublication', view_func=potag_social.addpublication,methods=["POST", "GET"])
app.add_url_rule('/profil', view_func=potag_social.profil,methods=["POST", "GET"])
app.add_url_rule('/deletepost', view_func=potag_social.deletepost,methods=["POST", "GET"])
app.add_url_rule('/visitprofile<username>', view_func=potag_social.visitprofile,methods=["POST", "GET"])
app.add_url_rule('/profilsfollowed', view_func=potag_social.profilsfollowed,methods=["POST", "GET"])
app.add_url_rule('/followers', view_func=potag_social.followers,methods=["POST", "GET"])
app.add_url_rule('/search', view_func=potag_social.recherche,methods=["POST", "GET"])
app.add_url_rule('/publicationliked', view_func=potag_social.publicationliked,methods=["POST", "GET"])

# Vente

import potag_vente

app.add_url_rule('/ventes', view_func=potag_vente.ventes,methods=["POST", "GET"])
app.add_url_rule('/addventes', view_func=potag_vente.addventes,methods=["POST", "GET"])
app.add_url_rule('/lockers', view_func=potag_vente.lockers,methods=["POST", "GET"])
app.add_url_rule('/achats',view_func=potag_vente.achats,methods=["POST", "GET"])

# Login et Inscriptions

import potag_login

app.add_url_rule('/signup', view_func=potag_login.signup,methods=["POST", "GET"])
app.add_url_rule('/passwordchoice', view_func=potag_login.passwordchoice,methods=["POST", "GET"])
app.add_url_rule('/login', view_func=potag_login.login,methods=["POST", "GET"])
app.add_url_rule('/password', view_func=potag_login.password,methods=["POST", "GET"])
app.add_url_rule('/logout', view_func=potag_login.logout,methods=["POST", "GET"])
app.add_url_rule('/forgot', view_func=potag_login.forgot,methods=["POST", "GET"])


# Preferences

import potag_preferences

app.add_url_rule('/parametres', view_func=potag_preferences.parametres,methods=["POST", "GET"])
app.add_url_rule('/profilepicture', view_func=potag_preferences.profile_picture,methods=["POST", "GET"])
app.add_url_rule('/changeadress', view_func=potag_preferences.changeadress,methods=["POST", "GET"])
app.add_url_rule('/changepassword', view_func=potag_preferences.changepassword,methods=["POST", "GET"])
app.add_url_rule('/deleteaccount', view_func=potag_preferences.deleteaccount,methods=["POST", "GET"])

# Main 

if __name__ == "__main__":
    app.run(debug=True)