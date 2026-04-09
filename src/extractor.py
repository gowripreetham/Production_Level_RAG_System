from unstructured.partition.auto import partition

KEEP_TYPES = {"NarrativeText", "Title", "ListItem", "Table", "Text"}
AVOID_TYPES = {"@", "http", "www", "doi.org"}

def extract_text_from_pdf(pdf_path):
    elements = partition(pdf_path)
    filtered = []
    for element in elements:
        # check element type is in KEEP_TYPES
        if type(element).__name__ in KEEP_TYPES:
            if not any(avoid in element.text for avoid in AVOID_TYPES):
                if len(element.text) > 75:
                    filtered.append(element)
        # check element.text doesn't contain @, http, www, doi.org
        # if passes both checks, append element.text to filtered
    return filtered

if __name__ == "__main__":
    texts = extract_text_from_pdf("data/1.pdf")
    print(f"Total elements extracted: {len(texts)}")
    for t in texts[:10]:
        print("---")
        print(t[:200])