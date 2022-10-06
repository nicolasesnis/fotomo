import streamlit as st
import extra_streamlit_components as stx
import datetime
from PIL import Image ,ImageOps
import requests
from io import BytesIO
from src.s3.read_file import create_presigned_url
import json


def show_basket():
    Image.MAX_IMAGE_PIXELS = 10000000000

    st.set_page_config(
        layout = "wide",
        page_title = "Mon panier",
        page_icon = "📷"
    )

    non_letter_keys = ['quantity', 'frame', 'price', 'text', 'number_photos', 'text_len']

    @st.cache(allow_output_mutation=True)
    def get_manager():
        return stx.CookieManager()

    cookie_manager = get_manager()

    cookies = cookie_manager.get_all()
    if 'basket' in cookies:
        basket = cookies['basket']
        
    else:
        basket = None


    def save_basket(basket, item_index, key=None, value=None):
        if key and value:
            basket[item_index][key] = value
        cookie_manager.set('basket', basket, expires_at=datetime.datetime(year=2030, month=2, day=2), key=str(item_index) + '_' + text + '_' + str(key))            

    with open('frames.json', 'r') as f:
        frames = json.load(f)
        


    def get_prices(basket):
        for item_index, item in enumerate(basket):
            if item['number_photos'] < 10:
                basket[item_index]['price'] = 5  * item['number_photos']
            else:
                basket[item_index]['price'] = 4.5  * item['number_photos']
            for key, value in item.items():    
                if key == 'frame':
                    if 'unit_price' in frames[value].keys():
                        basket[item_index]['price'] += frames[value]['unit_price'] * item['number_photos']
                    elif item['number_photos'] in frames[value].keys():
                        basket[item_index]['price'] += frames[value][item['text_len']]
                        
                if key == 'quantity':
                    basket[item_index]['price'] = basket[item_index]['price'] * basket[item_index]['quantity']
                

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
                st.success('feature pas encore dispo')
        
        for item_index, item in enumerate(basket):
            
            text = ''.join([value['letter'] for key, value in item.items() if key not in non_letter_keys])
            text_list = [value for key, value in item.items() if key not in non_letter_keys]
            
            with st.expander('#' +  str(item_index + 1)  + ' - Mot : ' + text + ' - Prix : ' + str(item['price']) + ' €', expanded = True ):
                
                
                cols = st.columns(len(text_list), gap='small')
                for letter_index, col in enumerate(cols):
                    with col:  
                        url = text_list[letter_index]['letter_photo_path']
                        if url: 
                            if item['number_photos'] > 2:
                                st.image(text_list[letter_index]['letter_photo_path'], use_column_width='auto')
                            else:
                                st.image(text_list[letter_index]['letter_photo_path'], width=200)
                        else:
                            st.write('')
                if st.button('❌ Supprimer du panier', key=str(item_index) + "_delete_" + text):
                    del basket[item_index]
                    save_basket(basket, item_index)
                    
                if 'frame' in item.keys():
                    frame = item['frame']
                else:
                    frame = 'Sans cadre'
                
                available_frames = {key: value for key, value in frames.items() if item['number_photos'] >= value['min'] and item['number_photos'] <= value['max'] and item['text_len'] not in value['unavailable_sizes'] }
                if item['text_len'] > 10:
                    st.info('Votre mot fait plus de 10 photos. Contactez-moi pour un devis de cadre ou de sous-verre sur mesure')
                elif item['text_len'] < 3:
                    st.info("L'option de cadre en bois n'est pas disponible pour un mot de moins 3 lettres.")
                frame =  st.radio('Option: Cadre', available_frames.keys(), index=list(available_frames.keys()).index(frame), key=str(item_index) + "_radio_" + text)
                
                if 'frame' not in item.keys() or frame != cookie_manager.get(cookie='basket')[item_index]['frame']:
                    save_basket(basket, item_index, 'frame', frame)
                
                if 'bois' in frame and st.button('✨ Prévisualiser avec le cadre en qualité maximale', key=str(item_index) + "_preview_" + text):
                    
                    def preview_with_frame():       
                        bucket_name = 'fotomo'
                        urls = [create_presigned_url('fotomo', '/'.join(url.split('/')[3:])) for url in [l['letter_photo_path'] for l in text_list]]
                        images = [Image.open(BytesIO(requests.get(url).content)) for url in urls]
                        widths, heights = zip(*(i.size for i in images))
                        
                        interval = 300
                        total_width = sum(widths) + interval * (len(text_list) - 1)
                        max_height = max(heights)
                        background_color = 'rgb(225,225,225)'
                        frame_color = 'rgb(0,0,0)'
                        new_im = Image.new('RGB', (total_width, max_height), color=background_color)
                        x_offset = 0
                        for im in images:
                            new_im.paste(im, (x_offset, 0))
                            x_offset += interval + im.size[0]
                        with_background = ImageOps.expand(new_im,border=300,fill=background_color)
                        with_frame = ImageOps.expand(with_background,border=500,fill=frame_color)

                        return with_frame
                        
                    img = preview_with_frame()
                    st.image(img)
                
                if 'quantity' in item.keys():
                    quantity = item['quantity']
                else:
                    quantity = 1
                    
                quantity = int(st.number_input('Quantité:',min_value=1, value=quantity, key=str(item_index) + "_quantity_" + text))
                if 'quantity' not in item.keys() or quantity != cookie_manager.get(cookie='basket')[item_index]['quantity']:
                    save_basket(basket, item_index, 'quantity', quantity)
                
                            
                
                    




                    

                