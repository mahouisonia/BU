from bdd import app, db, Auteur, Publication, Exemplaire, Administrateur
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import date

def add_data():
    with app.app_context():
        # Création d'auteurs
        auteurs = [
            Auteur(nom="Ahmed Aberkane"),
            Auteur(nom="Achour Boudjema"),
            Auteur(nom="Mouloud Mammeri"),
            Auteur(nom="Tahar Djaout"),
            Auteur(nom="Eric Zemmour"),
            Auteur(nom="Lounès Matoub")
        ]
        db.session.add_all(auteurs)
        db.session.commit()

        # Création de publications avec titres uniques
        types = ["Roman", "Essai", "Biographie", "Poésie", "Science"]
        titres = [f"Livre  {i}" for i in range(20)]  # Liste des titres uniques
        place = 0
        for i in range(20):
            
            auteur_id = random.choice(auteurs).id
            titre = random.choice(titres)
            titres.remove(titre)  # Assurez-vous que le titre est unique en le supprimant de la liste
            publication = Publication(
                titre=titre,
                type=random.choice(types),
                auteur_id=auteur_id
            )
            db.session.add(publication)
            db.session.commit()

            # Création de 5 exemplaires pour chaque publication
            for j in range(5):
                exemplaire = Exemplaire(
                    publication_id=publication.id,
                    emplacement= place   ,
                    etat=random.choice(["Bon", "moyen", "mauvais"])
                )
                db.session.add(exemplaire)
            place = place + 1
            db.session.commit()

        # Ajout d'un administrateur
        admin = Administrateur(
            nom="MAHOUI",
            prenom="Sonia",
            num_employer="EMP12345",
            email="mahouisonia55@gmail.com",
            mot_de_passe=generate_password_hash('123456789'),
            date_naissance=date(1985, 7, 23),
            telephone="0123456789",
            ville="Paris",
            code_postal="75001"
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    add_data()
