import streamlit as st
import extra_streamlit_components as stx
from src.s3.read_file import download_s3_file
from src.s3.upload_file import upload_s3_file
from src.s3.list_photos import list_bucket
import pandas as pd
import re
import datetime, os
from PIL import Image


st.set_page_config(
	# layout = "centered",
    layout = "wide",
	initial_sidebar_state = "expanded",
	page_title = "Mon Compte",
    page_icon = "📷"
)

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


if 'user_cookie' not in cookie_manager.get_all(): # User is not logged in
    download_s3_file('s3://fotomo-secrets/website_users.csv', 'tmp')
    all_users = pd.read_csv('tmp')
    tab1, tab2 = st.tabs(["Client existant", "Nouveau Client"])
    
    # Existing User - Login Form
    with tab1:
        form = st.form("login_form")
        form.write("Connectez-vous pour accéder à votre espace client")
        email = form.text_input('Adresse Email')
        password = form.text_input('Mot de passe')
        submitted = form.form_submit_button("Se Connecter")
        if submitted:
            user = all_users[(all_users.email == email) & (all_users.password == password)]
            if len(user) == 0:
                st.error('Aucun utilisateur ne correspond')
            else:
                st.success('Vous êtes connecté !')
                start_session(user.iloc[0].to_dict())
                
    # Register Form                    
    with tab2:
        form = st.form("register_form")
        name = form.text_input('Prénom')
        surname = form.text_input('Nom de famille')
        email = form.text_input('Adresse Email')
        password = form.text_input('Mot de passe')
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
                
else: # User is logged in
    st.button("Déconnexion", on_click=end_session)
    user_cookie = cookie_manager.get('user_cookie')
    col1, col2 = st.columns([2,3])
    with col1:
        st.image('https://cataas.com/cat/says/bonjour%20' + user_cookie['name'])
    with col2:
        for key, value in user_cookie.items():
            st.write(key + ": " + value)
    if user_cookie['email'] == 'nicolas.esnis@gmail.com':
        def sync_photos():
            private = [i['Key'] for i in list_bucket('s3://fotomo/')]
            public = [i['Key'] for i in list_bucket('s3://low-resolution-images/')]
            for item in private:
                if item not in public:
                    if '.' in item: # ignore albums
                        img_name = item.split('/')[-1]
                        st.write(img_name)
                        download_s3_file('s3://fotomo/' + item, img_name)
                        image_file = Image.open(img_name)
                        image_file = image_file.convert('RGB')
                        image_file.save(img_name, quality=30 if 'Galerie' not in item else 100)
                        upload_s3_file(img_name, 's3://low-resolution-images/' + item)
                        os.remove(img_name)                    
        if st.button('Sync Photos'):
            sync_photos()
        
        
                
    
    
        
