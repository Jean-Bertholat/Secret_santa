import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText

from smtp import email_config
from utils import generate_secret_santa, get_participants, send_email, send_recap

custom_css = """
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50; /* Vert */
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    div.stButton > button:first-child:hover {
        background-color: #45a049; /* Vert foncé au survol */
    }
    </style>
    """

def main():
    # Titre de l'application
    smtp_config = email_config()

    st.set_page_config(page_title="Secret Santa", page_icon = "🎅🏻")
    st.markdown(custom_css, unsafe_allow_html=True)
    st.title('🎅🏻 Secret Santa Organizer🎄')
    st.subheader("Qu'est-ce que Secret Santa?")
    st.write("""Secret Santa Organizer est un organisateur d'échange des cadeaux gratuit en ligne! Organisez une Secret Santa party avec des amis, de la famille ou même entre collègues. Après avoir reçu l'e-mail de Secret Santa, vous pourrez ajouter votre propre liste de souhaits, qui sera ensuite délivrée à votre Secret Santa.\
        Chaque année, autour de la période de des fêtes, les personnes du monde entier s'échangent des cadeaux.
        Pour garder les choses intéressantes, vous pouvez assigner une personne à une autre au hasard, afin de s'échanger et s'offrir des cadeaux.
        """)
        
    st.subheader("Comment ça fonctionne?")
    st.write("""Saisisez le nombre de participants, vous avez besoin d'au moins 3 participants. Une fois les informations remplies votre liste Secret Santa sera créée et tous les participants recevront un message contenant le nom de la personne à qu'ils doivent offrir un cadeau.""")


    # Liste des participants
    st.header("Ajouter les participants")
    
    """Retourne une liste de participants prédéfinis avec seulement les e-mails à remplir."""
    predefined_names = ["Lucie", "Amandine", "Océane", "Manon", "Alexandra", "Florance", "Raphaële"]
    participants = []

    st.write("⚠️ Entrez les emails des participants suivants :")
    for i, name in enumerate(predefined_names):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input(f"Nom du participant {i+1}", value=name, key=f"name_{i}", disabled=True)
        with col2:
            email = st.text_input(f"Email du participant {i+1}", key=f"email_{i}")
        participants.append((name, email))
            
    # Vérifier si tous les emails sont remplis
    missing_emails = [name for name, email in participants if not email]
    if missing_emails:
        st.error(f"Les emails suivants sont manquants : {', '.join(missing_emails)}")
        st.button("Générer les paires et envoyer les e-mails", disabled=True)
    
    # Bouton pour générer les paires et envoyer les e-mails
    else:
        if st.button("Générer les paires et envoyer les e-mails"):
            if len(participants) < len(predefined_names):
                st.error(f"Vous devez ajouter au moins {len(predefined_names)} participants pour jouer au Secret Santa.")
            else:
                pairs = generate_secret_santa()
                if pairs:
                    st.success("Paires générées avec succès et e-mails envoyés !")
                    st.header("Résultats du Secret Santa")
                    for giver, receiver in pairs:
                        giver_email = next(email for name, email in participants if name == giver)
                        #st.write(f"🎅 {giver} offre un cadeau à 🎁 {receiver} (Email: {receiver_email})")
                        send_email(giver, receiver, giver_email)
                    
                else:
                    st.error("Une erreur s'est produite lors de la génération des paires. Veuillez réessayer.")
                
                send_recap(pairs)

    # Footer
    st.write("\n\n---")
    st.caption("Créé avec ❤️ par votre Père Noël")

if __name__ == "__main__":
    main()
