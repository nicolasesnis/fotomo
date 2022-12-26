import streamlit as st 
import pandas as pd
import json
import os 

def save_new_order(basket, email):
    a = st.empty()
    with a:
        st.write('Création de la commande...')
    basket = {'item_' + str(i): j for i, j in enumerate(basket)}
    basket['price'] = sum([value['price'] for key, value in basket.items()])
    basket.update({
        'email': email,
        'purchase_time': str(pd.to_datetime('now', utc=True)),
        'payment_confirmed': False,
        'id': email + '_'   + str(pd.to_datetime('now', utc=True)),
    })
    with open('orders/' + basket['id'] + '.json', 'w') as f:
        json.dump(basket, f, indent=4)
    all_orders = pd.read_csv('orders/all_orders.csv')
    all_orders.loc[len(all_orders)] = [email, basket['id'], str(pd.to_datetime('today').date()), basket['price'], 'Paiement reçu/Commande reçue']
    all_orders.to_csv('orders/all_orders.csv', index=None)
    with a:
        st.write('')
    return basket['id']
    
    
