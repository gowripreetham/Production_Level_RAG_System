from unstructured.chunking.title import chunk_by_title

def chunk_text(elements):
    chunks = chunk_by_title(
        elements,
        max_characters=2000,
        new_after_n_chars=1500,
        overlap=200,
        overlap_all=True
    )
    return [chunk.text for chunk in chunks if len(chunk.text) > 100]