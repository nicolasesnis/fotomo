from json import load
import streamlit as st
from src.google_photos.utils import list_albums, list_album_photos

st.set_page_config(
	# layout = "centered",
    layout = "wide",
	initial_sidebar_state = "expanded",
	page_title = "Fotomo.fr",
    page_icon = "📷"
)



# @st.cache
def load_letters():
    all_albums = list_albums()
    letters = {}
    for index, album in all_albums.iterrows():
        if album.title not in ['Logos', 'Galerie']:

            photos = list_album_photos(album.id, size=None)
            letters[album.title] = photos.baseUrl
    return letters 
letters = load_letters()

text = st.text_input('Entrez un mot ou une phrase...')
if text != '':
    cols = st.columns(len(list(text)))
    for letter_index, col in enumerate(cols):
        letter = list(text)[letter_index].upper()
        with col:  
            if letter in letters.keys():
                photo_index = st.number_input('', min_value=0, max_value=len(letters[letter]) -1, key=str(letter_index))
                image = letters[letter][photo_index]
                st.image(image, use_column_width='auto')
                
            else:
                st.write(letter)