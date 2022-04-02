from flask import render_template
from flask_mail import Message
from ..app import mail, app

def send_email(subject, sender, recipients, text_body, html_body):
    """
    Fonction décrivant le modèle de la fonction d'envoie d'un mail
    :param subject: Objet du mail
    :param sender: Adresse mail émettrice
    :param recipients: Adresse mail réceptrice
    :param text_body: Contenu en texte simple
    :param html_body: Contenu au format html
    :return: None
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def inscription_mail(donnees):
    """
    Fonction envoyant un mail notifiant de l'inscription
    :param donnees: ensemble des attributs de classes enregistrées lors de la fonction inscription()
    :return: None
    """
    send_email("Validation inscription",
               sender=app.config['MAIL_USERNAME'],
               recipients=[donnees.user_email],
               text_body=render_template('email/pages/inscription_mail.txt', user=donnees),
               html_body=render_template("email/pages/inscription_mail.html", user=donnees))

def mdp_mail(user):
    """
    Fonction permettant d'envoyer un mail de réinitialisation de mot de passe
    :param user: utilisateur capturé
    :return: None
    """
    token = user.get_reset_password_token()
    send_email('GreenPy | Demande de mot de passe',
               sender=app.config['MAIL_USERNAME'],
               recipients=[user.user_email],
               text_body=render_template('email/pages/reset_mdp_requete.txt', user=user, token=token),
               html_body=render_template('email/pages/reset_mdp_requete.html', user=user, token=token))