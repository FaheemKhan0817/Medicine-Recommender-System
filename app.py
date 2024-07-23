import streamlit as st
import pickle
import pandas as pd
from PIL import Image
import os
import zipfile
import tempfile

# Path to save the extracted files in a temporary directory
temp_dir = tempfile.gettempdir()

# Streamlit file uploader for the zip file
uploaded_file = st.file_uploader("Upload your Pickle-files.zip", type="zip")

if uploaded_file is not None:
    # Extract the zip file into the temporary directory
    zip_file_path = os.path.join(temp_dir, 'Pickle-files.zip')
    with open(zip_file_path, 'wb') as file:
        file.write(uploaded_file.getbuffer())
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

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
else:
    st.warning('Please upload the Pickle-files.zip to proceed.')
