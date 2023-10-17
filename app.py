import streamlit as st
import pandas as pd
import os
from PIL import Image
import base64
import io

# Nahrání dat
@st.cache_data
def load_data():
    data = pd.read_csv('final.csv')
    return data

data = load_data()



# Vykreslení tabulky s logy
st.markdown("<h1 style='text-align: center;'>Žebříček největších společností světa</h1>", unsafe_allow_html=True)
st.write("")

output_dir = 'downloaded_logos'

# Vytvoření hlavičky tabulky s menšími nadpisy
col_headers = ['\u200B', '\u200B', 'Název společnosti', 'Tržní kapitalizace (v mld. USD)', 'Cena za 1 akcii (USD)']
col1, col_logo, col2, col3, col4 = st.columns([1, 1, 7, 7, 5])
columns = [col1, col_logo, col2, col3, col4]
for col, header in zip(columns, col_headers):
    col.markdown(f"<h3 style='text-align: center; font-size: 16px;'>{header}</h3>", unsafe_allow_html=True)

def image_to_base64(img_path, output_size=(64, 64)):
    with Image.open(img_path) as img:
        img = img.resize(output_size)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

for index, row in data.head(25).iterrows():
    company_name = row['Name']
    logo_path = os.path.join(output_dir, f'{company_name}.png')
    
    # Pořadí společnosti
    with col1:
        st.markdown(f"<div style='text-align: center; margin-bottom: 20px; line-height: 40px;'>{index + 1}</div>", unsafe_allow_html=True)
    
    # Logo společnosti
    with col_logo:
        if os.path.exists(logo_path):
            logo_base64 = image_to_base64(logo_path)
            st.markdown(f"<img src='{logo_base64}' style='width: 40px; height: 40px; margin-bottom: 20px; display: block; margin-left: auto; margin-right: auto;' />", unsafe_allow_html=True)
    
    # Název společnosti se zvětšeným písmem
    with col2:
        st.markdown(f"<div style='text-align: center; line-height: 40px; margin-bottom: 20px; font-size: 18px;'>{company_name}</div>", unsafe_allow_html=True)
    
    # Tržní kapitalizace
    with col3:
        market_cap_value = str(row['Market Cap'])
        st.markdown(f"<div style='text-align: center; margin-bottom: 20px; line-height: 40px;'>{market_cap_value}</div>", unsafe_allow_html=True)


    # Uzavírací cena akcie za poslední den
    with col4:
        st.markdown(f"<div style='text-align: center; margin-bottom: 20px; line-height: 40px;'>{row['Price']}</div>", unsafe_allow_html=True)
