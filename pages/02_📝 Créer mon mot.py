import streamlit as st
import datetime
from src.s3.list_photos import list_bucket
from random import randrange
from src.cookies.utils import get_manager

st.set_page_config(
    layout = "wide",
	page_title = "Créer mon mot",
    page_icon = "📷"
)

cookie_manager = get_manager()

@st.cache
def load_letters():
    """
    Loads all the letter images from S3.
    """
    all_albums = list_bucket('s3://low-resolution-images')
    letters = {}
    for photo in all_albums:
        album = photo['Key'].split('/')[0]
        if album not in ['Logos', 'Galerie'] and photo['Key'].split('/')[1] != "":
            if album not in letters.keys():
                letters[album] = {}
            letters[album][photo['Key'].split('/')[1].split('.')[0]] = {'path': 'https://low-resolution-images.s3.amazonaws.com/' + photo['Key']}
    return letters 
letters_photos = load_letters()


def get_next_index(letter, text_dict):
    """
    Return the last available photo index, to avoid showing the same picture twice.
    """
    global letters_photos
    used_indices = [text_dict[key]['index'] for key in text_dict.keys() if text_dict[key]['letter'] == letter]
    if max(used_indices) + 1 < len(letters_photos[letter].keys()):
        return max(used_indices) + 1
    else:
        return randrange(len(letters_photos[letter].keys()))
    

def update_photo(letter, index):
    global letters_photos
    if letter in letters_photos:
        photo_name = list(letters_photos[letter])[index]
        return {
            'index': index,
            'letter_photo_name': photo_name,
            'letter_photo_path': letters_photos[letter][photo_name]['path']
        }
    else: # special char or space
        return {
            'index': index,
            'letter_photo_name': letter,
            'letter_photo_path': None
        }
    

st.info("📷 Pour protéger mes photos, les lettres s'affichent en moindre qualité. Passez commande de votre mot pour recevoir les photos imprimées professionnellement en format 10 x 15 cm, finition brillante, sur papier Fujifilm épais (210 g/m2).")
st.info("🏷️ 5€ par photo (4,50 € si 10 photos ou plus sont sélectionnées)")

def set_allow_reset_text_dict():
    """ 
    Allow the reset of the text dict. Avoids resetting the text_dict each time a single photo is edited.
    """
    st.session_state['allow_reset_text_dict'] = True

initial_value = '' if 'text_dict' not in st.session_state else ''.join([value['letter'] for key, value in  st.session_state['text_dict'].items() if type(value) == dict])
text = st.text_input('Entrez un mot ou une phrase...', value=initial_value,  on_change=set_allow_reset_text_dict)

def set_text_dict():
    """ 
    Update the text_dict object with new input word
    """
    text_dict = {}
    for letter_index, letter in enumerate(list(text)):
        letter = letter.upper()
        if letter not in letters_photos.keys():
            if letter_index == len(list(text)) - 1 and text_dict == {}:
                st.error('Veuillez entrer au moins 1 charactère alphabétique.')
                break
            index  = 0
        elif letter in [text_dict[key]['letter'] for key in text_dict.keys()]:
            index = get_next_index(letter, text_dict)
        else:
            index  = 0
        text_dict[letter_index] = {'letter': letter}
        text_dict[letter_index].update(
            update_photo(letter, index)
        )    
        
        if  text_dict != {}:
            st.session_state['text_dict'] = text_dict

if 'allow_reset_text_dict' in st.session_state and st.session_state['allow_reset_text_dict']:
    set_text_dict()
    
if text != '' and 'text_dict' in st.session_state:
    cols = st.columns(len(list(text)), gap='small')
    for letter_index, col in enumerate(cols):
        letter = list(text)[letter_index].upper()
        with col:  
            if letter in letters_photos.keys():
                if st.button('Changer',  key = str(letter_index)):
                    st.session_state['allow_reset_text_dict'] = False
                    index = get_next_index(letter, st.session_state['text_dict'])
                    st.session_state['text_dict'][letter_index].update(update_photo(letter, index))
                image = st.session_state['text_dict'][letter_index]['letter_photo_path']
                st.image(image, use_column_width='auto')                
            else:
                st.write(letter)

    basket = cookie_manager.get('basket')
    st.session_state['basket'] = basket if basket else []
    
    def add_to_cart(item):
        
        id = '_'.join([value['letter_photo_path'] for key, value in item.items() if value['letter_photo_path'] is not None])
        if len([item for item in st.session_state['basket'] if ('id' in item and item['id'] == id)]) == 0:
            item['number_photos'] = len([value for key, value in item.items() if value['letter_photo_path'] is not None])
            item['text'] = text
            item['text_len'] = len(text)
            item['id'] = id
            st.session_state['basket'].append(st.session_state['text_dict'])
            st.session_state['atc_message'] = 'Les photos ont été ajoutées au panier - [Mon panier](https://fotomo.streamlitapp.com/Mon_panier)'
            cookie_manager.set('basket', st.session_state['basket'], expires_at=datetime.datetime(year=2030, month=2, day=2), key='basket')            
        else:
            st.session_state['atc_message'] = 'Cette combinaison de photos est déjà dans votre panier.'
    
    if st.button('Ajouter au panier', disabled=text == ''):    
        add_to_cart(item = st.session_state['text_dict'])
        
    if 'atc_message' in st.session_state:
        st.success(st.session_state['atc_message'])
