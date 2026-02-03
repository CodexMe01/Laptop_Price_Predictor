import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the saved model and column structure
model = pickle.load(open('laptop_model.pkl', 'rb'))
model_columns = pickle.load(open('columns.pkl', 'rb'))

st.title("💻 Laptop Price Predictor")
st.write("Enter the specifications to get the estimated price.")

# --- USER INPUTS ---
col1, col2 = st.columns(2)

with col1:
    company = st.selectbox("Company", ['Apple', 'HP', 'Dell', 'Lenovo', 'Asus', 'Acer', 'MSI', 'Toshiba', 'Others'])
    typename = st.selectbox("Type", ['Ultrabook', 'Notebook', 'Gaming', 'Workstation', 'Netbook', '2 in 1 Convertible'])
    ram = st.selectbox("RAM (in GB)", [2, 4, 6, 8, 12, 16, 24, 32, 64])

with col2:
    opsys = st.selectbox("Operating System", ['Windows 10', 'macOS', 'Linux', 'No OS', 'Chrome OS', 'Windows 7'])
    weight = st.number_input("Weight (in kg)", min_value=0.5, max_value=5.0, value=2.0)
    inches = st.number_input("Screen Size (Inches)", min_value=10.0, max_value=20.0, value=15.6)

# --- PREDICTION LOGIC ---
if st.button("Predict Price"):
    # 1. Create a row of zeros matching our training columns
    input_data = pd.DataFrame(0, index=[0], columns=model_columns)
    
    # 2. Fill in the numerical values
    input_data['Ram'] = ram
    input_data['Weight'] = weight
    input_data['Inches'] = inches
    
    # 3. Handle One-Hot Encoding (Set the correct 'True' column)
    # Note: drop_first=True means some categories (like Acer or Apple) 
    # might be represented by all zeros.
    if f'Company_{company}' in model_columns:
        input_data[f'Company_{company}'] = 1
    if f'TypeName_{typename}' in model_columns:
        input_data[f'TypeName_{typename}'] = 1
    if f'OpSys_{opsys}' in model_columns:
        input_data[f'OpSys_{opsys}'] = 1
    
    # 4. Predict
    prediction = model.predict(input_data*108.62)[0]
    
    st.success(f"The estimated price for this laptop is: {round(prediction, 2)}INR")
