
import streamlit as st
import extra_streamlit_components as stx
import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_manager(key=generate_random_string(12)):
    return stx.CookieManager(key)