# 🩺 Medical Report Analyzer

The **Medical Report Analyzer** is an AI-powered Streamlit web application that analyzes medical reports (PDF files), extracts key health parameters (like WBC, Hemoglobin, etc.), and provides:

- 🔍 Health condition analysis  
- 🍽️ Food recommendations for improvement  
- 😊 Compliments for healthy indicators  
- 📄 A simple, user-friendly health summary

---

## 🚀 Features

- ✅ Upload and analyze medical report PDFs
- 🧠 Extracts useful health data using LLMs (Groq)
- 🍎 Food suggestions for low or high values
- 🙌 Compliments for healthy readings
- 📊 Summarized health analysis in a clean UI
- 💾 Optionally download the result as a PDF

---

## 📁 Example Parameters Analyzed

- White Blood Cells (WBC)  
- Red Blood Cells (RBC)  
- Hemoglobin  
- Platelet Count  
- Blood Sugar  
- Cholesterol  
- And many more...

---

## 🛠 Tech Stack

- **Python** – Core language  
- **Streamlit** – For building the web interface  
- **LangChain** – Prompt orchestration with LLMs  
- **LLMs** – OpenAI / Groq / Hugging Face  
- **PyMuPDF (fitz)** – For extracting text from PDF reports  

---

## ⚙️ How to Run Locally

### 1. Clone the Repository 
```bash
git clone https://github.com/your-username/medical-report-analyzer.git
cd medical-report-analyzer
```
### 2. Use your own API key

