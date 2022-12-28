import streamlit as st
import extra_streamlit_components as stx
import datetime
from PIL import Image ,ImageOps
import requests
from io import BytesIO
from src.s3.read_file import create_presigned_url
from src.stripe.utils import get_product_price, load_product_prices
import numpy as np


Image.MAX_IMAGE_PIXELS = 10000000000

@st.cache(allow_output_mutation=True)
def get_manager():
    return stx.CookieManager()

def save_basket(basket, item_index, cookie_manager, text, new = None):
    if new:
        for key, value in new.items():
            basket[item_index][key] = value
    cookie_manager.set('basket', 
                       basket, 
                       expires_at=datetime.datetime(year=2030, month=2, day=2), 
                       key=str(item_index) + '_' + text + '_' + str(new))            
    return basket


    
def get_prices(basket):
    for item_index, item in enumerate(basket):
        if item['number_photos'] < 10:
            basket[item_index]['price'] = get_product_price({'type': 'photo', 'pricing': 'regular'})  * item['number_photos']
        else:
            basket[item_index]['price'] = get_product_price({'type': 'photo', 'pricing': 'discount'})  * item['number_photos']
        if 'frame_price' in item:
            basket[item_index]['price'] += item['frame_price']
        if 'quantity' in item:
            basket[item_index]['price'] = item['price'] * item['quantity']
        

# @st.cache(ttl=60, suppress_st_warning=True)
def preview_with_frame(text_list):       
    background_color = '#FFFFFF'
    frame_color = 'rgb(0,0,0)'
    
    urls = []
    for url in [l['letter_photo_path'] for l in text_list]:
        if url:
            # url = 'https://images.fotomo.fr/' + url
            # url = create_presigned_url('fotomo', '/'.join(url.split('/')[3:]))
            url = url.replace('low-resolution-images', 'letters')
        else:
            url = None
        urls.append(url)
    images = []
    for url in urls:
        if url:
            # images.append(Image.open(BytesIO(requests.get(url).content), timeout=9999999))
            images.append(Image.open(url))
        else:
            last_size = images[-1].size
            img = Image.new('RGB', (last_size[0],last_size[1]) , background_color) 
            images.append(img)
    
    widths, heights = zip(*(i.size for i in images))
    
    interval = 300
    total_width = sum(widths) + interval * (len(text_list) - 1)
    max_height = max(heights)
    
    new_im = Image.new('RGB', (total_width, max_height), color=background_color)
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += interval + im.size[0]
    with_background = ImageOps.expand(new_im,border=300,fill=background_color)
    with_frame = ImageOps.expand(with_background,border=500,fill=frame_color)
    with_frame_white = ImageOps.expand(with_frame,border=100,fill=background_color)

    return with_frame_white

def get_frames():
    products, prices  = load_product_prices()
    frames = [p for p in products if 'type' in p['metadata'] and p['metadata']['type'] == 'frame']
    frames = [{'name': p['name'], 'number_photos': int(p['metadata']['number_photos']), 'description': p['description'], 'id': p['id'], 'image': p['images'][0]} for p in frames]
    for f in frames:
        f['price'] = [p['unit_amount'] for p in prices if p['product'] == f['id']][0] / 100
    frames.append({'name': 'Sans Cadre', 'description': '', 'number_photos': 999, 'price': 0, 'image': ''}) 
    return  frames

def show_basket(basket):
    
    non_letter_keys = ['quantity', 'frame', 'price', 'text', 'number_photos', 'text_len', 'id', 'frame_price']
    cookie_manager = get_manager()
    frames = get_frames()
    get_prices(basket)
    
    st.write('Sous-total avant les frais de livraison : __' +  str(sum([item['price'] for item in basket])) + '__ €')
    
    st.info('Les photos sont imprimées professionnellement en format 10 x 15 cm, finition brillante, sur papier Fujifilm épais (210 g/m2).')
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
                basket = save_basket(basket=basket, item_index=item_index, cookie_manager=cookie_manager, text=text)
            
            available_frames = [frame for frame in frames if item['text_len'] == frame['number_photos'] or frame['number_photos'] == 999 ]
            
            if 'frame' in item.keys():
                frame = item['frame']
            else:
                frame = available_frames[0]['name']
            
            if item['text_len'] > 10:
                st.info('Votre mot fait plus de 10 photos. Contactez-moi pour un devis de cadre ou de sous-verre sur mesure')
            elif item['text_len'] < 3:
                st.info("L'option de cadre en bois n'est pas disponible pour un mot de moins 3 lettres.")
            if len(available_frames) == 0:
                st.info('Pas de cadre disponible pour les photos choisies. Contactez-moi pour un devis de cadre ou de sous-verre sur mesure.')
            
            
            col1, col2, col3 = st.columns([4,2,5])
            # with col1:
            frame =  st.selectbox('Option: Cadre', [f['name'] + ' (+ ' + str(f['price']) + ' €)' for f in available_frames], index=[f['name'] for f in available_frames].index(frame), key=str(item_index) + "_radio_" + text)
            frame = frame.split(' (')[0] # remove price
            if frame != 'Sans Cadre':
                st.info([f['description'] for f in frames if f['name'] == frame][0])
            # with col2:
            #     if frame != 'Sans Cadre':
            #         st.image([f['image'] for f in frames if f['name'] == frame][0])
            
            if 'bois' in frame and st.button('✨ Prévisualiser avec le cadre en qualité maximale', key=str(item_index) + "_preview_" + text):
                img = preview_with_frame(text_list)
                st.image(img)
            
            if 'frame' not in item.keys() or (frame != item['frame']):
                basket = save_basket(basket=basket, item_index=item_index, cookie_manager=cookie_manager, text=text, new={
                    'frame_price':[f['price'] for f in available_frames if f['name'] == frame][0],
                    'frame':frame
                    })
                
            if 'quantity' in item.keys():
                quantity = item['quantity']
            else:
                quantity = 1
            quantity = int(st.number_input('Quantité:',min_value=1, value=quantity, key=str(item_index) + "_quantity_" + text))
            if 'quantity' not in item.keys() or (quantity != item['quantity']):
                basket = save_basket(basket=basket, item_index=item_index, cookie_manager=cookie_manager, text=text, new={'quantity': quantity})
            
            
                
            
                        
            
                




                

            