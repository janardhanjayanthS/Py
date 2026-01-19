import pymupdf

doc = pymupdf.open("data/ml.pdf")
corpus = []
for page in doc:
    if page:
        corpus.append(page.get_text())
