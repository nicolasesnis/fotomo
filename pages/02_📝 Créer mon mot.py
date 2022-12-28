import streamlit as st
from streamlit_image_select import image_select
import os
import datetime
from random import randrange
from src.cookies.utils import get_manager

st.set_page_config(
    layout = "wide",
	page_title = "Créer mon mot",
    page_icon = "📷",
    initial_sidebar_state='collapsed'
)

cookie_manager = get_manager()

@st.cache
def load_letters():
    all_albums = os.listdir('images/low-resolution-images')
    letters = {}
    for album in all_albums:
        for photo in os.listdir('images/low-resolution-images/' + album):
            if album not in letters.keys():
                letters[album] = {}
            letters[album][photo.split('.')[0]] = {'path': 'images/low-resolution-images/' + album + '/' + photo}
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
    
    
st.title('Créer mon mot 📝')
st.info("📷 Pour protéger mes photos, les lettres s'affichent en moindre qualité. Passez commande de votre mot pour recevoir les photos imprimées professionnellement en format 10 x 15 cm, finition brillante, sur papier Fujifilm épais (210 g/m2).")
st.info("🏷️ 5€ par photo (4,50 € si 10 photos ou plus sont sélectionnées)")


initial_value = '' if 'text_dict' not in st.session_state else ''.join([value['letter'] for key, value in  st.session_state['text_dict'].items() if type(value) == dict])

def set_text_dict():
    """ 
    Update the text_dict object with new input word
    """
    text_input = st.session_state['text_input']
    text_dict = {}
    for letter_index, letter in enumerate(list(text_input)):
        letter = letter.upper()
        if letter not in letters_photos.keys():
            if letter_index == len(list(text_input)) - 1 and text_dict == {}:
                st.error('Veuillez entrer au moins 1 charactère alphabétique.')
                break
            index  = 0
        elif letter in [text_dict[key]['letter'] for key in text_dict.keys()]:
            index = get_next_index(letter, text_dict)
        else:
            index  = 0
        if letter in letters_photos:
            photo_name = list(letters_photos[letter])[index]
            text_dict[letter_index] = {
                'letter': letter,
                'index': index,
                'letter_photo_name': photo_name,
                'letter_photo_path': letters_photos[letter][photo_name]['path']
            }
        else: # special char or space
            text_dict[letter_index] = {
                'index': index,
                'letter_photo_name': letter,
                'letter_photo_path': None
            }
            
        if  text_dict != {}:
            st.session_state['text_dict'] = text_dict
            
text_input = st.text_input('Entrez un mot ou une phrase...', value=initial_value,  on_change=set_text_dict, placeholder='Pierre, Bretagne, Bienvenue...', key='text_input')
if len(text_input) > 0:
    cols = st.columns(len(list(text_input)), gap='small')

def display_letter_image(letter_photo_path, letter_index, letter):
    with cols[letter_index]: 
        st.image(letter_photo_path, use_column_width='auto')     
        if st.button('Changer',  key = str(letter_index)):
            st.session_state['edit_letter'] = {'letter_index': letter_index, 'letter': letter}           
            # index = get_next_index(letter, st.session_state['text_dict'])
            # st.session_state['text_dict'][letter_index].update(update_photo(letter, index))
    
def display_word(text_dict):
    for letter_index, col in enumerate(cols):
        letter = list(text_input)[letter_index].upper()
        if letter in letters_photos.keys():
            display_letter_image(text_dict[letter_index]['letter_photo_path'], letter_index, letter)
        else:
            st.write(letter)
    
if text_input != '' and 'text_dict' in st.session_state:
    display_word(st.session_state['text_dict'])
    

    basket = cookie_manager.get('basket')
    st.session_state['basket'] = basket if basket else []
    
    def add_to_cart(item):
        id = '_'.join([value['letter_photo_path'] for key, value in item.items() if len(str(key)) < 3 and value['letter_photo_path'] is not None])
        if len([item for item in st.session_state['basket'] if ('id' in item and item['id'] == id)]) == 0:
            item['number_photos'] = len([value for key, value in item.items() if len(str(key)) < 3 and value['letter_photo_path'] is not None])
            item['text'] = text_input
            item['text_len'] = len(text_input)
            item['id'] = id
            st.session_state['basket'].append(st.session_state['text_dict'])
            st.session_state['atc_message'] = 'Les photos ont été ajoutées au panier'
            cookie_manager.set('basket', st.session_state['basket'], expires_at=datetime.datetime(year=2030, month=2, day=2), key='basket')            
        else:
            st.session_state['atc_message'] = 'Cette combinaison de photos est déjà dans votre panier.'
    
    def display_image_select(letter_index, letter):
        with st.expander('Choisir une photo pour la lettre ' +  letter, expanded=True):
            all_letter_pics = []
            letter_dir_path = 'images/low-resolution-images/' + letter + '/'
            for photo in os.listdir(letter_dir_path):
                all_letter_pics.append(letter_dir_path + photo)
            new_letter_photo_path = image_select(
                label="",
                images=all_letter_pics,
                captions=[a.split('/')[-1].split('.')[0] for a in all_letter_pics]
            )
            if new_letter_photo_path != st.session_state['text_dict'][letter_index]['letter_photo_path']:
                st.session_state['text_dict'][letter_index]['letter_photo_path'] = new_letter_photo_path
                st.experimental_rerun()
                
    if 'edit_letter' in st.session_state:
        display_image_select(st.session_state['edit_letter']['letter_index'], st.session_state['edit_letter']['letter'])
        
        
    if st.button('Ajouter au panier', disabled=text_input == ''):    
        add_to_cart(item = st.session_state['text_dict'])
        
    if 'atc_message' in st.session_state:
        st.success(st.session_state['atc_message'])
        if st.session_state['atc_message'] == 'Les photos ont été ajoutées au panier':
            st.write('<a href="https://fotomo.fr/Mon_panier" target="_self">Voir mon panier</a>', unsafe_allow_html=True)