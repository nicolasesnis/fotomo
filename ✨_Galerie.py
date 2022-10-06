import streamlit as st
import os, json
from src.s3.list_photos import list_bucket
from src.styles.utils import cta_button, sidebar_font_color, set_bg_pattern, hide_navbar

st.set_page_config(
    layout = "wide",
	initial_sidebar_state = "collapsed",
	page_title = "Fotomo.fr",
    page_icon = "📷"
)

set_bg_pattern()
hide_navbar()

with open('src/styles/custom_theme.json', 'r')  as f:
    custom_theme = json.load(f)


st.info('🚧 Bienvenue sur Fotomo.fr! Le site est actuellement en cours de construction. Contactez-moi directement à valerie.esnis@fotomo.fr pour tout demande ou question.')

with st.sidebar:
    
    # st.image('https://low-resolution-images.s3.amazonaws.com/Logos/logo.jpg')
    st.write("[![Insta](https://img.shields.io/badge/Fotomo-33-orange?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAIAAACRXR/mAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTExIDc5LjE1ODMyNSwgMjAxNS8wOS8xMC0wMToxMDoyMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTUgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjIwOUJGN0FEOUQ3RTExRTc5QjQxRTcyOEEwNjkyNjc1IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjIwOUJGN0FFOUQ3RTExRTc5QjQxRTcyOEEwNjkyNjc1Ij4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MjA5QkY3QUI5RDdFMTFFNzlCNDFFNzI4QTA2OTI2NzUiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6MjA5QkY3QUM5RDdFMTFFNzlCNDFFNzI4QTA2OTI2NzUiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz44A/5kAAAQpElEQVR42qRZ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)](https://www.instagram.com/valerie_esnis/)")
    st.write("[![Facebook](https://img.shields.io/badge/Val%C3%A9rie%20Esnis-Fotomo-blue?labelColor=ffffff&logo=data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxANEBAQDgsQDxUPEhwQERAODQ8NFRAOFR0bHxYbFx8aHC8gGSYrGx8fJD0tMTUxLjY1Fys/ODMsRTEtLjUBCgoKDg0OGxAQFysgHR0rKy4tLi0tKy0tLSsrKystKy0rKy0tLS0tLTcrKystLjMtLTc4Ny0tKzgtKzItKys3N//AABEIAEsASwMBEQACEQEDEQH/xAAcAAEAAgIDAQAAAAAAAAAAAAAAAwcEBgEFCAL/xAA0EAABAwMBAwkHBQEAAAAAAAABAAISAwQRMQUGByEjMkFyc5GxsiIkQlFhcYElNKHB0RT/xAAbAQEAAgMBAQAAAAAAAAAAAAAABQYBAgMEB//EACQRAQACAgEEAgIDAAAAAAAAAAABAgMRBQQhMTISQTRRFCIz/9oADAMBAAIRAxEAPwDIyrq+fGUDKBlAysHkyshlYNGVkMrAZQRyWWxJAkgSQAc6JMxEd2YiZnUM+lse6eMttKpHYIXmnq8NZ72emvRZrRuKorjZ9ekM1LeowDUuY4DxW1Oox3nVbNL9Nlp3tDFkvQ4ElgJIIpLZsSQJIxpxJY8MxG1lbm7AZRpMrVGA1KgkJDMGnQBVvr+rtkvNaz2hZ+P6KtKfO0d5bQo1K9nS75Ef8Vf7D1Bezof96vDyGv49lUSVrVEkgSQQTWW2iaGiaGn3SOXNHzIHitcnrLbHG7QvOm3AAHUFSrTuV3pGqxDTOIW2atA0qNKoacwXOc04JGgGepS3F9NTJu1u+kRynU3x6rVodS+qvBDq9RwOodUcQf5U7XBSs7iEFbLe0amUEl005EkNE0NIZLZs4khplbNs33VVtGkAXPzjJwOQZ/pcs2WuKk2t9OuLDbJb41+2w0dx74OaSynyEE86NB+FHX5TDNdbe+nGZonelqBVtY48aaZvxu7cXtWm+g1hDGRMnx5c5Urx/V48FZi32i+Q6TJntE1+mn7V3XurOmatZrA0EDkqSOSpfD1+LLb41lE5uhyYq/KzpJr3PFokhomhpBNZb6Joad/uI79Qt/u70leDkvx5ezoI1nhc2fqqmtO4EZEY3ppPFO5jbUmZ6dXP4aD/AKFLcTj3lmf0iuUvHwiP2rCasulf0TQ0TQ0hktm2iSGnLKpacgkEdYJBWJiJZjcMm2vKk2c8/pD43fNccmKnwns60yW+Ud3oEaBUmVtr4VjxVuHsuKAa9zeaPRcW/F9FP8PSLVttCcpeYtGmi1Lhzuk9zsaScXY8VORjivhEzabeXxJbNdEk0aJJo0hksttEkNEkY0ltne2ztDzXPL6S6Y4/tD0Y3QKiz5W2viFV8XT7zb90fUrFwvrZC8p7Q0KSnESSQ0SQJII8rLJlAygltT7bO2PNc8npLpj9oekBoFRJ8rZXwqjjAfebfuj6irFwnrZCcn7Q0HKnUUZQMoGUHwsthByjCS16bO2PNc8vpLfH7Q9JjQKhz5WyvhU/GL9zb90fUVY+E9bIXk/aFfqdRYgICD//2Q==)](https://www.facebook.com/profile.php?id=100085408903046)")
    st.write('📧 valerie.esnis@fotomo.fr')
    st.write('📞 +33 6 12 59 34 57')
    
st.markdown("<h1 style='text-align: center; font-size: 5em; margin-bottom: -50px'>Fotomo</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-style: italic'>Les mots en photo</h2>", unsafe_allow_html=True)
st.write('')
st.write('')
st.write('')
st.markdown("""<p style='text-align: center; font-size: 1.2em; font-family: "Georgia", Times, serif;'>Mes lettres sont à votre disposition pour écrire le mot de votre choix et l’offrir à ceux que vous aimez.</p>""", unsafe_allow_html=True)
cta_button("Créer mon mot", custom_theme['colorPaletteLightGreen'], 'https://fotomo.streamlitapp.com/Créer_mon_mot')

st.write('')
st.subheader('*Galerie*')

galerie = list_bucket('s3://fotomo/Galerie')

st.markdown(
    """
    <style>
    #photos {
        line-height: 0;
            -webkit-column-count: 2;
            -webkit-column-gap:   3px;
            -moz-column-count:    2;
            -moz-column-gap:      3px;
            column-count:         2;
            column-gap:           3px;  
        }

    #photos img {
        padding: 20px;
        width: 100% !important;
        height: auto !important;
    }
    @media (max-width: 1200px) {
        #photos {
            -moz-column-count:    2;
            -webkit-column-count: 2;
            column-count:         2;
        }
    }
    @media (max-width: 1000px) {
        #photos {
            -moz-column-count:    2;
            -webkit-column-count: 2;
            column-count:         2;
        }
    }
    @media (max-width: 800px) {
        #photos {
            -moz-column-count:    1;
            -webkit-column-count: 1;
            column-count:         1;
        }
    }
    @media (max-width: 400px) {
        #photos {
            -moz-column-count:    1;
            -webkit-column-count: 1;
            column-count:         1;
        }
    }
    </style>
    <section id="photos">""" + ''.join([
        "<img src = 'https://low-resolution-images.s3.amazonaws.com/" + photo['Key'] + "' alt= '" + photo['Key'].split('/')[1].split('.')[0] + "'/>" 
        for photo in galerie]) + """
    </section>
    """,
    unsafe_allow_html=True
    )
