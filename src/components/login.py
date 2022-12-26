import streamlit as st
import pandas as pd
import extra_streamlit_components as stx
from src.email.utils import send_email
import re
import datetime, os
from PIL import Image
from src.cookies.utils import get_manager

cookie_manager = get_manager()

all_users = pd.read_csv('secrets/website_users.csv')

def start_session(user):
    # for key, value in user.items():
    cookie_manager.set('user_cookie', user, expires_at=datetime.datetime(year=2030, month=2, day=2))

# Existing User - Login Form
def login():
    form = st.form("login_form")
    email = form.text_input('Adresse Email')
    password = form.text_input('Mot de passe', type='password')
    submitted = form.form_submit_button("Se Connecter")
    if submitted:
        user = all_users[(all_users.email == email) & (all_users.password == password)]
        if len(user) == 0:
            st.error('Aucun utilisateur ne correspond')
        else:
            st.success('Vous êtes connecté !')
            start_session(user.iloc[0].to_dict())
            
def register():
    form = st.form("register_form")
    name = form.text_input('Prénom')
    surname = form.text_input('Nom de famille')
    email = form.text_input('Adresse Email')
    password = form.text_input('Mot de passe' , type='password')
    submitted = form.form_submit_button("S'inscrire")
    if submitted:
        if email in all_users.email.unique():
            st.error('Cette adresse email est déjà associée à un compte Fotomo.')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error('Veuillez entrer une adresse email valide.')
        elif email == '' or name == '' or password == '' or surname == '':
            st.error('Veuillez renseigner tous les champs.')
        elif len(password)  < 6:
            st.error('Mot de passe trop court.')
        else:
            all_users.loc[len(all_users.index)] = [name,	surname,	email,	password] 
            all_users.to_csv('secrets/website_users.csv', index=None)
            user = {
                    'name': name,
                    'surname': surname,	
                    'email': email,	
                    'password': password
                }
            st.success('Vous êtes connecté !')
            send_email(['valerie.esnis@fotomo.fr', 'nicolas.esnis@gmail.com'], 'Nouvel utilisateur sur Fotomo.fr', str(user))
            start_session(user)

                
    
    
        
