import os
import fitz  # PyMuPDF
import streamlit as st
from datetime import datetime
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

groq_api_key = os.getenv('GROQ_API_KEY', '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')
llm = ChatGroq(
    temperature=0,
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

prompt_extract = PromptTemplate.from_template("""
### MEDICAL REPORT TEXT:
{page_data}

### INSTRUCTION:
1. Extract important test values (e.g., WBC, Hemoglobin).
2. Classify them as Low, Normal, or High.
3. Suggest foods for Low values.
4. Compliment for Normal ones.
5. Add a health summary and patient details.
6. Explain each test briefly.
7. Return as clean JSON.

### FORMAT:
{{
    "tests": [...],
    "summary": "...",
    "patient": {{
        "name": "John Doe",
        "age": "32"
    }}
}}
### OUTPUT:
""")


prompt_summary = PromptTemplate.from_template("""
### MEDICAL REPORT JSON:
{med_report}

### INSTRUCTION:
Write a professional and friendly summary with:
- Name, age, summarizer name (Luv Nichat), date, disclaimer
- Bullet points for all test values
- Advice or compliments based on value
- Final health summary

### OUTPUT FORMAT (No markdown/code):
- Clean structured text
- Line breaks between bullets and sections
""")

def create_pdf(summary_text, filename):
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)

    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        name="CustomStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=18,
        textColor=colors.HexColor("#333333"),
        spaceAfter=12,
    )

    content = []
    for para in summary_text.split("\n\n"):
        content.append(Paragraph(para.strip().replace("\n", "<br/>"), style))
        content.append(Spacer(1, 12))

    doc.build(content)


def process_pdf(pdf_bytes):
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        text = "".join([page.get_text() for page in doc])

    text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
    extract_chain = prompt_extract | llm
    extract_result = extract_chain.invoke({"page_data": text})
    json_data = JsonOutputParser().parse(extract_result.content)

    summarize_chain = prompt_summary | llm
    final_summary = summarize_chain.invoke({"med_report": str(json_data)}).content

    return final_summary, json_data

st.title("🩺 Medical Report Summarizer")
st.markdown("Upload a medical PDF report. We'll extract, analyze, and summarize it with AI.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    with st.spinner("Analyzing report..."):
        summary_text, data = process_pdf(uploaded_file.read())

        st.subheader("📝 Health Summary:")
        st.text_area("Summary", summary_text, height=400)

        pdf_filename = f"report_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        create_pdf(summary_text, pdf_filename)

        with open(pdf_filename, "rb") as f:
            st.download_button("📥 Download PDF Report", f, file_name=pdf_filename)

