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
	initial_sidebar_state = "expanded",
	page_title = "Mon panier",
    page_icon = "📷"
)

# Login
@st.cache(allow_output_mutation=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

basket = cookie_manager.get(cookie='basket')

if basket is None:
    st.warning('Votre panier est vide.')
else:
    st.subheader('Il y  a ' + str(len(basket)) + ' sélection(s) dans votre panier')
    if st.button('Passer commande'):
        st.success('Success')
    

@st.cache 
def load_full_word(urls):
    images = []
    for url in urls:
        # st.write('Téléchargement de', url.split('/')[-1], '...')
        with urllib.request.urlopen(urllib.parse.quote(url).replace('https%3A', 'https:')) as url:    
            # st.write(url)    
            img = Image.open(url)
        images.append(img)
    # st.write('Juxtaposition des photos...')
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height), color = (255,255,255))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += 100 +  im.size[0]
    return new_im
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    # min_shape = sorted( [(np.sum(i.size), i.size ) for i in images])[0][1]
    # imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in images ) )
    # imgs_comb = Image.fromarray( imgs_comb)
    # return imgs_comb
    
for item_index, item in enumerate(basket):
    word = ''.join([value['letter'] for key, value in item.items() if key != 'quantity'])
    
    with st.expander('#' +  str(item_index + 1)  + ' - ' + word, expanded = True if item_index== 0 else False):
        if st.button('🔎 Afficher le mot', key=str(item_index)) or item_index == 0:
            urls = [value['letter_photo_path'] for key, value in item.items() if key != 'quantity']
            new_im = load_full_word(urls)
            st.image(new_im, )
        
        if 'quantity' in item.keys():
            quantity = item['quantity']
        else:
            quantity = 1
        basket[item_index]['quantity'] = int(st.number_input('Quantité:', value=quantity, key=str(item_index) + "_"))
        
        
        cookie_manager.set('basket', basket, expires_at=datetime.datetime(year=2030, month=2, day=2), key=str(item_index) + '_quantity')            
        if st.button('❌ Supprimer du panier', key=str(item_index) + '_delete'):
            del basket[item_index]
            cookie_manager.set('basket', basket, expires_at=datetime.datetime(year=2030, month=2, day=2), key=str(item_index) + '_delete_' + word)            




            

        