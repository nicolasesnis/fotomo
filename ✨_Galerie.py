import streamlit as st
import os, json
from src.s3.list_photos import list_bucket

st.set_page_config(
	# layout = "centered",
    layout = "wide",
	initial_sidebar_state = "expanded",
	page_title = "Fotomo.fr",
    page_icon = "📷"
)

if 'secrets.json' in os.listdir(): # localhost
      with open('secrets.json', 'r')  as f:
        secrets = json.load(f)
else: # streamlit cloud
      secrets = st.secrets
  

st.success('Bienvenue sur Fotomo.fr! Le site est actuellement en cours de développement. Contactez-moi directement à valerie.esnis@fotomo.fr pour tout demande ou question.')
st.title('Galerie')

galerie = list_bucket('s3://fotomo/Galerie')
for photo in galerie:
    st.image('https://low-resolution-images.s3.amazonaws.com/' + photo['Key'],  caption=photo['Key'].split('/')[1].split('.')[0])
    
    