

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ESPECES_PAR_PAGE = 10

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

#INITIALISATION DES VARIABLES
app = Flask(
    "BioDiVienne",
    #template_folder=templates,
    #static_folder=statics
)
# On configure la base données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BioDivVie2.db'
# On initie l'extension
db = SQLAlchemy(app)
login = LoginManager(app)
app.secret_key = "pain_de_vie"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


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
    return_code = 0
    count_id = db.session.query(Authorship).filter(Authorship.authorship_espece_id == espece_id).filter(Authorship.authorship_user_id == current_user.user_id).count()

    if count_id == 1: # l'utilisateur est autorisé à supprimer l'instance
        return_code = db.session.query(Espece).filter(Espece.espece_id == espece_id).delete()
        # test: return_code = 0
        if return_code != 0: # si pas d'erreur dans la suppression d'espece
            db.session.query(Authorship).filter(Authorship.authorship_espece_id == espece_id).delete()
            db.session.commit()
    return render_template('pages/moncompte.html', action="suppr", statut=return_code)

@app.route("/modifier/<int:espece_id>")
def espece_modif(espece_id):
    """ Route permettant de modifier une espèce
                :param espece_id: Identifiant numérique de l'espèce
                """
    unique_espece = Espece.query.get(espece_id)

    return render_template('pages/modifier.html', espece=unique_espece)

@app.route("/modifier_post", methods=['POST'])
def modifier_post():
    """ Route permettant de modifier l'espèce dans la base de données """
    return_code = 0

    if request.method == "POST":
        data = request.form  # c'est un tableau associatif (clé-valeur) appelé collection en python, ou dictionnaire de données
        espece_id_data = data["espece_id"]
        vernaculaire_data = data["vernaculaire"]
        latin_data = data["latin"]
        description_data = data["description"]
        preoccupation_data = data["preoccupation"]
        regne_data = data["regne"]

        # vérification que l'utilisateur est bien l'auteur de l'espèce avant modification
        count_authorship = db.session.query(Authorship).filter(Authorship.authorship_espece_id == espece_id_data).filter(
            Authorship.authorship_user_id == current_user.user_id).count()
        # vérification du nom latin unique ou non avant modification
        count_latin = db.session.query(Espece).filter(Espece.espece_nom_latin == latin_data).filter(Espece.espece_id != espece_id_data).count()

        if count_authorship == 1 and count_latin == 0: # l'utilisateur est autorisé à modifier l'instance

            unique_espece = Espece.query.get(espece_id_data) # récupération de l'instance de l'espèce de la base

            if unique_espece: # pas d'erreur, récupération OK
                unique_espece.espece_nom_vernaculaire = vernaculaire_data
                unique_espece.espece_nom_latin = latin_data
                unique_espece.espece_description = description_data
                unique_espece.espece_regne = regne_data
                unique_espece.espece_preoccupation = preoccupation_data

            # Puis modification de l'espèce
                db.session.commit()
                return_code = 1  # OK
    return render_template('pages/moncompte.html', action="modif", statut=return_code)






