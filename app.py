import streamlit as st
import requests
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io
import fitz  # PyMuPDF for PDF text extraction
import docx  # python-docx for DOCX text extraction

# ---------------------------
# ✅ Hugging Face API Configuration
# ---------------------------
api_key = "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"  # ⚠️ Hardcoded API key (not recommended for security)

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

HEADERS = {"Authorization": f"Bearer {api_key}"}

# ---------------------------
# ✅ Function to Call Hugging Face API
# ---------------------------
def query_huggingface(payload):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        if response.text.strip():
            return response.json()
        else:
            return {"error": "Empty response from API"}
    except requests.exceptions.RequestException as e:
        return {"error": "API Request Failed", "details": str(e)}
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response"}

# ---------------------------
# ✅ Function to Extract Text from PDF
# ---------------------------
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

# ---------------------------
# ✅ Function to Extract Text from DOCX
# ---------------------------
def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# ---------------------------
# ✅ Streamlit UI
# ---------------------------
st.title("📊 Data Analyst Agent")

uploaded_file = st.file_uploader("📂 Upload a file", type=["csv", "xlsx", "txt", "pdf", "docx", "png", "jpg"])

if uploaded_file is not None:
    st.success("✅ File uploaded successfully.")
    file_type = uploaded_file.type

    # ---------------------------
    # 📜 Text-Based Files (TXT, PDF, DOCX)
    # ---------------------------
    if file_type == "text/plain":
        file_contents = uploaded_file.read().decode("utf-8")
    elif file_type == "application/pdf":
        file_contents = extract_text_from_pdf(uploaded_file)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        file_contents = extract_text_from_docx(uploaded_file)
    else:
        file_contents = None
    
    if file_contents:
        st.text_area("📄 File Content", file_contents, height=200)
        query = st.text_input("🔎 Ask a question about the document")
        if st.button("📖 Get Answer"):
            structured_query = f"""
            Given the following document:
            \n{file_contents}\n\n
            Answer the question based only on the document content:
            \nQuestion: {query}
            """
            result = query_huggingface({"inputs": structured_query})
            st.json(result)

    # ---------------------------
    # 📊 CSV & Excel Files
    # ---------------------------
    elif file_type in ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        df = pd.read_csv(uploaded_file, low_memory=False) if file_type == "text/csv" else pd.read_excel(uploaded_file)
        st.dataframe(df)

        st.subheader("📊 Data Summary")
        st.write(df.describe())

        # 📊 Generate Visualization
        st.subheader("📉 Visualizations")
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_columns:
            selected_column = st.selectbox("📌 Select a column for visualization", numeric_columns)
            fig, ax = plt.subplots()
            sns.histplot(df[selected_column], bins=20, kde=True, ax=ax)
            st.pyplot(fig)

            # Additional Visualizations
            st.subheader("📈 Additional Visualizations")
            
            # Bar Plot for Mean Values
            fig, ax = plt.subplots()
            df[numeric_columns].mean().plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title("Mean Values of Numeric Columns")
            st.pyplot(fig)
            
            # Box Plot for Outlier Detection
            fig, ax = plt.subplots()
            sns.boxplot(data=df[numeric_columns], ax=ax)
            ax.set_title("Box Plot for Numeric Columns")
            st.pyplot(fig)
            
            # Pair Plot for Relationships
            st.subheader("📊 Pair Plot (Feature Relationships)")
            pair_plot = sns.pairplot(df[numeric_columns])
            st.pyplot(pair_plot)
        
        query = st.text_input("💡 Ask a question about the data")
        if st.button("📊 Get Data Insights"):
            structured_query = f"""
            Given the following dataset:
            \n{df.to_json()}\n\n
            Answer the question based only on the dataset content:
            \nQuestion: {query}
            """
            result = query_huggingface({"inputs": structured_query})
            st.json(result)

    # ---------------------------
    # 🖼️ Image Handling
    # ---------------------------
    elif file_type in ["image/png", "image/jpeg"]:
        image = Image.open(uploaded_file)
        st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)
        
        if st.button("🧐 Analyze Image"):
            img_bytes = io.BytesIO()
            image.save(img_bytes, format=image.format)
            files = {"file": img_bytes.getvalue()}
            response = requests.post(API_URL, headers=HEADERS, files=files)
            result = response.json()
            st.json(result)