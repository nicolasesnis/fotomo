import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
	# layout = "centered",
    layout = "wide",
	initial_sidebar_state = "expanded",
	page_title = "Fotomo.fr",
    page_icon = "📷"
)


st.title('Fotomo')

components.html(height=10000, scrolling=True, html="""
<script
  type="text/javascript"
  src="https://unpkg.com/instafeed.js@2.0.0-rc2/src/instafeed.js"
></script>

<div id="instafeed"></div>

<script type="text/javascript">
  var feed = new Instafeed({
    accessToken: "token",
    template:'<a href="{{link}}"><img style="max-width: 200px; max-height: 200px" title="{{caption}}" src="{{image}}" /></a>'
  });
  feed.run();
</script>
""")