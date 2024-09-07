from datetime import datetime, timedelta
import random
from bdd import Utilisateur  
from mailjet_rest import Client
import os



def generate_number():
    number = random.randint(100000, 999999)
    return number


def send_activation_code_pin(user_email, code_pin):
    # Récupérer les clés API de vos variables d'environnement
    api_key = os.environ['Api_Key']
    api_secret = os.environ['Secret_Key']

    # Initialiser le client Mailjet
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
  
    # Préparer les données pour l'e-mail
    data = {
      'Messages': [
        {
          "From": {
            "Email": "ccsonia87@gmail.com",  # Votre adresse e-mail
            "Name": "Bibliothèque municipale"
          },
          "To": [
            {
              "Email": user_email,  # Adresse e-mail du destinataire
              "Name": "You"
            }
          ],
          "Subject": "Activation de votre compte",
          "HTMLPart": f"""
            <p>Bonjour ! Merci de vous être inscrit sur notre site.</p>
            <p>Pour activer votre compte, veuillez cliquer sur le lien ci-dessous :</p>
             <a >Activer votre compte  {code_pin}</a>
        
          """
        }
      ]
    }

  
    result = mailjet.send.create(data=data)

    print(result.status_code)
    print(result.json())
   


def email_exists(email):
    
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    
    
    return utilisateur is not None

def send_msg_rappel(user_email):
    # Récupérer les clés API de vos variables d'environnement
    api_key = os.environ['Api_Key']
    api_secret = os.environ['Secret_Key']

    # Initialiser le client Mailjet
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
  
    # Préparer les données pour l'e-mail
    data = {
      'Messages': [
        {
          "From": {
            "Email": "ccsonia87@gmail.com",  # Votre adresse e-mail
            "Name": "Bibliothèque municipale"
          },
          "To": [
            {
              "Email": user_email,  # Adresse e-mail du destinataire
              "Name": "You"
            }
          ],
          "Subject": "Rappel de retour de votre location à la bibliothèque Opéra",

"HTMLPart": f"""
<p>Bonjour,</p>
<p>Nous vous rappelons que la date de retour de votre location approche.</p>
<p>Veuillez vous assurer de retourner votre emprunt avant la date due.</p>
<p>Si vous avez des questions ou si vous souhaitez prolonger votre location, n'hésitez pas à nous contacter.</p>
<p>Merci de votre attention et à bientôt à la bibliothèque!</p>
<p>Cordialement,</p>
<p>L'équipe de la bibliothèque Opéra</p>
"""

        }
      ]
    }

  
    result = mailjet.send.create(data=data)



   