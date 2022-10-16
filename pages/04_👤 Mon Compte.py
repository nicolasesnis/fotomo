import streamlit as st
import extra_streamlit_components as stx
from src.s3.read_file import download_s3_file, read_s3_df_file
from src.s3.upload_file import upload_s3_file
from src.s3.list_photos import list_bucket
from src.email.utils import send_email
import re
import datetime, os
from PIL import Image
from src.cookies.utils import get_manager

st.set_page_config(
    layout = "wide",
	page_title = "Mon Compte",
    page_icon = "📷"
)

from src.components.login import login, register

cookie_manager = get_manager()

def end_session():
    cookie_manager.delete('user_cookie')


if 'user_cookie' not in cookie_manager.get_all(): # User is not logged in
    st.write("Connectez-vous pour accéder à votre espace client")
    tab1, tab2 = st.tabs(["Client existant", "Nouveau Client"])
    # Existing User - Login Form
    with tab1:
        login()
    # Register Form                    
    with tab2:
        register()
                
else: # User is logged in
    st.button("Déconnexion", on_click=end_session)
    user_cookie = cookie_manager.get('user_cookie')
    col1, col2 = st.columns([2,3])
    with col1:
        st.image('https://cataas.com/cat/says/bonjour%20' + user_cookie['name'])
    with col2:
        for key, value in user_cookie.items():
            st.write(key + ": " + value)
            
    # Admin
    if user_cookie['email'] in ['nicolas.esnis@gmail.com', 'valerie.esnis@fotomo.fr']:
        
        if user_cookie['email'] == 'valerie.esnis@fotomo.fr':
            st.write('Bonjour chère mère')
        
        def sync_photos():
            private = [i['Key'] for i in list_bucket('s3://fotomo/')]
            public = [i['Key'] for i in list_bucket('s3://low-resolution-images/')]
            for item in private:
                if item not in public or 1==1:
                    if '.' in item: # ignore albums
                        img_name = item.split('/')[-1]
                        download_s3_file('s3://fotomo/' + item, img_name)
                        image_file = Image.open(img_name)
                        image_file = image_file.convert('RGB')
                        if 'Galerie' not in item:
                            image_file.save(img_name, quality = 5   )
                            st.write(img_name)
                        else:
                            image_file.save(img_name, quality= 100)
                        upload_s3_file(img_name, 's3://low-resolution-images/' + item)
                        os.remove(img_name)                    
                        
        if st.button('Sync Photos'):
            sync_photos()
        
        
                
    
    
        
