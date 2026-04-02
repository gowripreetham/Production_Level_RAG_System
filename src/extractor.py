import pymupdf
import os
import re


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


