import pdfplumber

with pdfplumber.open("/Users/gowripreetam/Desktop/RAG-P/docs/1.pdf") as pdf:
    print(pdf.pages[0].extract_text())


print("*********Line Break***********")

import pymupdf

doc = pymupdf.open("/Users/gowripreetam/Desktop/RAG-P/docs/1.pdf") # open a document
out = open("output.txt", "wb") # create a text output
text = doc[0].get_text() # get plain text (is in UTF-8)
print(text)
out.close()