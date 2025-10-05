import pytesseract
from pdf2image import convert_from_path
import os

# ----------- CONFIG -----------
PDF_PATH = "/Users/aryan/Downloads/Amrit Sagar bade panditji.pdf"  # your input PDF
OUTPUT_PATH = "/Users/aryan/Downloads/Amrit_Sagar_Hindi_Extracted.txt"         # output text file
LANG = "hin"                                            # Hindi OCR
PAGES_PER_BATCH = 5                                     # to process in small chunks
MAX_PAGES = 10                                          # limit to first N pages (set to None for all)
# ------------------------------

# Convert PDF to images (in small batches to manage memory)
def pdf_to_images(pdf_path, start_page, end_page):
    return convert_from_path(pdf_path, first_page=start_page, last_page=end_page)

# Perform OCR on each image and append text
def extract_text_from_pdf(pdf_path, output_path):
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    # Limit pages if MAX_PAGES is set
    pages_to_process = min(total_pages, MAX_PAGES) if MAX_PAGES else total_pages

    print(f"Total pages in PDF: {total_pages}")
    print(f"Processing pages: {pages_to_process}")
    full_text = ""

    for start in range(1, pages_to_process + 1, PAGES_PER_BATCH):
        end = min(start + PAGES_PER_BATCH - 1, pages_to_process)
        print(f"Processing pages {start} to {end}...")
        pages = pdf_to_images(pdf_path, start, end)
        for page in pages:
            text = pytesseract.image_to_string(page, lang=LANG)
            full_text += text + "\n\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"\n✅ Extraction complete! Saved to {output_path}")

if __name__ == "__main__":
    extract_text_from_pdf(PDF_PATH, OUTPUT_PATH)