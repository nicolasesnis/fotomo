import streamlit as st
from streamlit.components.v1 import html
from src.components.basket import show_basket
from src.cookies.utils import get_manager
from src.components.checkout import create_checkout_session



st.set_page_config(
        layout = "wide",
        page_title = "Mon panier",
        page_icon = "📷"
    )

from src.components.login import login, register



cookie_manager = get_manager()

cookies = cookie_manager.get_all()

if 'basket' in cookies:
    basket = cookies['basket']
else:
    basket = None

if basket is None or len(basket) == 0:
    st.info('Votre panier est vide ! Dirigez-vous vers la section "Créer mon mot" pour effectuer une sélection.')
else:
    
    col1, col2 = st.columns([3,1])
    with col1:
        st.subheader('Il y  a ' + str(len(basket)) + ' sélection(s) dans votre panier')
    with col2:
        st.write('')
        checkout = st.button('Valider le panier ✅ ')
    if not checkout:
        show_basket(basket)
    else:
        if 'user_cookie' not in cookies: # User is not logged in
            st.write('Veuillez créer un compte ou vous connecter afin de continuer.')
            tab1, tab2 = st.tabs(["Client existant", "Nouveau Client"])
            # Existing User - Login Form
            with tab1:
                login()
            # Register Form                    
            with tab2:
                register()
        else:
            out = create_checkout_session(client_email=cookies['user_cookie']['email'], basket=basket)
            st.markdown('<a href="' + out + '" target="_blank">Payer avec Stripe</a>', unsafe_allow_html=True)
