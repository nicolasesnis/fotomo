import streamlit as st
from streamlit.components.v1 import html
from src.components.basket import show_basket
from src.cookies.utils import get_manager
from src.components.checkout import create_checkout_session
from src.components.orders import save_new_order


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
    
    tab1, tab2 = st.tabs(["Mon Panier", "Valider mon panier (checkout)"])
    with tab1:
        st.subheader('Il y  a ' + str(len(basket)) + ' sélection(s) dans votre panier')
        show_basket(basket)
    with tab2:
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
            order_id = save_new_order(basket, cookies['user_cookie']['email'])
            out = create_checkout_session(client_email=cookies['user_cookie']['email'], order_id=order_id, basket=basket)
            st.markdown('<a href="' + out + '" target="_blank">Payer avec Stripe (nouvelle fenêtre)</a>', unsafe_allow_html=True)
