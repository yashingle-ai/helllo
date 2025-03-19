# Data Analyst Agent

##  Overview
The **Data Analyst Agent** is a powerful tool that allows users to **upload various document types** (.csv, .xlsx, .txt, .pdf, .docx, images) and perform data analysis using an **LLM-powered backend**. The agent can **answer questions**, **generate insights**, and **create visualizations** from structured and unstructured data.

##  Features
- ✅ **Upload and process files** (CSV, Excel, Text, PDF, DOCX, Images)
- 🤖 **Ask any questions** and get AI-generated answers
- 📊 **Automatic data analysis** and summarization
- 📈 **Interactive visualizations** (histograms, box plots, pair plots, etc.)
- 📄 **Extract and analyze text from PDFs and DOCX files**
- 🖼️ **Analyze images** using multimodal AI models

## 🛠️ Technologies Used
- **Python** (Primary language)
- **Streamlit** (UI framework)
- **Pandas** (Data handling and processing)
- **Matplotlib & Seaborn** (Data visualization)
- **Requests** (API calls to Hugging Face)
- **PyMuPDF (Fitz)** (PDF text extraction)
- **python-docx** (DOCX text extraction)

## 📥 Installation
To set up and run the **Data Analyst Agent**, follow these steps:

### 1️⃣ Clone the repository
```bash
git clone <repository-url>
cd data-analyst-agent
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set up environment variables
Create a `.env` file and add your **Hugging Face API Key**:
```
HUGGINGFACE_API_KEY=your_api_key_here
```

### 4️⃣ Run the Streamlit app
```bash
streamlit run app.py
```

## 📂 Usage
1. **Upload a file** (CSV, Excel, PDF, DOCX, Image, etc.)
2. **View the extracted content or dataset summary**
3. **Ask questions** related to the uploaded document or dataset
4. **Generate insights and visualizations** using AI-powered analysis
5. **Download results if needed**

## 📝 Example Queries
- "What is the average sales in this dataset?"
- "Summarize the content of this document."
- "Show me the distribution of product prices."
- "How many missing values are in this dataset?"

## 📌 Future Enhancements
- 🔍 **Improved NLP for question-answering**
- 📊 **More advanced visualizations** (correlation heatmaps, scatter plots, etc.)
- 🌐 **Deployment on cloud services**
- 📦 **Export analysis reports in PDF format**

## 📞 Contact
For any issues or suggestions, feel free to reach out at **yash.ingle003@gmail.com** or create an issue in the repository.

---
**© 2025 Data Analyst Agent | Developed by Yash Ingle**
