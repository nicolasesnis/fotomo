import streamlit as st
import os, json
from src.google_photos.utils import list_albums, list_album_photos


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
  


# def add_logo():
#     st.markdown(
#         """
#         <style>
#             [data-testid="stSidebarNav"] {
#                 background-image: url(https://drive.google.com/uc?export=view&id=1DHb3O60Yi26sb6vhg1mxdM1IU0cCpefr);
#                 background-size: 80%;
#                 background-repeat: no-repeat;
#                 padding-top: 90px;
#                 background-position: 20px 20px;
#             }
#             [data-testid="stSidebarNav"]::before {
#                 content: "";
#                 margin-left: 20px;
#                 margin-top: 20px;
#                 font-size: 30px;
#                 position: relative;
#                 top: 100px;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
# add_logo()


st.success('Bienvenue sur Fotomo.fr! Le site est actuellement en cours de développement. Contactez-moi directement à valerie.esnis@fotomo.fr pour tout demande ou question.')
st.title('Galerie')


all_albums = list_albums()
album_id = all_albums.loc[all_albums.title == 'Galerie', 'id'].values[0]
photos = list_album_photos(album_id, size='original')

for index, row in photos.iterrows():  
  st.image(row.baseUrl,  caption=row.filename.split('.')[0])