import streamlit as st
from src.s3.list_photos import list_bucket

st.set_page_config(
	# layout = "centered",
    layout = "wide",
	initial_sidebar_state = "expanded",
	page_title = "Fotomo.fr",
    page_icon = "📷"
)


@st.cache
def load_letters():
    all_albums = list_bucket('s3://fotomo')
    letters = {}
    for photo in all_albums:
        album = photo['Key'].split('/')[0]
        if album not in ['Logos', 'Galerie']:
            if album not in letters.keys():
                letters[album] = []
            letters[album].append('https://fotomo.s3.amazonaws.com/' + photo['Key'])
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