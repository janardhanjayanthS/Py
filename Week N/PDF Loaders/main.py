# 1. shows only the image - not the actual text
# import fitz

# doc = fitz.open("Plans-1-8new.pdf")
# for page in doc:
#     images = page.get_images()
#     print("image: ", images)
#     text = page.get_text()
#     print("text: ", text)


# 2. Does not work
# import pdfplumber

# with pdfplumber.open("Plans-1-8new.pdf") as pdf:
#     for page in pdf.pages:
#         text = page.extract_text()
#         tables = page.extract_tables()
#         print(text)
#         print(tables)


# 3. works! - uses ocr to extract text since the pdf contains image text
"""
docs: https://docs.unstructured.io/open-source/core-functionality/partitioning#partition_pdf
pre reqs.:
- poppler - https://github.com/oschwartz10612/poppler-windows/releases
- tesseract - https://github.com/UB-Mannheim/tesseract/wiki
"""

# from unstructured.partition.pdf import partition_pdf

# # elements = partition_pdf("Plans-1-8new.pdf")
# elements = partition_pdf("Plans-1-8new.pdf", strategy="ocr_only", languages=["eng"])
# for element in elements:
#     print(element)
#     print()
#     print("element text:")
#     print(element.text)
#     print("-" * 100)

# 4. page_content attr of each doc is empty
# from langchain_community.document_loaders import PyMuPDFLoader

# loader = PyMuPDFLoader("Plans-1-8new.pdf")
# documents = loader.load()
# print(documents)
