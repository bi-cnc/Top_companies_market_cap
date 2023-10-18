import pandas as pd
import streamlit as st
from PIL import Image
import base64
import io
import os

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("final.csv")
    return df

data = load_data().copy()

# Convert image to Base64
def image_to_base64(img_path, output_size=(64, 64)):
    # Check if the image path exists
    if os.path.exists(img_path):
        with Image.open(img_path) as img:
            img = img.resize(output_size)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"
    return ""

# If 'Logo' column doesn't exist, create one with path to the logos
if 'Logo' not in data.columns:
    output_dir = 'downloaded_logos'
    data['Logo'] = data['Name'].apply(lambda name: os.path.join(output_dir, f'{name}.png'))

# Convert image paths to Base64
data["Logo"] = data["Logo"].apply(image_to_base64)

image_column = st.column_config.ImageColumn(label="Logo", width="medium")


# Adjust the index to start from 1 and display only the first 25 companies
data.reset_index(drop=True, inplace=True)
data = data.head(25)
data.index = data.index + 1


# Display the dataframe
st.write("# Přehled společností")
st.dataframe(data, height=1500, column_config={"Logo": image_column})
