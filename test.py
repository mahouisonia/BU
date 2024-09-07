from datetime import datetime, timedelta
from bdd import *

def add_dta():
    with app.app_context():
        # Votre code existant pour remplir la base de données...

        # Récupération des utilisateurs
        utilisateur1 = Utilisateur.query.get(1)

        # Calcul de la date de retour pour les utilisateurs 1 et 2 (5 jours à partir d'aujourd'hui)
        date_retour_1_2 = datetime.now() + timedelta(days=5)

        # Calcul de la date de retour pour l'utilisateur 3 (5 jours avant aujourd'hui)
        date_retour_3 = datetime.now() + timedelta(days=4)

        # Calcul de la date de retour pour l'utilisateur 3 (5 jours avant aujourd'hui)
        date_emprunt = datetime.now()

        # Ajout des locations pour les utilisateurs
        location1 = Location(
            exemplaire_id=10,  # ID de l'exemplaire que vous souhaitez attribuer
            utilisateur_id=utilisateur1.id,
            date_emprunt=date_emprunt,
            date_retour=date_retour_1_2
        )
        db.session.add(location1)
        db.session.commit()

if __name__ == "__main__":
    add_dta()
