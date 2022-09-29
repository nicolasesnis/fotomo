import streamlit as st
import base64

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         [data-testid="stHeader"]  {{
          background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
        }}
         </style>
         """,
         unsafe_allow_html=True
     )
    
def sidebar_bg(side_bg):
    
   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )

def sidebar_bg_color(color):
    
   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background-color: """ + color + """;
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
   
def cta_button(text):
    st.markdown("""
<style type="text/css">
.btn-1{
  width: 300px;
  height: 150px;
  display: flex;
  margin: auto;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.btn-1 a
{
  text-decoration: none;
  border: 2px solid #010100;
  padding: 15px;
  color: #000;
  text-transform: uppercase;
  letter-spacing: 2px;
  position: relative;
  display: inline-block;
}

span {
  position: relative;
  /* z-index coz when we put bg to before and after this span text will not be visible */
  z-index: 3;
}

.btn-1 a::before {
  content: "";
  position: absolute;
  top: 5px;
  left: -2px;
  width: calc(100% + 6px);
  /*100% plus double the times left values*/
  height: calc(100% - 10px);
  background-color: #F0FFFF;
  transition: all 0.5s ease-in-out;
  transform: scaleY(1);
}

.btn-1 a:hover::before,
.btn-2 a:hover::before {
  transform: scaleY(0);
}

.btn-1 a::after {
  content: "";
  position: absolute;
  left: 5px;
  top: -5px;
  width: calc(100% - 10px);
  /*100% plus double the times left values*/
  height: calc(100% + 10px);
  background-color: #F0FFFF;
  transition: all 0.5s ease-in-out;
  transform: scaleX(1);
}

.btn-1 a:hover::after {
  transform: scaleX(0);
}

</style>
  
<div class="btn-1">
<a target=_self href='https://nicolasesnis-fotomo--galerie-ehy3aw.streamlitapp.com/Cr%C3%A9er_mon_mot' style='text-align: center' href=""><span >""" + text+ """</span></a>
</div>

    """, unsafe_allow_html=True)
    



