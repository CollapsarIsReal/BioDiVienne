from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
# Crédits Roy's tutorial : https://roytuts.com/upload-and-display-image-using-python-flask/
import os
#import flask_login
#from app import app
import urllib.request
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#INITIALISATION DES VARIABLES
app = Flask("Application")
#On configure la base données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BioDivVie2.db'
# On initie l'extension
db = SQLAlchemy(app)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# flask_login
#import flask_login
#login_manager = flask_login.LoginManager()
#login_manager.init_app(app)

# On crée nos différents modèles
class Personne(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text)
    prenom = db.Column(db.Text)
    utilisateurON = db.Column(db.Integer)

class Compte(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    mail = db.Column(db.Text, unique=True, nullable=False)
    pseudo = db.Column(db.Text, unique=True, nullable=False)
    mdp = db.Column(db.Text, nullable=False)
    photos = db.relationship("Photo", back_populates="compte")

class Photo(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    titre = db.Column(db.Text)
    datePrise = db.Column(db.Text)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    compte = db.relationship("Compte", back_populates="photos")
    lien_interne = db.Column(db.Text, unique=True, nullable=False)
    lien_externe = db.Column(db.Text)

class Espece(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    fichier = db.Column(db.Text, unique=True, nullable=False)
    regne = db.Column(db.Text, nullable=False) #peut-être faire du booléen 0=vegetal et 1=animal ?
    nom_vernaculaire = db.Column(db.Text)
    nom_latin = db.Column(db.Text)
    description = db.Column(db.Text)
    preoccupation = db.Column(db.Text) #faire liste selon LRN ou LRR avec lettres déroulantes


@app.route("/espece/<int:id>")
def espece(id):
    unique_espece = Espece.query.get(id)
    return render_template("photo2.html", espece=unique_espece)


@app.route("/")
def accueil_(exemple=None):
    especes = Espece.query.all()
    return render_template("accueil4.html", especes=especes)


@app.route("/accueil")
#fonction de lancement de la page d'accueil
def accueil(exemple=None):
    especes = Espece.query.all()
    return render_template("accueil4.html", especes=especes)


@app.route("/recherche")
def recherche():
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    motclef = request.args.get("keyword", None)
    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats = []
    # On fait de même pour le titre de la page
    if motclef:
        resultats = Espece.query.filter(
            Espece.fichier.like("%{}%".format(motclef))
        ).all()
        critère = "Résultat pour la recherche `" + motclef + "`"
    return render_template("form3.html", resultats=resultats, critere=motclef)


@app.route("/charger")
#fonction pour enregistrer une espèce
def upload_form():
    return render_template("charger17OK.html")


@app.route("/upload", methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash("L'image a été correctement téléchargée.")

        return render_template('charger17OK.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route("/enregistrer", methods=['POST'])
def enregistrer_image():
    data = request.form #c'est un tableau associatif (clé-valeur) appelé collection en python, ou dictionnaire de données
    filename_data = data["fichier"]
    regne_data = data["regne"]
    vernaculaire_data = data["vernaculaire"]
    latin_data = data["latin"]
    description_data = data["description"]
    preoccupation_data = data["preoccupation"]


    espece = Espece(
        fichier=filename_data,
        nom_vernaculaire=vernaculaire_data,
        nom_latin=latin_data,
        description=description_data,
        regne=regne_data,
        preoccupation=preoccupation_data
    )
    db.session.add(espece)
    db.session.commit()
    return render_template('charger17OK.html', filename=filename_data)


@app.route('/display/<filename>')
#affiche l'image depuis le repertoire static
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/modifier/<especeid>')
def espece_modif(especeid):
    #photo = Photo.query.filter(id=photoid)
    espece = Espece.query.get(especeid)
    return render_template('modifier2.html', espece=espece)

@app.route('/faune')
def espece_faune():
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    especes = Espece.query.all()
    flash(especes)
    #regne = Espece.query.filter(Espece.regne.like("faune".formal(regne)))).all()
    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    #resultats = []
    # On fait de même pour le titre de la page
    #for espece in especes :
        #if espece:
       # resultats = Espece.query.filter(
        #    Espece.fichier.like("%{}%".format(regne))
        #).all()
        #critère = "Résultat pour la recherche `" + motclef + "`"
   # return render_template('espece_faune2.html', resultats=resultats,  espece=espece)
    return render_template('espece_faune2.html', espece=especes)


@app.route('/flore')
def espece_flore():
    return render_template('espece_flore.html')

@app.route('/apropos')
def page_apropos():
    return render_template('apropos.html')


if __name__ == "__main__":
    app.run(debug=True)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#OBJECTIFS DU 15 MARS 2022:
# - terminer de mettre les champs pour toutes les colonnes de la base dans upload
# - réaranger la redirection après les résultats
# - bien déterminer ce que je veux faire avec mon appli (photo ou pas ?)
