import streamlit as st

st.set_page_config(
    layout = "wide",
	page_title = "À propos de Fotomo",
    page_icon = "📷"
)

st.header('Photos')
st.write('Les photos sont imprimées professionnellement en format 10 x 15 cm, finition brillante, sur papier Fujifilm épais (210 g/m2).\nDe plus grands formats (11x15cm ou 13x18 cm) peuvent être réalisés sur demande.')

st.header('Petite histoire de Fotomo, les mots en photos')
st.write("""Fotomo est né dans la petite cité de caractère de Piriac-sur-mer (44). 
\n\n\nDéambuler dans ses jolies rues donne envie de prendre des photos…
C’est alors que l’idée de chercher des éléments d’architecture ressemblant à des lettres m’est venue. Dès lors, je me suis transformée en « chasseuse de lettres ». Partout où je vais, je cherche le bon point de vue, celui qui permet de transformer un objet ou un élément d’architecture en une lettre. 
\n\n\nJe suis désormais complètement accro : impossible de regarder une maison sans voir le Z inscrit dans ses volets, le S incrusté dans une grille ou le A formé par les pieds d’une chaise que l’on regarde sous le bon angle.
Et bien sûr, avec les lettres, j’ai écrit des mots (le prénom de mes enfants d’abord, puis celui de mes amis) et même des messages (Bon anniversaire Elsa, Merci Dani, I ❤️ Piriac…).
\n\n\nMaintenant, à vous de jouer et d’écrire vos mots ou vos messages personnels. Toute occasion est bonne : un anniversaire, un mariage, un baptême, ou simplement un merci à dire à un ami… Une fois les mots encadrés, ou chaque lettre placée dans un simple sous-verre à clips, vous obtenez un tableau personnalisé et original et une déco créative. 
\n\n\nMes lettres sont à votre disposition pour écrire le mot de votre choix et l’offrir à ceux que vous aimez.""")

st.header('Légal')
st.write('Fotomo est géré par Valérie Esnis et basé au 8 impasse du Closio, 44420 Piriac-sur-Mer')

st.header('Contact')
st.write('📧 valerie.esnis@fotomo.fr')
st.write('📞 +33 6 12 59 34 57')

st.header('Modalités de livraison')
st.write('La livraison des photos s’effectue en lettre suivie')

st.header('Délais de livraison')
st.write('2 à 3 jours ouvrés en France métropolitaine.')
st.write('3 à 8 jours à l’international.')

st.header('Frais de livraison')
st.write('2,75€ pour la France métropolitaine')
st.write('3,20€ à l’international')