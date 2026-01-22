import os
from typing import Any

import pymupdf  # noqa: F401
from langchain_community.document_loaders import PyMuPFDLoader

corpus: list[str | list[Any] | dict[Any, Any]] = []
pdf_dir: str = os.getcwd() + "/../data/new_pdfs"
pdf_files = os.listdir(pdf_dir)

for pdf in pdf_files:
    doc = pymupdf.open(pdf_dir + f"/{pdf}")

    new_doc = PyMuPFDLoader(pdf_dir + f"/{pdf}")
    print(new_doc)
