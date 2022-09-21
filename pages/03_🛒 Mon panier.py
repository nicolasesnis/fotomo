import streamlit as st
import numpy as np
import extra_streamlit_components as stx
import datetime
from PIL import Image 
import urllib.request
import urllib.parse

Image.MAX_IMAGE_PIXELS = 10000000000

# from io import BytesIO


st.set_page_config(
	# layout = "centered",
    layout = "wide",
	initial_sidebar_state = "collapsed",
	page_title = "Mon panier",
    page_icon = "📷"
)


@st.cache(allow_output_mutation=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

cookies = cookie_manager.get_all()
if 'basket' in cookies:
    basket = cookies['basket']
else:
    basket = None


def save_basket(basket, item_index):
    cookie_manager.set('basket', basket, expires_at=datetime.datetime(year=2030, month=2, day=2), key=str(item_index) + '_' + text)            
    
frames = {
        'Sans cadre': 0, 
        'Sous verre, clipsé (+ 7€)': 7,
        'Cadre en bois, couleur noire (+ 20€)': 20
    }
    
non_letter_keys = ['quantity', 'frame', 'price']

def get_prices(basket):
    # price per letter: 5
    
    for item_index, item in enumerate(basket):
        basket[item_index]['price'] = 0
        for key, value in item.items():
            if key not in non_letter_keys:
                basket[item_index]['price'] += 5
            elif key == 'frame':
                basket[item_index]['price'] += frames[value]
    
            
            
            
            

if basket is None or len(basket) == 0:
    st.info('Votre panier est vide ! Dirigez-vous vers la section "Créer mon mot" pour effectuer une sélection.')
else:
    get_prices(basket)
    st.info('Les photos sont imprimées professionnellement en format 10 x 15 cm, finition brillante, sur papier Fujifilm épais (210 g/m2).')
    st.subheader('Il y  a ' + str(len(basket)) + ' sélection(s) dans votre panier')
    col1, col2 = st.columns([3,1])
    with col1:
        st.write('Sous-total avant les frais de livraison : __' +  str(sum([item['price'] for item in basket])) + '__ €')
    
    with col2:
        if st.button('Valider le panier ✅ '):
            st.success('Success')
    
    for item_index, item in enumerate(basket):
        
        text = ''.join([value['letter'] for key, value in item.items() if key not in non_letter_keys])
        text_list = [value for key, value in item.items() if key not in non_letter_keys]
        
        with st.expander('#' +  str(item_index + 1)  + ' - Mot : ' + text, expanded = True if item_index== 0 else False):
            
            
            cols = st.columns(len(text_list), gap='small')
            for letter_index, col in enumerate(cols):
                with col:  
                    st.image(text_list[letter_index]['letter_photo_path'], use_column_width='auto')
            
            
            
            if 'frame' in item.keys():
                frame = item['frame']
            else:
                frame = 'Sans cadre'
            basket[item_index]['frame'] =  st.radio('Option: Cadre', frames.keys(), index=list(frames.keys()).index(frame), on_change=save_basket, kwargs={'basket': basket, 'item_index': item_index}, key=str(item_index) + "_radio_" + text)
            
            if st.button('✨ Prévisualiser avec le cadre en qualité maximale'):
                st.write('Mum envoie moi les cadres please!')
            
            if 'quantity' in item.keys():
                quantity = item['quantity']
            else:
                quantity = 1
                
            basket[item_index]['quantity'] = int(st.number_input('Quantité:',min_value=1, value=quantity, key=str(item_index) + "_quantity_" + text, on_change=save_basket, kwargs={'basket': basket, 'item_index': item_index}))
            
            if st.button('❌ Supprimer du panier', key=str(item_index) + "_delete_" + text):
                del basket[item_index]
                save_basket(basket, item_index)
                




                

            