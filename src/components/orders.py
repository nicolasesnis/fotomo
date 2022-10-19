import streamlit as st 
import pandas as pd
import json
from src.s3.upload_file import upload_s3_file
from src.s3.read_file import read_s3_df_file
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
    with open(basket['id'] + '.json', 'w') as f:
        json.dump(basket, f, indent=4)
    upload_s3_file(basket['id'] + '.json', 's3://fotomo-secrets/orders/' + basket['id'] + '.json')    
    os.remove(basket['id'] + '.json')
    all_orders = read_s3_df_file('s3://fotomo-secrets/orders/all_orders.csv')
    all_orders.loc[len(all_orders)] = [email, basket['id'], str(pd.to_datetime('today').date()), basket['price'], 'Paiement reçu/Commande reçue']
    all_orders.to_csv(basket['id'] + '.csv', index=None)
    upload_s3_file(basket['id'] + '.csv', 's3://fotomo-secrets/orders/all_orders.csv')    
    os.remove(basket['id'] + '.csv')
    with a:
        st.write('')
    return basket['id']
    
    
