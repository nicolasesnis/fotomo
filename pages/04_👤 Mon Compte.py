import streamlit as st
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
            order = read_s3_json_file('s3://fotomo-secrets/orders/' + order_id + '.json')
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
            
            
    with tab2:
        all_orders = read_s3_df_file('s3://fotomo-secrets/orders/all_orders.csv')
        orders = all_orders[all_orders[all_orders.columns[0]] == user_cookie['email']].reset_index()
        if len(orders) == 0:
            st.info("Vous n'avez aucune commande en cours ou passée.")
        else:
            for index, row in orders.iterrows():
                with st.expander(row['date'] + ' - ' + row['price'] + '€ - ' + row[orders.columns[-1]], True if index==0 else False):
                    order = read_s3_json_file('s3://fotomo-secrets/orders/' + row['order_id'] + '.json')
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
                                
        
            
