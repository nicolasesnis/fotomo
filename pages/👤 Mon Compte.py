import streamlit as st
import extra_streamlit_components as stx
import datetime

st.set_page_config(
	# layout = "centered",
    layout = "wide",
	initial_sidebar_state = "expanded",
	page_title = "Fotomo.fr",
    page_icon = "📷"
)


st.title('Fotomo')


# Login

@st.cache(allow_output_mutation=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookies = cookie_manager.get_all()

def end_session():
    cookie_manager.delete('login')

# if 'login' not in cookies:
cookie_manager.set('token', '123', expires_at=datetime.datetime(year=2030, month=2, day=2))
token = cookie_manager.get('token')
st.write(token)
