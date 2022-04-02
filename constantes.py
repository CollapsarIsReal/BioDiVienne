from warnings import warn

#Constantes des résultats de recherche
RESULTATS_PAR_PAGES = 10


#Secret Key
SECRET_KEY = "La patate est un excellent féculent"

if SECRET_KEY == "La patate est un excellent féculent":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)