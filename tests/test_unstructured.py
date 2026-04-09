from unstructured.partition.auto import partition

elements = partition("data/1.pdf")

for element in elements[:20]:
    print(f"Type: {type(element).__name__}")
    print(f"Text: {element.text[:100]}")
    print("---")