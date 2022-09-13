import streamlit as st
import streamlit.components.v1 as components
import os, json

st.set_page_config(
	# layout = "centered",
    layout = "wide",
	initial_sidebar_state = "expanded",
	page_title = "Fotomo.fr",
    page_icon = "📷"
)


secrets = st.secrets
  


def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://drive.google.com/uc?export=view&id=1DHb3O60Yi26sb6vhg1mxdM1IU0cCpefr);
                background-size: 80%;
                background-repeat: no-repeat;
                padding-top: 90px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
add_logo()
st.title('Fotomo')

components.html(height=1000, scrolling=True, html="""
<script
  type="text/javascript"
  src="https://unpkg.com/instafeed.js@2.0.0-rc2/src/instafeed.js"
></script>

<div id="instafeed"></div>

<script type="text/javascript">
  var feed = new Instafeed({
  accessToken: '""" + secrets["instagram_user_token"] + """"',
  template:
    '<a href="{{link}}" target="_blank"><img style="max-height: 300px" title="{{caption}}" src="{{image}}" /></a>',
  transform: function (item) {
    //Transform receives each item as its argument
    // Over-write the original timestamp
    console.log(item)
    // return the modified item
    return item;
  },
});
feed.run();
</script>
""")