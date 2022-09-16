import streamlit as st
import extra_streamlit_components as stx
from src.s3.read_file import download_s3_file
from src.s3.upload_file import upload_s3_file
import pandas as pd
import re
import datetime


st.set_page_config(
	# layout = "centered",
    layout = "wide",
	initial_sidebar_state = "expanded",
	page_title = "Mon Compte",
    page_icon = "📷"
)


download_s3_file('s3://fotomo-secrets/website_users.csv', 'tmp')


# Login

@st.cache(allow_output_mutation=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()


def start_session(user):
    # for key, value in user.items():
    cookie_manager.set('user_cookie', user, expires_at=datetime.datetime(year=2030, month=2, day=2))
    
    
def end_session():
    cookie_manager.delete('user_cookie')


if 'user_cookie' not in cookie_manager.get_all():
    
    all_users = pd.read_csv('tmp')
    tab1, tab2 = st.tabs(["Client existant", "Nouveau Client"])
    with tab1:
        with st.form("login_form"):
            st.write("Connectez-vous pour accéder à votre espace client")
            email = st.text_input('Adresse Email')
            password = st.text_input('Mot de passe')
            submitted = st.form_submit_button("Se Connecter")
            if submitted:
                user = all_users[(all_users.email == email) & (all_users.password == password)]
                if len(user) == 0:
                    st.error('Aucun utilisateur ne correspond')
                else:
                    st.success('Vous êtes connecté !')
                    start_session(user.loc[0].to_dict())
                    
    with tab2:
        with st.form("register_form"):
            name = st.text_input('Prénom')
            surname = st.text_input('Nom de famille')
            email = st.text_input('Adresse Email')
            password = st.text_input('Mot de passe')
            submitted = st.form_submit_button("S'inscrire")
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
                    all_users.to_csv('tmp', index=None)
                    upload_s3_file('tmp', 's3://fotomo-secrets/website_users.csv')
                    user = {
                            'name': name,
                            'surname': surname,	
                            'email': email,	
                            'password': password
                        }
                    st.success('Vous êtes connecté !')
                    start_session(user)
else:
    st.button("Déconnexion", on_click=end_session)
    user_cookie = cookie_manager.get('user_cookie')
    col1, col2 = st.columns([2,3])
    with col1:
        st.image('https://cataas.com/cat/says/bonjour%20' + user_cookie['name'])
    with col2:
        for key, value in user_cookie.items():
            st.write(key + ": " + value)
    
    
    
    
        

# cookie_manager.set('token', '123', expires_at=datetime.datetime(year=2030, month=2, day=2))
# token = cookie_manager.get('token')
# st.write(token)
