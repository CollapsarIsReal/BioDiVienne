# BioDiVienne

![image accueil du site](https://github.com/CollapsarIsReal/BioDiVienne/blob/master/biodivienne/static/images/accueil.png "accueil")

Ce dépot contient le projet final du cours Python dispensé en M2 TNAH de l'Ecole nationale des chartes par Mr Thibault Clérice, doctorant et référent master à l'école.
BioDiVienne est un projet de recensement des espèces animales et végétales parmis lesquels nous vivons. Idéal pour un usage personnel, à domicile ou au travail (si c'est pas trop bétonné), cette application permet ainsi de pouvoir créer des fiches correspondantes aux différentes espèces rencontrées.

Ce travail doit être rendu au plus tard le lundi 2 mai afin qu'il soit évalué et corrigé.
Cependant, certains points du projets n'ont pu être traité jusqu'à présent, la liste ci-dessous étant un récapitulatif du travail qu'il reste à faire ainsi que des choses à améliorer à l'avenir.

## Travail effectué:
BioDiVienne est une application avec base de données relationnelle, comprenant formulaire pour ajout, suppression, édition. Il est possible de naviguer dans la collection, d'y faire une recherche simple. Un index (sous trois formes) y est inclu.

## Travail restant:

* reprendre la structure HTML des templates
* revoir la structure des fichiers .py (quelques commentaires inutiles doivent encore se cacher...)
* afficher un message d'erreur si l'authentification de l'utilisateur échoue
* résoudre quelques problèmes de css
* rendre les valeurs des champs de formulaire en italiques

## Idées de perfectionnement pour la suite

* proposer un système de datation pour visualiser les espèces rencontrées en fonction des jours de l'année.
* permettre une recherche avancée avec différents filtres
* planter des arbres
* manger local...mais je m'égare...
* divers outils statistiques

## Installation de l'application (crédit au tuto du projet [OBBC](https://github.com/Chartes-TNAH/projet_OBBC_AppPy) qui explique ça mieux que moi...)

1. Installer BioDiVienne à partir de la branche master du dépôt BioDiVienne Github :
`$ git clone https://github.com/CollapsarIsReal/BioDiVienne.git `

2. Installer Python via le [site](https://www.python.org/downloads/). Pour rappel : la plupart des systèmes Linux, intègre déjà Python.

3. Créer un environnement virtuel à l'aide de VirtualEnv. Dans votre terminal, taper la commande : `$ pip install virtualenv` pour installer VirtualEnv puis `$ virtualenv -p python3 env` ou sous windows : `$ virtualenv -p` puis `$ env:python3 env`

4. Activer l'environnement virtuel via `$ source env/bin/activate`. Pour quitter l'environnement taper simplement `$ deactivate`.

5. Dans le terminal, rentrer la commande `$ cd BioDiVienne/` pour se placer au niveau du fichier requirements.txt, puis installer les différents packages nécéssaires avec la commande suivante : `$ pip install -r requirements.txt`.

6. A la fin du téléchargement, lancer l'application avec la commande `$ python run.py` ou `$ python3 run.py` via le serveur local et selon votre version de python `($ python --version ou -V)`
