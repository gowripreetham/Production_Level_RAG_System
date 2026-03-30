import pymupdf
import os
import re

# Path to your PDFs folder
DATA_DIR = "/Users/gowripreetam/Desktop/RAG-P/rag-professor/data"

# --- Cleaning Rules ---
def clean_line(line):
    line = line.strip()

    # Rule 1: Remove empty lines
    if not line:
        return None

    if len(line) < 5:
        return None

    if "@" in line:
        return None
    
    if line.startswith("http"):
        return None
    
    if ".com" in line:
        return None
    
    if " Published by " in line:
        return None

    return line


def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    cleaned_lines = []

    for page in doc:
        text = page.get_text()
        lines = text.split("\n")

        for line in lines:
            cleaned = clean_line(line)
            if cleaned:
                cleaned_lines.append(cleaned)

    return cleaned_lines


def main():
    pdf_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")])

    print(f"Found {len(pdf_files)} PDF files\n")

    for i, pdf_file in enumerate(pdf_files):
        pdf_path = os.path.join(DATA_DIR, pdf_file)
        print(f"Processing: {pdf_file}")

        cleaned_text = extract_text_from_pdf(pdf_path)

        # Only print for the FIRST paper
        if i == 0:
            print("\n--- Cleaned Text (First PDF Only) ---\n")
            for line in cleaned_text[:100]:  # limit to first 100 lines for readability
                print(line)

        print(f"Finished: {pdf_file}\n")


if __name__ == "__main__":
    main()