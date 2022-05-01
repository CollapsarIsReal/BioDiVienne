from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import LoginManager, current_user, logout_user, login_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# concernant la sauvegarde des images : Crédits Roy's tutorial : https://roytuts.com/upload-and-display-image-using-python-flask/

# création des routes
@app.route("/")
def accueil_(exemple=None):
    """ Route permettant l'affichage d'une page accueil"""
    especes = Espece.query.all()
    #image_1 = Espece.query.get(id)
    return render_template("pages/accueil.html", especes=especes)

@app.route("/accueil")
def accueil(exemple=None):
    """ Route permettant l'affichage d'une page accueil"""
    especes = Espece.query.all()
    #image_1 = Espece.query.get(id)
    return render_template("pages/accueil.html", especes=especes)

@app.route("/recherche")
def recherche():
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats = []

    # On fait de même pour le titre de la page
    titre = "Recherche"
    if motclef:
        resultats = Espece.query.filter(
            Espece.espece_fichier.like("%{}%".format(motclef))
        ).paginate(page=page, per_page=ESPECES_PAR_PAGE)
        titre = "Résultat pour la recherche `" + motclef + "`"

    return render_template("pages/chercher2.html", resultats=resultats, titre=titre, keyword=motclef)


@app.route("/charger")
def upload_form():
    """ Première étape pour appeler /upload
        A FAIRE: paramètres action et statut
        """
    return render_template("pages/charger.html")


@app.route("/upload", methods=['POST'])
def upload_image():
    """Route permettant d'enregistrer l'image de l'espèce que l'on enregistre
        """
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

        return render_template('pages/charger.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route("/enregistrer", methods=['POST'])
def enregistrer_image():
    """Route permettant d'enregistrer l'espèce dans la base de donnée"""
    data = request.form #c'est un tableau associatif (clé-valeur) appelé collection en python, ou dictionnaire de données
    filename_data = data["fichier"]
    regne_data = data["regne"]
    vernaculaire_data = data["vernaculaire"]
    latin_data = data["latin"]
    description_data = data["description"]
    preoccupation_data = data["preoccupation"]

    # initialisation du code retour: 0 = erreur
    return_code = 0
    count_latin = db.session.query(Espece).filter(Espece.espece_nom_latin == latin_data).count()

    # création espèce pour gestion dans le template espece.html
    espece = Espece(
        espece_fichier=filename_data,
        espece_nom_vernaculaire=vernaculaire_data,
        espece_nom_latin=latin_data,
        espece_description=description_data,
        espece_regne=regne_data,
        espece_preoccupation=preoccupation_data,
    )

    # création autorisée si le nom latin est unique
    if count_latin == 0: # nom latin unique


        # On enregistre en premier dans la table authorship la lien espèce/user
        a_cree = Authorship(user=current_user, espece=espece)

        # Puis enregistre l'espèce
        db.session.add(espece)
        db.session.add(a_cree)
        db.session.commit()
        return_code = 1 # OK

    return render_template('pages/espece.html', espece=espece, statut=return_code)


@app.route('/display/<filename>')
def display_image(filename):
    """ Route permettant d'afficher l'image d'une espèce
    depuis le repertoire static """
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/regne/<int:espece_id>')
def regne(espece_id):
    """ Route permettant l'affichage des espèces selon leur règne:
    :param espece_id: Identifiant numérique de l'espèce:
        # id=0 renvoie toutes les espèces peu importe leur règne
        # id=1 renvoie les espèces du règne animal
        # id=2 renvoie les espèces du règne vegetal
        """
    especes = []
    if espece_id == 0:
        especes = Espece.query.all()
    elif espece_id == 1:
        especes = Espece.query.filter(Espece.espece_regne.like("animal")).all()
    elif espece_id == 2:
        especes = Espece.query.filter(Espece.espece_regne.like("vegetal")).all()
    else:
        especes = []
    return render_template('pages/regne.html', especes=especes)


@app.route('/apropos')
def page_apropos():
    """ Route permettant d'accéder à la page "à propos" """
    return render_template('pages/apropos.html')

@app.route('/moncompte')
def mon_compte():
    """ Route permettant d'accéder à la liste de toutes les espèces enregistrées
        selon le compte utilisé
        """
    #unique_espece = Espece.query.get(1)
    especes_user = db.session.query(Espece)\
        .filter(Espece.espece_id == Authorship.authorship_espece_id)\
        .filter(User.user_id == Authorship.authorship_user_id)\
        .filter(User.user_id == current_user.user_id).all()

    return render_template('pages/moncompte.html', especes=especes_user)
    #return render_template('pages/accueil.html')
