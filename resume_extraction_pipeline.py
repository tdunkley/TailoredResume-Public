import os
import sys
import json
import re
import pdfplumber
import pytesseract
from docx import Document
from PIL import Image
import spacy

# ✅ Dynamically add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))  # Move up two levels
sys.path.append(project_root)

from modules.utils.path_manager import PATHS, add_project_to_sys_path

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Regex for structured field extraction
EMAIL_REGEX = r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+"
PHONE_REGEX = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
LINKEDIN_REGEX = r"(https?:\/\/)?([\w]+\.)?linkedin\.com\/in\/[\w-]+"

def clean_extracted_text(text):
    """ Remove unwanted artifacts like page numbers or extra spacing """
    text = re.sub(r'Page \d+ of \d+', '', text)  # Remove "Page X of Y"
    text = re.sub(r'\n\s*\n', '\n', text)  # Remove excessive newlines
    return text.strip()

def extract_text_from_pdf(pdf_path):
    """ Extract text from PDF using pdfplumber and OCR fallback """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        text = clean_extracted_text(text)  # Apply cleaning
        if not text.strip():
            text = pytesseract.image_to_string(Image.open(pdf_path))
    except FileNotFoundError:
        print(f"⚠️ PDF not found: {pdf_path}")
    except Exception as e:
        print(f"Error processing PDF: {e}")
    return text

def extract_text_from_docx(docx_path):
    """ Extract text from DOCX """
    try:
        doc = Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return clean_extracted_text(text)
    except FileNotFoundError:
        print(f"⚠️ DOCX not found: {docx_path}")
    except Exception as e:
        print(f"Error processing DOCX: {e}")
    return ""

def extract_contact_info(text):
    """ Extract email, phone, and LinkedIn profile from text """
    def safe_search(pattern, text):
        match = re.search(pattern, text)
        return match.group(0).strip() if match else None  # Return `None` if no match is found

    return {
        "email": safe_search(EMAIL_REGEX, text),
        "phone": safe_search(PHONE_REGEX, text),
        "linkedin": safe_search(LINKEDIN_REGEX, text)
    }

def classify_sections(text):
    """ Use NLP to classify resume sections dynamically """
    doc = nlp(text)
    sections = {}
    current_section = "General"
    
    for line in text.split("\n"):
        if len(line.strip()) > 3:
            if "experience" in line.lower():
                current_section = "Experience"
            elif "education" in line.lower():
                current_section = "Education"
            elif "skills" in line.lower():
                current_section = "Skills"
            sections.setdefault(current_section, []).append(line)
    
    return {k: "\n".join(v) for k, v in sections.items()}

def process_resume():
    """ Attempt to process both PDF and DOCX if available """
    text = ""
    pdf_path = PATHS["resume_pdf"]
    docx_path = PATHS["resume_file"]  # Assuming this points to the DOCX version

    # Try PDF first
    if os.path.exists(pdf_path):
        print(f"✅ Processing PDF: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)
    elif os.path.exists(docx_path):
        print(f"✅ PDF not found. Switching to DOCX: {docx_path}")
        text = extract_text_from_docx(docx_path)
    else:
        print("❌ No resume file found (PDF or DOCX). Exiting.")
        return None

    if not text.strip():
        print("⚠️ Warning: No text extracted from the resume file.")

    contact_info = extract_contact_info(text)
    sections = classify_sections(text)

    return {
        "contact_info": contact_info,
        "sections": sections
    }

def save_to_json(data, output_path=PATHS["resume_output_json"]):
    """ Save extracted data to JSON file """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Resume extraction complete. Saved to {output_path}.")
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")

# Main execution block
if __name__ == "__main__":
    result = process_resume()
    if result:
        save_to_json(result)
