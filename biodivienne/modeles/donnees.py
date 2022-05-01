from flask import url_for
import datetime

from .. app import db

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
    espece_regne = db.Column(db.Text)
    espece_nom_vernaculaire = db.Column(db.Text, nullable=False)
    espece_nom_latin = db.Column(db.Text, unique=True, nullable=False)
    espece_description = db.Column(db.Text)
    espece_preoccupation = db.Column(db.Text)
    authorships = db.relationship("Authorship", back_populates="espece")

