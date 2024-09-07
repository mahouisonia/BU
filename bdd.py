from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.secret_key = '6fnzy39A58a58Q7XdrxF6Zac42PNBBxM'
db = SQLAlchemy(app)


class Auteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    publications = db.relationship('Publication', back_populates='auteur')

# Définition du modèle Publication
class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    auteur_id = db.Column(db.Integer, db.ForeignKey('auteur.id'), nullable=False)
    auteur = db.relationship('Auteur', back_populates='publications')
    exemplaires = db.relationship('Exemplaire', back_populates='publication')

# Définition du modèle Exemplaire
class Exemplaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=False)
    publication = db.relationship('Publication', back_populates='exemplaires')
    emplacement = db.Column(db.Integer, nullable=False)
    etat = db.Column(db.String(20), nullable=False)
    locations = db.relationship('Location', back_populates='exemplaire')
    est_valide = db.Column(db.Boolean, nullable=False, default=True)

# Définition du modèle Utilisateur
class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    telephone = db.Column(db.String(15), nullable=False, unique=True)
    ville = db.Column(db.String(50), nullable=False)
    code_postal = db.Column(db.String(10), nullable=False)
    locations = db.relationship('Location', back_populates='utilisateur')
   
    
# Définition du modèle Utilisateur
class Administrateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    num_employer = db.Column(db.String(20), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    telephone = db.Column(db.String(15), nullable=False, unique=True)
    ville = db.Column(db.String(50), nullable=False)
    code_postal = db.Column(db.String(10), nullable=False)

class Location(db.Model):
    exemplaire_id = db.Column(db.Integer, db.ForeignKey('exemplaire.id'), primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)
    date_emprunt = db.Column(db.Date, nullable=False)
    date_retour = db.Column(db.Date, nullable=True)
    exemplaire = db.relationship('Exemplaire', back_populates='locations')
    utilisateur = db.relationship('Utilisateur', back_populates='locations')

if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()

