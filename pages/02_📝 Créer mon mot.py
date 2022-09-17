import streamlit as st
from src.s3.list_photos import list_bucket
from random import randrange


st.set_page_config(
	# layout = "centered",
    layout = "wide",
	initial_sidebar_state = "expanded",
	page_title = "Fotomo.fr",
    page_icon = "📷"
)


@st.cache
def load_letters():
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
    global letters_photos
    used_indices = [text_dict[key]['index'] for key in text_dict.keys() if text_dict[key]['letter'] == letter]
    if max(used_indices) + 1 < len(letters_photos[letter].keys()):
        return max(used_indices) + 1
    else:
        return randrange(len(letters_photos[letter].keys()))
    

def update_photo(letter, index):
    global letters_photos
    photo_name = list(letters_photos[letter])[index]
    return {
        'index': index,
        'letter_photo_name': photo_name,
        'letter_photo_path': letters_photos[letter][photo_name]['path']
    }

def func(text):
    st.write(text)
    
def set_allow_reset_text_dict():
    st.session_state['allow_reset_text_dict'] = True
    
text = st.text_input('Entrez un mot ou une phrase...', on_change=set_allow_reset_text_dict)

if 'allow_reset_text_dict' in st.session_state and  st.session_state['allow_reset_text_dict']:
    text_dict = {}
    for letter_index, letter in enumerate(list(text)):
        letter = letter.upper()
        if letter not in letters_photos.keys():
            continue
        if letter not in [text_dict[key]['letter'] for key in text_dict.keys()]:
            index  = 0
        else:
            index = get_next_index(letter, text_dict)
        text_dict[letter_index] = {'letter': letter}
        photo_name = list(letters_photos[letter])[index]
        text_dict[letter_index].update(
            update_photo(letter, index)
        )    
        if  text_dict != {}:
            st.session_state['text_dict'] = text_dict


if text != '':
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
                # header_html = '<img src="' + image + '" style="width: 50%; height: 50%"/>' 
                # st.markdown(
                #     header_html, unsafe_allow_html=True,
                # )

                
            else:
                st.write(letter)

if 'text_dict' in st.session_state:
    st.write('Photos sélectionnées:')
    st.write(st.session_state['text_dict'])

