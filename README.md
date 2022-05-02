# BioDiVienne

Ce dépot contient le projet final du cours Python dispensé en M2 TNAH de l'Ecole nationale des chartes par Mr Thibault Clérice, doctorant et référent master à l'école.
BioDiVienne est un projet de recensement des espèces animales et végétales parmis lesquels nous vivons. Idéal pour un usage personnel, à domicile ou au travail (si c'est pas trop bétonné), cette application permet ainsi de pouvoir créer des fiches correspondantes aux différentes espèces rencontrées.

Ce travail doit être rendu au plus tard le lundi 2 mai afin qu'il soit évalué et corrigé.
Cependant, certains points du projets n'ont pu être traité jusqu'à présent, la liste ci-dessous étant un récapitulatif du travail qu'il reste à faire ainsi que des choses à améliorer à l'avenir.

## Travail effectué:
BioDiVienne est une application avec base de données relationnelle, comprenant formulaire pour ajout, suppression, édition. Il est possible de naviguer dans la collection, d'y faire une recherche simple. Un index (sous trois formes) y est inclu.

## Travail restant:

* faire fonctionner mon fichier requirement.txt avec les différents modules appelés...
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

EDIT: Pour l'instant, l'application ne fonctionne pas en lançant le fichier **requirements.txt**. En attendant vous devez récupérer le dossier **envBDV** qui se trouve dans le commit intitulé "upload et pagination OK" n°c9f15272ba8e84d42a51c1af34e3113e745295f0 du 2 mai 2022 ([voir ici](https://github.com/CollapsarIsReal/BioDiVienne/tree/c9f15272ba8e84d42a51c1af34e3113e745295f0)). Placez ce dossier dans le répertoir BioDiVienne créé à la suite du git clone (voir étape 1). Promis, ce problème sera réglé très bientôt.

3. Lancez l'environnement virtuel grâce à la commande `$ source env/bin/activate`.

4. Après cela, vous pouvez lancer l'application avec la commande `$ python3 run.py`.
-----
