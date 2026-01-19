import pymupdf

doc = pymupdf.open("data/algorithms_to_live_by.pdf")
corpus = []
for page in doc:
    if page:
        corpus.append(page.get_text())
