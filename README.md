# Medicine Recommender System

Welcome to the Medicine Recommender System! This application provides alternative recommendations for medicines using a machine learning model. It is built with Streamlit for the frontend and leverages Python's data processing capabilities.

![Medicine Recommender System](images/medicine-image.jpg)

## Features

- **Medicine Search:** Type the name of a medicine to get alternative recommendations.
- **Recommendations:** Provides a list of recommended medicines with purchase links.
- **Beautiful Interface:** Custom CSS for an enhanced user experience.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/FaheemKhan0817/Medicine-Recommender-System.git
    
    cd Medicine-Recommender-System
    ```

2. **Install the required dependencies:**

    Since there is no `requirements.txt` file, you can manually install the necessary packages:

    ```sh
    pip install streamlit pandas pillow
    ```

3. **Extract the necessary data files:**

    Ensure you have `pickle-file.rar` in the `data/` directory. Extract the `.pkl` files from `pickle-file.rar`:

    ```sh
    cd data
    unrar e pickle-file.rar
    cd ..
    ```

4. **Run the application:**

    ```sh
    streamlit run app.py
    ```

## Usage

1. **Search for a Medicine:**
   - Type the name of the medicine in the search box.
   - Click on the 'Recommend Medicine' button.

2. **View Recommendations:**
   - The application will display a list of alternative medicines.
   - Click on the provided links to purchase the recommended medicines.

## Project Structure

```plaintext
medicine-recommender-system/
├── css/
│   └── style.css           # Custom CSS for styling the application
├── images/
│   └── medicine-image.jpg  # Image displayed in the app
├── data/
│   └── pickle-file.rar     # Archive containing pickle files
├── app.py                  # Main application script
└── README.md               # Project README file
