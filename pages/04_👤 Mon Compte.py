import streamlit as st
import pandas as pd
import json
from src.s3.read_file import download_s3_file, read_s3_df_file, read_s3_json_file
from src.s3.upload_file import upload_s3_file
from src.s3.list_photos import list_bucket
from src.email.utils import send_email
import os
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

all_orders = pd.read_csv('orders/all_orders.csv')

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
    st.subheader('Mon espace client')
    st.button("Déconnexion", on_click=end_session)
    user_cookie = cookie_manager.get('user_cookie')
    if 'order_id' in st.experimental_get_query_params():
            order_id = st.experimental_get_query_params()['order_id'][0]
            st.balloons()
            st.success("Merci pour votre commande ! Un email de confirmation a été envoyé à " + user_cookie['email'] + ". Vous pouvez suivre l'état de votre commande à tout moment en vous connectant à votre espace client Fotomo.")
            if 'basket' in cookie_manager.get_all(key='empty_basket'):
                cookie_manager.delete('basket')
            with open('orders/' + order_id + '.json', 'r') as f:
                order = json.load(f)
            all_orders.loc[all_orders.order_id == order_id, 'payment_confirmed'] = True
            all_orders.to_csv('orders/all_orders.csv', index=None)
            send_email(['nicolas.esnis@gmail.com', 'valerie.esnis@fotomo.fr'], 'Nouvelle commande sur Fotomo.fr', json.dumps(order, indent=4))
            
    tab1, tab2 = st.tabs(["Mes informations personnelles", "Mes commandes"])
    with tab1:

        col1, col2 = st.columns([2,3])
        with col1:
            st.image('https://cataas.com/cat/says/bonjour%20' + user_cookie['name'])
        with col2:
            for key, value in user_cookie.items():
                if key != 'password':
                    st.write(key + ": " + value)
        # Admin
        if user_cookie['email'] in ['nicolas.esnis@gmail.com', 'valerie.esnis@fotomo.fr']:
            
            if user_cookie['email'] == 'valerie.esnis@fotomo.fr':
                st.write('Bonjour chère mère')
            
            def sync_photos():
                for path, subdirs, files in os.walk('images/letters'):
                    for name in files:
                        album = path.split('/')[-1]
                        if album not in os.listdir('images/low-resolution-images'):
                            os.mkdir('images/low-resolution-images/' + album)
                        if name not in os.listdir('images/low-resolution-images/' + album):
                            image_file = Image.open(path + '/' + name)
                            image_file = image_file.convert('RGB')
                            image_file.save('images/low-resolution-images/'  + album + '/' + name, quality = 5   )
                            st.write('images/low-resolution-images/' + album + '/' + name)
            
            if st.button('Sync Photos'):
                sync_photos()
            
            
    with tab2:
        orders = all_orders[(all_orders[all_orders.columns[0]] == user_cookie['email']) & (all_orders.payment_confirmed == True)].reset_index()
        if len(orders) == 0:
            st.info("Vous n'avez aucune commande en cours ou passée.")
        else:
            for index, row in orders.iterrows():
                with st.expander(row['date'] + ' - ' + row['price'] + '€ - ' + row[orders.columns[-1]], True if index==0 else False):
                    with open('orders/' + row['order_id'] + '.json', 'r') as f:
                        order = json.load(f)
                    items = [value for key, value in order.items() if 'item' in key]
                    for i, item in enumerate(items):
                        
                        st.markdown('---')
                        st.write('**Article #' + str(i + 1) + "**")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write('Mot : ' + item['text'] )
                            st.write('Nombre de photos : ' + str(item['number_photos'] ))
                        with col2:
                            st.write('Cadre : ' + item['frame'])
                            st.write('Quantité : ' + str(item['quantity']))
                        st.markdown('---')
                        cols = st.columns(item['text_len'], gap='small')
                        for letter_index, col in enumerate(cols):
                            with col:
                                if item[str(letter_index)]['letter_photo_path']:
                                    
                                    st.image(item[str(letter_index)]['letter_photo_path'])
                                
        
            
