import streamlit as st


def email_config():
    # Configuration SMTP
    #("Configuration SMTP (pour envoyer les e-mails)")
    conf_smtp = st.secrets["smtp"]
    
    smtp_email = conf_smtp["email"]
    recap_reciever = conf_smtp["recap"]
    smtp_password = conf_smtp["password"]
    smtp_server = conf_smtp["server"]
    smtp_port = conf_smtp["port"]
    
    dict = {
        'email': smtp_email,
        'password': smtp_password,
        'recap': recap_reciever,
        'server': smtp_server,
        'port': smtp_port
    }
    

    
    return dict