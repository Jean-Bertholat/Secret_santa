from email.mime.text import MIMEText
import random
import smtplib
import streamlit as st

from smtp import email_config

def get_participants():
    participantsXmail = []
    num_participants = st.number_input(" Nombre de participants", min_value=1, step=1, value=1)

    for i in range(num_participants):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(f"Nom du participant {i+1}", key=f"name_{i}")
        with col2:
            email = st.text_input(f"Email du participant {i+1}", key=f"email_{i}")
        if name and email:
            participantsXmail.append((name, email))
    
    return participantsXmail

def generate_secret_santa():
    """Retourne une liste de paires hard-coded pour le Secret Santa."""
    group = st.secrets["smtp"]['group']
    groups = st.secrets["smtp"]['groups']

    # Maintenir la paire fixe
    fixed_pairs = [("Manon", "Alexandra")]

    # Générer les paires aléatoires pour group1
    givers1 = group[:]
    receivers1 = group[:]
    random.shuffle(receivers1)
    while any(giver == receiver for giver, receiver in zip(givers1, receivers1)):
        random.shuffle(receivers1)
    pairs1 = list(zip(givers1, receivers1))

    # Générer les paires aléatoires pour group2 (sauf Manon et Alexandra)
    givers2 = [g for g in groups if g != "Manon"]
    receivers2 = [r for r in groups if r != "Alexandra"]
    random.shuffle(receivers2)
    while any(giver == receiver for giver, receiver in zip(givers2, receivers2)):
        random.shuffle(receivers2)
    pairs2 = list(zip(givers2, receivers2))

    # Combiner toutes les paires
    return pairs1 + pairs2 + fixed_pairs
    
def send_recap(pairs):
    smtp_config = email_config()

    subject = "Récapitulatif Secret Santa"
    body = "Voici les paires de cette année pour le Secret Santa :\n\n"
    for giver, receiver in pairs:
        body += f"- {giver} offre un cadeau à {receiver}\n"
    body += "\nJoyeuses fêtes !"

    # Créer le message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_config['email']
    msg['To'] = smtp_config['recap']  # Envoyer à l'organisateur ou à une liste de diffusion

    # Envoyer l'e-mail
    try:
        with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
            server.starttls()
            server.login(smtp_config['email'], smtp_config['password'])
            server.sendmail(smtp_config['email'], smtp_config['recap'], msg.as_string())
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de l'e-mail : {e}")
    
def send_email(giver, receiver, giver_email):
    """Envoie un e-mail au donneur avec le nom du receveur."""
    smtp_config = email_config()
    
    subject = "Votre Secret Santa 🎅"
    body = f"Bonjour {giver},\n\nVous êtes le Secret Santa de {receiver} ! Préparez lui un joli cadeau 🎁 !\n\nJoyeuses fêtes !"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_config['email']
    msg['To'] = giver[1]

    with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
        try:
            server.starttls()
            server.login(smtp_config['email'], smtp_config['password'])
            server.sendmail(smtp_config['email'], giver_email, msg.as_string())
            st.write(f"Email sent successfully to {giver}!")
        except Exception as e:
            st.error(f'Mail error sending to {giver}!')