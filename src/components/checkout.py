
import json
import stripe
import streamlit as st
from src.stripe.utils import load_product_prices

# This is your test secret API key.

def create_checkout_session(client_email, order_id, basket=None): 
    try:
        if basket:
            products, prices = load_product_prices()
            photo_product_ids = [p for p in products if 'type' in p['metadata'] and p['metadata']['type'] == 'photo']
            regular_photo_id = [p['id'] for p in photo_product_ids if p['metadata']['pricing'] == 'regular']
            regular_price = [p['id'] for p in prices if p['product'] == regular_photo_id[0]][0] 
            discount_photo_id = [p['id'] for p in photo_product_ids if p['metadata']['pricing'] == 'discount']
            discount_price = [p['id'] for p in prices if p['product'] == discount_photo_id[0]][0] 
            total_number_photos = sum([i['number_photos'] * i['quantity'] for i in basket])
            line_items = []
            
            for item in basket:
                if total_number_photos < 10:
                    line_items.append({'price': regular_price, 'quantity': item['number_photos']*item['quantity']})
                else:
                    line_items.append({'price': discount_price, 'quantity': item['number_photos']*item['quantity']})
                if item['frame'] != 'Sans Cadre':
                    frame_id = [p['id'] for p in products if p['name'] == item['frame']]
                    frame_price  = [p['id'] for p in prices if p['product'] == frame_id[0]][0] 
                    line_items.append({'price': frame_price, 'quantity': item['quantity']})
            # for item in line_items:
            #     item['adjustable_quantity'] = {'enabled': True}
        else: # test
            line_items= [{'price': 'price_1LuPgHGY9GmA5aoItriIcZEZ', 'quantity': 1}]

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url='https://fotomo.fr/Mon_Compte?order_id=' + order_id,
            cancel_url='https://fotomo.fr/Mon_panier',
            metadata = {'order_id': order_id},
            client_reference_id = client_email,
            billing_address_collection='required',
            shipping_address_collection={'allowed_countries': ['FR']},
            shipping_options=[{'shipping_rate': 'shr_1LuQ5iGY9GmA5aoIMrYzMy0O' if basket else 'shr_1LuPynGY9GmA5aoIw6bXkeLt'}],
            locale='fr'
        )
    except Exception as e:
        st.error(e)
        return str(e)

    return checkout_session.url

