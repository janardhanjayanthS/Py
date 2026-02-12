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

# 5. Sarvam ai
"""
Outputs a .zip file containing information about the .pdf,
within that there is a metadata dir. which contains .json for each page
the document.md within output dir contains .md version of the pdf
"""
# from os import getenv

# from dotenv import load_dotenv
# from sarvamai import SarvamAI

# load_dotenv()

# SARVAM_API_KEY = getenv("SARVAM_API_KEY")

# client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

# job = client.document_intelligence.create_job(
#     language="hi-IN",  # Target language (BCP-47 format)
#     output_format="md",  # Output format: "html" or "md" (delivered as ZIP)
# )

# job.upload_file("Plans-1-8new.pdf")
# job.start()
# status = job.wait_until_complete()
# print(f"Job completed: {status.job_state}")
# metrics = job.get_page_metrics()
# print(f"Pages processed: {metrics['pages_processed']}")

# # Download the output (ZIP file containing the processed document)
# job.download_output("./output.zip")
# print("Output saved to ./output.zip")


# 6. Using LLM with PyMuPDF
# OCR PDF using PyMuPDF + OpenAI Vision
# import base64
# from io import BytesIO
# from os import getenv

# import fitz  # PyMuPDF
# from dotenv import load_dotenv
# from openai import OpenAI
# from PIL import Image

# load_dotenv()
# OPENAI_API_KEY = getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=OPENAI_API_KEY)


# def pdf_page_to_base64(pdf_path, page_number, dpi=300):
#     """
#     Convert PDF page to base64 encoded image

#     Args:
#         pdf_path: Path to PDF
#         page_number: Page number (0-indexed)
#         dpi: Resolution (higher = better OCR, but slower)
#     """
#     doc = fitz.open(pdf_path)
#     page = doc[page_number]

#     # Render page to image at high resolution for better OCR
#     mat = fitz.Matrix(dpi / 72, dpi / 72)  # 72 is default DPI
#     pix = page.get_pixmap(matrix=mat)

#     # Convert to PIL Image
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     # Convert to base64
#     buffered = BytesIO()
#     img.save(buffered, format="PNG")
#     img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

#     doc.close()
#     return img_base64


# def extract_text_with_vision(pdf_path, page_number=0, prompt=None):
#     """
#     Extract text from PDF page using OpenAI Vision

#     Args:
#         pdf_path: Path to PDF
#         page_number: Page to extract (0-indexed)
#         prompt: Custom extraction prompt (optional)
#     """
#     # Convert page to image
#     img_base64 = pdf_page_to_base64(pdf_path, page_number)

#     # Default prompt for OCR
#     if prompt is None:
#         prompt = """
#         Extract all text from this image exactly as it appears.
#         Output the extracted text as same as the image, do not change context.
#         Do not add ``` symbol or titles at the start and end of the response
#         """

#     # Call OpenAI Vision API
#     response = client.chat.completions.create(
#         model="gpt-4o",  # or "gpt-4-turbo" or "gpt-4o-mini"
#         messages=[
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": prompt},
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/png;base64,{img_base64}",
#                             "detail": "high",  # high, low, or auto
#                         },
#                     },
#                 ],
#             }
#         ],
#         max_tokens=4096,
#     )

#     return response.choices[0].message.content


# # Usage - Extract page 2 (index 1)
# print("Extracting page 6 using GPT-4 Vision OCR...")
# extracted_text = extract_text_with_vision(
#     "Plans-1-8new.pdf",
#     page_number=5,  # Page 2 (0-indexed)
# )

# print("\n" + "=" * 60)
# print("EXTRACTED TEXT")
# print("=" * 60)
# print(extracted_text)

# # Save output
# with open("page_6_gpt4_vision_ocr.md", "w", encoding="utf-8") as f:
#     f.write(extracted_text)
# print("\n✓ Saved to page_2_gpt4_vision_ocr.md")


# 7. OCRmyPDF - converts the images in pdf to text (refer Plans-1-8new_ocr_advanced.pdf),
# so that we can process it with any document loaders (I think)
"""
requires:
- Ghostscript - https://ghostscript.com/releases/gsdnld.html
"""
# import ocrmypdf


# def ocr_pdf_advanced(input_pdf, output_pdf, language="eng"):
#     """
#     Advanced OCR with optimized settings for technical documents
#     """
#     try:
#         ocrmypdf.ocr(
#             input_pdf,
#             output_pdf,
#             # Language settings
#             language=language,  # 'eng', 'eng+fra' for multiple
#             # OCR behavior
#             force_ocr=True,  # False = smart OCR (skip text pages)
#             skip_text=False,  # Keep existing text
#             redo_ocr=False,  # Re-do OCR on pages that already have it
#             # Image processing
#             deskew=True,  # Straighten pages
#             clean=False,  # Clean image before OCR
#             clean_final=False,  # Clean final output
#             remove_background=False,  # Remove background (experimental)
#             # Image optimization
#             optimize=1,  # 0=none, 1=safe, 2=lossy, 3=aggressive
#             jpeg_quality=95,  # JPEG quality (0-100)
#             png_quality=95,  # PNG quality (0-100)
#             jbig2_lossy=False,  # Use lossy JBIG2 (smaller files)
#             # OCR engine settings
#             tesseract_timeout=180,  # Timeout per page (seconds)
#             rotate_pages=True,  # Auto-rotate pages
#             remove_vectors=False,  # Remove vector graphics
#             # Output settings
#             output_type="pdfa",  # 'pdfa', 'pdf', 'pdfa-1', 'pdfa-2', 'pdfa-3'
#             pdfa_image_compression="auto",  # 'auto', 'jpeg', 'lossless'
#             # Performance
#             jobs=4,  # Parallel processing (number of CPU cores)
#             use_threads=True,  # Use threading
#             # Progress
#             progress_bar=True,
#             # Keep metadata
#             keep_temporary_files=False,
#             # Advanced
#             oversample=300,  # DPI for oversampling (improves OCR)
#         )
#         print(f"✓ Advanced OCR completed: {output_pdf}")
#         return True
#     except Exception as e:
#         print(f"ERROR: {e}")
#     # except ocrmypdf.exceptions.PriorOcrFoundError:
#     #     print("⚠️ PDF already has OCR text layer")
#     #     return False
#     # except Exception as e:
#     #     print(f"❌ OCR failed: {str(e)}")
#     #     return False


# # Usage
# ocr_pdf_advanced("Plans-1-8new.pdf", "Plans-1-8new_ocr_advanced.pdf", language="eng")


# 8. Pdf2image - works

# import pytesseract
# from pdf2image import convert_from_path

# # convert to image using resolution 600 dpi
# pages = convert_from_path("plans-1-8new.pdf", 400)

# # extract text
# text_data = ""
# for page in pages:
#     text = pytesseract.image_to_string(page)
#     text_data += text + "\n"
# print(text_data)


# 9. PyMuPdf with easyocr
"""
Converts each page into image (.png) -> then uses easy ocr to read
contents from it using a model
"""

# from os import getcwd, listdir

# import easyocr
# import fitz

# pdffile = "Plans-1-8new.pdf"
# doc = fitz.open(pdffile)
# zoom = 4
# mat = fitz.Matrix(zoom, zoom)
# count = 0
# # Count variable is to get the number of pages in the pdf
# for p in doc:
#     count += 1
# for i in range(count):
#     val = f"image_{i + 1}.png"
#     page = doc.load_page(i)
#     pix = page.get_pixmap(matrix=mat)
#     pix.save(val)
# doc.close()

# imgs = [content for content in listdir(getcwd()) if content.endswith(".png")]
# reader = easyocr.Reader(["en"])
# for img in imgs:
#     result = reader.readtext(img, detail=0)
#     print(result)
#     print("-" * 100)
