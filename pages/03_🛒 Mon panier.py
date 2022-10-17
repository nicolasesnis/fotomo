import streamlit as st
from streamlit.components.v1 import html
from src.components.basket import show_basket
from src.cookies.utils import get_manager

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
            st.write('Goo!')
            html("""            
                <script type="text/javascript">
                    function onVisaCheckoutReady() {
                        V.init({
                        apikey: '""" + st.secrets['visa_api_key'] + """',
                        encryptionKey: '""" + st.secrets['visa_encryption_key'] + """',
                        paymentRequest: {
                            currencyCode: "USD",
                            subtotal: "1.00",
                        },
                        });
                    }
                    V.on("payment.success", function (payment) {
                        alert(JSON.stringify(payment));
                    });
                    V.on("payment.cancel", function (payment) {
                        alert(JSON.stringify(payment));
                    });
                    V.on("payment.error", function (payment, error) {
                        alert(JSON.stringify(error));
                    });
                </script>
                <img
                    alt="Visa Checkout"
                    class="v-button"
                    role="button"
                    src="https://sandbox.secure.checkout.visa.com/wallet-services-web/xo/button.png"
                />
                <script
                    type="text/javascript"
                    src="https://sandbox-assets.secure.checkout.visa.com/checkout-widget/resources/js/integration/v1/sdk.js"
                ></script>
            """)
    