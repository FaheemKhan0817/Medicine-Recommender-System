import streamlit as st
import pickle
import pandas as pd
from PIL import Image
import gdown
import os
import patoolib
import tempfile

# Define the URL of your pickle file stored in Google Drive
url = 'https://drive.google.com/uc?id=1LV4cFPzsghSVneCHMf7QhDZLXNVU4rij'

# Path to save the downloaded file in a temporary directory
temp_dir = tempfile.gettempdir()
output = os.path.join(temp_dir, 'pickle-file.rar')

# Download the file if it does not exist
if not os.path.exists(output):
    gdown.download(url, output, quiet=False)

# Extract the rar file into the temporary directory
if not os.path.exists(os.path.join(temp_dir, 'medicine_dict.pkl')):
    patoolib.extract_archive(output, outdir=temp_dir)

# To Add External CSS
try:
    with open('css/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning('CSS file not found.')

# Caching the data loading
@st.cache_data
def load_data():
    try:
        medicines_dict = pickle.load(open(os.path.join(temp_dir, 'medicine_dict.pkl'), 'rb'))
        similarity = pickle.load(open(os.path.join(temp_dir, 'similarity.pkl'), 'rb'))
        medicines = pd.DataFrame(medicines_dict)
        return medicines, similarity
    except FileNotFoundError:
        st.error("Data files not found. Please make sure 'medicine_dict.pkl' and 'similarity.pkl' are in the correct directory.")
        return None, None

medicines, similarity = load_data()

if medicines is not None and similarity is not None:

    # Recommendation Function
    def recommend(medicine):
        try:
            medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
            distances = similarity[medicine_index]
            medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

            recommended_medicines = [medicines.iloc[i[0]].Drug_Name for i in medicines_list]
            return recommended_medicines
        except IndexError:
            st.error(f'Medicine {medicine} not found in the dataset.')
            return []

    # Application Frontend
    st.title('Medicine Recommender System')

    # Searchbox
    selected_medicine_name = st.selectbox(
        'Type your medicine name whose alternative is to be recommended',
        medicines['Drug_Name'].values)

    # Recommendation Program
    if st.button('Recommend Medicine'):
        with st.spinner('Finding recommendations...'):
            recommendations = recommend(selected_medicine_name)
            if recommendations:
                for j, medicine in enumerate(recommendations, start=1):
                    st.write(f"{j}. {medicine}")
                    st.write(f"[Click here to buy]({'https://pharmeasy.in/search/all?name='+medicine})")

    # Image load
    try:
        image = Image.open('images/medicine-image.jpg')
        st.image(image, caption='Recommended Medicines')
    except FileNotFoundError:
        st.warning('Image file not found.')
