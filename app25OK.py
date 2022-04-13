from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
# concernant la sauvgarde des images : Crédits Roy's tutorial : https://roytuts.com/upload-and-display-image-using-python-flask/
import os
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import LoginManager, current_user, logout_user, login_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


UPLOAD_FOLDER = 'static/uploads/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ESPECES_PAR_PAGE = 5

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

#INITIALISATION DES VARIABLES
app = Flask(
    "BioDieVienne",
    #template_folder=templates,
    #static_folder=statics
)
#On configure la base données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BioDivVie2.db'
# On initie l'extension
db = SQLAlchemy(app)
login = LoginManager(app)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# On crée nos différents modèles
''' cette classe ne sert à rien car j'ai déjà user ?
class Personne(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text)
    prenom = db.Column(db.Text)
    utilisateurON = db.Column(db.Integer)'''

class Authorship(db.Model):
    # table qui recoupe l'id du user et l'id de l'espèce qu'il a enregistré
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_espece_id = db.Column(db.Integer, db.ForeignKey('espece.espece_id'))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.relationship("User", back_populates="authorships")
    espece = db.relationship("Espece", back_populates="authorships")

class Espece(db.Model):
    # table qui décrit les espèces
    espece_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    espece_fichier = db.Column(db.Text, unique=True, nullable=False)
    espece_regne = db.Column(db.Text, nullable=False)
    espece_nom_vernaculaire = db.Column(db.Text)
    espece_nom_latin = db.Column(db.Text)
    espece_description = db.Column(db.Text)
    espece_preoccupation = db.Column(db.Text)
    espece_droit_image = db.Column(db.Text)
    authorships = db.relationship("Authorship", back_populates="espece")

class User(UserMixin, db.Model):
    # table qui recense les utilisateurs (et donc inscrits) de l'application
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_nom = db.Column(db.Text, nullable=False)
    user_login = db.Column(db.String(45), nullable=False, unique=True)
    user_email = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    authorships = db.relationship("Authorship", back_populates="user")

    @staticmethod
    def identification(login, motdepasse):
        """ Identifie un utilisateur. Si cela fonctionne, renvoie les données de l'utilisateurs.

        :param login: Login de l'utilisateur
        :param motdepasse: Mot de passe envoyé par l'utilisateur
        :returns: Si réussite, données de l'utilisateur. Sinon None
        :rtype: User or None
        """
        utilisateur = User.query.filter(User.user_login == login).first()
        if utilisateur and check_password_hash(utilisateur.user_password, motdepasse):
            return utilisateur
        return None

    @staticmethod
    def creer(login, email, nom, motdepasse):
        """ Crée un compte utilisateur-rice. Retourne un tuple (booléen, User ou liste).
        Si il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur
        Sinon, elle renvoie True suivi de la donnée enregistrée

        :param login: Login de l'utilisateur-rice
        :param email: Email de l'utilisateur-rice
        :param nom: Nom de l'utilisateur-rice
        :param motdepasse: Mot de passe de l'utilisateur-rice (Minimum 6 caractères)

        """
        erreurs = []
        if not login:
            erreurs.append("Le login fourni est vide")
        if not email:
            erreurs.append("L'email fourni est vide")
        if not nom:
            erreurs.append("Le nom fourni est vide")
        if not motdepasse or len(motdepasse) < 6:
            erreurs.append("Le mot de passe fourni est vide ou trop court")

        # On vérifie que personne n'a utilisé cet email ou ce login
        uniques = User.query.filter(
            db.or_(User.user_email == email, User.user_login == login)
        ).count()
        if uniques > 0:
            erreurs.append("L'email ou le login sont déjà inscrits dans notre base de données")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs

        # On crée un utilisateur
        utilisateur = User(
            user_nom=nom,
            user_login=login,
            user_email=email,
            user_password=generate_password_hash(motdepasse)
        )

        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(utilisateur)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        """ Retourne l'id de l'objet actuellement utilisé

        :returns: ID de l'utilisateur
        :rtype: int
        """
        return self.user_id


@login.user_loader
def trouver_utilisateur_via_id(identifiant):
    return User.query.get(int(identifiant))

@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions des utilisateurs
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")

@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions des utilisateurs
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")

login.login_view = 'connexion'

@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """ Route gérant la déconnexion des utilisateurs
        """
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")

@app.route("/espece/<int:espece_id>")
def espece(espece_id):
    """ Route permettant l'affichage des espèces recensées

        :param espece_id: Identifiant numérique de l'espèce
        """
    unique_espece = Espece.query.get(espece_id)
    return render_template("pages/espece.html", espece=unique_espece)

@app.route("/supprimer/<int:espece_id>")
def espece_supp(espece_id):
    """ Route permettant l'affichage des espèces recensées
            :param espece_id: Identifiant numérique de l'espèce
            """
    espece_supp_ = db.session.query(Espece).filter(Espece.espece_id == Authorship.authorship_espece_id)\
        .filter(User.user_id == Authorship.authorship_user_id)\
        .filter(User.user_id == current_user.user_id)\
        .filter(Espece.espece_id == espece_id).all()
    flash(espece)
    return render_template('pages/moncompte.html', espece_supp=espece_supp_)


@app.route("/accueil")
def accueil(exemple=None):
    """ Route permettant l'affichage d'une page accueil"""
    especes = Espece.query.all()
    #image_1 = Espece.query.get(id)
    return render_template("pages/accueil6.html", especes=especes)

@app.route("/")
def accueil_(exemple=None):
    """ Route permettant l'affichage d'une page accueil"""
    especes = Espece.query.all()
    #image_1 = Espece.query.get(id)
    return render_template("pages/accueil6.html", especes=especes)


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

    return render_template(
        "pages/chercher2.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef
    )


@app.route("/charger")
def upload_form():
    """ Route permettant d'enregistrer une espèce
        """
    return render_template("charger19.html")


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

        return render_template('charger19.html', filename=filename)
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
    droit_image_data = data["droit_image"]


    espece = Espece(
        espece_fichier=filename_data,
        espece_nom_vernaculaire=vernaculaire_data,
        espece_nom_latin=latin_data,
        espece_description=description_data,
        espece_regne=regne_data,
        espece_preoccupation=preoccupation_data,
        espece_droit_image=droit_image_data
    )
    # On enregistre en premier dans la table authorship la lien espèce/user
    a_cree = Authorship(user=current_user, espece=espece)
    # Puis enregistre l'espèce
    db.session.add(espece)
    db.session.add(a_cree)
    db.session.commit()
    return render_template('charger19.html', filename=filename_data)


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
    return render_template('regne2.html', especes=especes)


@app.route('/apropos')
def page_apropos():
    """ Route permettant d'accéder à la page "à propos" """
    return render_template('pages/apropos.html')

@app.route('/moncompte')
def mon_compte():
    """ Route permettant d'accéder à la liste de toutes les espèces enregistrées
        selon le compte utilisé
        """
    especes_user = db.session.query(Espece)\
        .filter(Espece.espece_id == Authorship.authorship_espece_id)\
        .filter(User.user_id == Authorship.authorship_user_id)\
        .filter(User.user_id == current_user.user_id).all()
    return render_template('pages/moncompte.html', especes=especes_user)


if __name__ == "__main__":
    app.run(debug=True)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
