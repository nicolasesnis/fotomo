import stripe
import streamlit as st


stripe.api_key = st.secrets['stripe_live_secret']

def load_product_prices():    
    products = list(stripe.Product.list(limit=999))
    prices = list(stripe.Price.list(limit=999))
    return  products, prices

products, prices  = load_product_prices()

def get_product_price(attr):
    for key, value in attr.items():
        product_id = [p['id'] for p in products if key in p['metadata'] and p['metadata'][key] == value]
    price = [p['unit_amount'] for p in prices if p['product'] == product_id[0]][0] / 100
    return price