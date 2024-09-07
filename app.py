from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from sqlalchemy.orm import joinedload

from bdd import app, db, Utilisateur, Auteur, Exemplaire, Publication, Administrateur, Location
from  activation_mail import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@app.route('/')
def acceuil():
    return render_template("acceuil.html")

@app.route('/page_user')
def page_user():
    return render_template('page_user.html')

@app.route('/page_administrateur')
def page_administrateur():
    return render_template('page_administrateur.html')

from sqlalchemy.exc import IntegrityError

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')
        date_naissance_str = request.form.get('date_naissance')
        date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d')
        telephone = request.form.get('telephone')
        ville = request.form.get('ville')
        code_postal = request.form.get('code_postal')

        if not (nom and email and mot_de_passe and telephone):
            flash("Veuillez remplir tous les champs requis.")
            return redirect(url_for('inscription'))

        if Utilisateur.query.filter_by(telephone=telephone).first():
            flash("Ce numéro de téléphone est déjà utilisé par un autre compte.", "error")
            return redirect(url_for('inscription'))
        
        if Utilisateur.query.filter_by(email= email).first() :
            flash("Ceette adresse mail est déjà utilisé par un autre compte.", "error")
            return redirect(url_for('inscription'))

        hashed_password = generate_password_hash(mot_de_passe)
        new_user = Utilisateur(nom=nom, prenom=prenom, email=email, mot_de_passe=hashed_password,
                               date_naissance=date_naissance, telephone=telephone, ville=ville,
                               code_postal=code_postal)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('connexion'))
        except IntegrityError:
            db.session.rollback()
            flash('Erreur de base de données. Veuillez réessayer.', 'error')
            return redirect(url_for('inscription'))

    return render_template('inscription.html')



@app.route('/ajout_administrateur', methods=['GET', 'POST'])
def ajout_administrateur():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        num_employer = request.form.get('num_employer')
        mot_de_passe = request.form.get('mot_de_passe')
        date_naissance_str = request.form.get('date_naissance')
        date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d')
        telephone = request.form.get('telephone')
        ville = request.form.get('ville')
        code_postal = request.form.get('code_postal')
        
        hashed_password = generate_password_hash(mot_de_passe)
        new_adm= Administrateur(nom=nom, prenom=prenom, email=email, num_employer= num_employer, mot_de_passe=hashed_password,
                               date_naissance=date_naissance, telephone=telephone, ville=ville,
                               code_postal=code_postal)
        db.session.add(new_adm)
        db.session.commit()
        flash('administrateur ajouté avec succes', 'success')
        return redirect(url_for('ajout_administrateur'))
    return render_template('ajout_administrateur.html')
    

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')

        user = Utilisateur.query.filter_by(email=email).first()
        if user and check_password_hash(user.mot_de_passe, mot_de_passe):
            session['utilisateur_id'] = user.id
            flash('Connexion réussie!')
            return redirect(url_for('page_user'))
        else:
            flash('Email ou mot de passe incorrect.')
            return redirect(url_for('connexion'))
    return render_template('connexion.html')

@app.route('/mes_locations')
def mes_locations():
    id_utlisateur = session.get('utilisateur_id')
    mes_locations = db.session.query(Location).filter_by(utilisateur_id = id_utlisateur).\
        join(Location.utilisateur).\
        join(Location.exemplaire).\
        join(Exemplaire.publication).\
        all()
    return render_template('mes_locations.html', mes_locations=mes_locations)
    


@app.route('/connexion_adminitrateur', methods=['GET', 'POST'])
def connexion_administrateur():
    if request.method == 'POST':
        num_employer = request.form.get('num_employer')
        mot_de_passe = request.form.get('mot_de_passe')

        user = Administrateur.query.filter_by(num_employer=num_employer).first()
        if user and check_password_hash(user.mot_de_passe, mot_de_passe):
            session['user_id'] = user.id
            flash('Connexion réussie!')
            return redirect(url_for('page_administrateur'))
        else:
            flash('Email ou mot de passe incorrect.')
            return redirect(url_for('connexion_administrateur'))
    return render_template('connexion_administrateur.html')

@app.route('/verification_email', methods=['GET', 'POST'])
def verification_email():
    if request.method == 'POST':
        email = request.form.get('email')
        if email and email_exists(email):
            temp = generate_number()
            send_activation_code_pin(email, temp)
            
            send_time = datetime.now() 
            session['email'] = email
            session['send_time'] = send_time
            session['user_secret_code'] = temp  
            print(temp)
            return render_template('code_pin_submit.html')
        else:
            flash("Adresse mail incorrecte ou non fournie!")
            return redirect(url_for('verification_email'))
    return render_template('mail_submit.html')

@app.route('/submit_code', methods=['GET', 'POST'])
def submit_code():
    if request.method == 'POST':
        user_code = int( request.form.get('code'))
        if not user_code:
            flash("Aucun code fourni!")
            return redirect(url_for('submit_code'))
        
        send_time_org = session.get('send_time') 
        send_time =send_time_org.strftime("%Y-%m-%d %H:%M:%S")
        valid_time = datetime.now() - timedelta(minutes=10)  
        
        if send_time and datetime.strptime(send_time, "%Y-%m-%d %H:%M:%S") < valid_time:
            flash("Le code a expiré. Veuillez demander un nouveau code.")
            return redirect(url_for('verification_email'))

        session_code = session.get('user_secret_code')  
        if user_code == session_code:
            return redirect(url_for('change_password'))  
        else:
            flash("Le code saisi est incorrect.")
            return redirect(url_for('submit_code'))

    return render_template('code_pin_submit.html')  


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        new_password = request.form['confirmation_mot_de_passe']
        
        user = Utilisateur.query.filter_by(email=session.get('email')).first()
        
        if user:
            hashed_password = generate_password_hash(new_password)
            user.mot_de_passe = hashed_password 
            db.session.commit()  
            flash('Votre mot de passe a été mis à jour avec succès!')
            return redirect(url_for('connexion'))  
        else:
            flash('Nom d utilisateur incorrect.')

    return render_template('changement_MDP.html')


@app.route('/recherche_livre', methods=['GET'])
def recherche_livre():
    page_type = request.args.get('page_type')
    search_type = request.args.get('filter')
    query = request.args.get('q', '')
    

    books_query = db.session.query(
        Publication,
        db.func.count(Exemplaire.id).label('exemplaire_count')
    ).join(Exemplaire).filter(Exemplaire.est_valide == True)

    if search_type == 'titre':
        books_query = books_query.filter(Publication.titre.like(f'%{query}%'))
    elif search_type == 'auteur':
        books_query = books_query.join(Auteur).filter(Auteur.nom.like(f'%{query}%'))
    elif search_type == 'type':
        books_query = books_query.filter(Publication.type.like(f'%{query}%'))

    books_query = books_query.group_by(Publication.id)
    books = books_query.all()

    if page_type == 'admin':
        return render_template('page_administrateur.html', books=books)
    else:
        return render_template('page_user.html', books=books)



@app.route('/louer_exemplaire', methods=['POST'])
def louer_exemplaire():
    user_id = request.form['user_id']
    publication_id = request.form['publication_id']
    
    user = Utilisateur.query.filter_by(id = user_id).all()
    if not user :
        flash("utilisateur introuvable")
        return redirect(url_for('page_administrateur'))
    exemplaire = Exemplaire.query.filter_by(publication_id=publication_id, est_valide=True).order_by(db.func.random()).first()
    if not exemplaire:
        flash("Aucun exemplaire disponible pour cette publication.")
        return redirect(url_for('page_administrateur'))

    date_emprunt = datetime.utcnow()
    date_retour = date_emprunt + timedelta(days=30)

    nouvelle_location = Location(
        utilisateur_id=user_id,
        exemplaire_id=exemplaire.id,
        date_emprunt=date_emprunt,
        date_retour=date_retour
    )
    exemplaire.est_valide = False  
    db.session.add(nouvelle_location)
    db.session.commit()

    flash("La location a été effectuée avec succès. La date de retour est le " + date_retour.strftime('%Y-%m-%d') + ".")
    return redirect(url_for('page_administrateur'))


@app.route('/add_publication', methods=['GET', 'POST'])
def add_publication():
    if request.method == 'POST':
        titre = request.form['titre']
        type_ = request.form['type']
        nom_auteur = request.form['auteur']
        nb_exemplaires =int (request.form['nb_exemplaires'])

        auteur = Auteur.query.filter_by(nom=nom_auteur).first()
        publication = Publication.query.filter_by(titre=titre).first()
        
            
        if not auteur:
            auteur = Auteur(nom=nom_auteur)
            db.session.add(auteur)
            db.session.commit()
            
            
        dernier_exemplaire = Exemplaire.query.order_by(Exemplaire.id.desc()).first() 
        place = dernier_exemplaire.emplacement 
        if not publication :
            nouvelle_publication = Publication(titre=titre, type=type_, auteur_id=auteur.id)
            db.session.add(nouvelle_publication)
            db.session.commit()
            for j in range(nb_exemplaires ):
                exemplaire = Exemplaire(
                    publication_id= nouvelle_publication.id,
                    emplacement=place +1,
                    etat= 'Neuf'
                )
                db.session.add(exemplaire)
            
            db.session.commit()
        
        else:
            exemplaire = db.session.query(Exemplaire).join(Publication).filter(Publication.titre == titre).first()
            placee = exemplaire.emplacement 
            for j in range(nb_exemplaires ):
                exemplaire = Exemplaire(
                    publication_id= publication.id,
                    emplacement=placee,
                    etat= 'Neuf'
                )
                db.session.add(exemplaire)
            
            db.session.commit()
            

        flash('Publication ajoutée avec succès.')
        return redirect(url_for('add_publication'))

    return render_template('add_publication.html')

@app.route('/delete_publication/<int:publication_id>', methods=['POST','GET'])
def delete_publication(publication_id):
        publication = Publication.query.get(publication_id)
        
        if publication:
            Exemplaire.query.filter_by(publication_id=publication_id).delete()
            db.session.delete(publication)
            db.session.commit()
            
            flash('Publication supprimée avec succès.')
        else:
            flash('Publication introuvable.')

        return redirect(url_for('page_administrateur'))




@app.route('/Afficher_locations')
def Afficher_locations():
    
    
    date_actuelle = datetime.now()


    date_limite = date_actuelle + timedelta(days=5)
    Afficher_locations = Location.query.filter(Location.date_retour <= date_limite).all()
    
   
    
    return render_template('Afficher_locations.html', Afficher_locations=Afficher_locations)






@app.route('/toutes_locations')
def toutes_locations():
    # Récupération des données en utilisant les jointures nécessaires
    toutes_locations = db.session.query(Location).\
        join(Location.utilisateur).\
        join(Location.exemplaire).\
        join(Exemplaire.publication).\
        all()
    return render_template('toutes_location.html', toutes_locations=toutes_locations)

@app.route('/message_rappel', methods=['GET', 'POST'])
def message_rappel():
    date_actuelle = datetime.now()

    # Calculer la date limite (5 jours à partir de la date actuelle)
    date_limite = date_actuelle + timedelta(days=5)

    # Effectuer la requête pour récupérer les locations où la date de retour est dans les 5 prochains jours
    locations_a_rendre = Location.query.filter(Location.date_retour <= date_limite).all()

    # Récupérer les e-mails des utilisateurs associés à ces locations
    emails = [location.utilisateur.email for location in locations_a_rendre]

    emails = [email for email in emails if email]  # Filtrer les e-mails vides
    if emails:
        for email in emails:
            send_msg_rappel(email)  # Utiliser email au lieu de mail
        flash("Messages envoyés avec succès !")
    else:
        flash('Aucun e-mail trouvé.')

    return render_template("afficher_locations.html")
        
    
@app.route('/retourner_exemplaire', methods=['POST','GET'])
def retourner_exemplaire():
    if request.method == 'POST':
        exemplaire_id = request.form['id_exemplaire']
        location = Location.query.filter_by(exemplaire_id=exemplaire_id).first()
        exemplaire = Exemplaire.query.get(exemplaire_id)   
        if location and exemplaire :
            db.session.delete(location)
            exemplaire = Exemplaire.query.get(exemplaire_id)
            exemplaire.est_valide = True
            db.session.commit()
            flash('Le livre a été rendu avec succès.')
            
        else:
            flash('Aucune location trouvée pour cet exemplaire.')
    return render_template('retourner_livre.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')
if __name__ == '__main__':
    app.run(debug=True, port=5001)
