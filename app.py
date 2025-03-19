import streamlit as st
import requests
import pandas as pd
import json
import os

# api_key = os.environ.get("API_KEY")  # Use .get() to avoid KeyError if variable is missing
api_key = os.environ.get("api")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

HEADERS = {"Authorization": f"Bearer {api_key}"}

def query_huggingface(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

# Streamlit UI
st.title("Data Analyst Agent")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx", "txt", "pdf", "docx", "png", "jpg"])

if uploaded_file is not None:
    st.write("File uploaded successfully.")
    file_type = uploaded_file.type
    
    # Handle text-based files
    if file_type in ["text/plain", "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        file_contents = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", file_contents, height=200)
        
        if st.button("Analyze with AI"):
            result = query_huggingface({"inputs": file_contents})
            st.write("AI Response:", result)
    
    # Handle CSV and Excel files
    elif file_type in ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        df = pd.read_csv(uploaded_file) if file_type == "text/csv" else pd.read_excel(uploaded_file)
        st.dataframe(df)
        
        if st.button("Analyze Data"):
            result = query_huggingface({"inputs": df.to_json()})
            st.write("AI Response:", result)

    # Handle images
    elif file_type in ["image/png", "image/jpeg"]:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Analyze Image"):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(API_URL, headers=HEADERS, files=files)
            result = response.json()
            st.write("AI Response:", result)
