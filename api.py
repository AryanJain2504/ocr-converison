from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import uuid
from datetime import datetime
import shutil
from pathlib import Path

app = FastAPI(title="PDF OCR Converter API")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('outputs')
STATIC_FOLDER = Path('static')
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Create folders if they don't exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)
STATIC_FOLDER.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_FOLDER)), name="static")

def pdf_to_images(pdf_path: str, start_page: int, end_page: int):
    """Convert PDF pages to images"""
    return convert_from_path(pdf_path, first_page=start_page, last_page=end_page)

def extract_text_from_pdf(pdf_path: str, output_path: str, lang: str = 'hin', 
                         pages_per_batch: int = 5, max_pages: int = None):
    """Extract text from PDF using OCR"""
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        # Limit pages if max_pages is set
        pages_to_process = min(total_pages, max_pages) if max_pages else total_pages
        
        full_text = f"OCR Extraction Results\n"
        full_text += f"Total pages in PDF: {total_pages}\n"
        full_text += f"Pages processed: {pages_to_process}\n"
        full_text += f"Language: {lang}\n"
        full_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        full_text += "=" * 80 + "\n\n"

        for start in range(1, pages_to_process + 1, pages_per_batch):
            end = min(start + pages_per_batch - 1, pages_to_process)
            print(f"Processing pages {start} to {end}...")
            
            pages = pdf_to_images(pdf_path, start, end)
            for page_num, page in enumerate(pages, start=start):
                full_text += f"\n--- Page {page_num} ---\n\n"
                text = pytesseract.image_to_string(page, lang=lang)
                full_text += text + "\n"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        
        return True, pages_to_process, None
    except Exception as e:
        return False, 0, str(e)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    html_file = STATIC_FOLDER / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(), status_code=200)
    return HTMLResponse(content="<h1>PDF OCR Converter</h1><p>Frontend not found</p>", status_code=404)

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    language: str = Form('hin'),
    max_pages: int = Form(None)
):
    """Upload and process PDF file"""
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed")
    
    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        original_filename = file.filename.replace(' ', '_')
        pdf_filename = f"{file_id}_{original_filename}"
        txt_filename = f"{file_id}_{original_filename.rsplit('.', 1)[0]}.txt"
        
        pdf_path = UPLOAD_FOLDER / pdf_filename
        output_path = OUTPUT_FOLDER / txt_filename
        
        # Save uploaded file
        with pdf_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the PDF
        success, pages_processed, error = extract_text_from_pdf(
            str(pdf_path), 
            str(output_path), 
            lang=language,
            max_pages=max_pages
        )
        
        if not success:
            # Clean up files
            if pdf_path.exists():
                pdf_path.unlink()
            raise HTTPException(status_code=500, detail=f"OCR processing failed: {error}")
        
        # Clean up uploaded PDF
        if pdf_path.exists():
            pdf_path.unlink()
        
        return {
            "success": True,
            "message": f"Successfully processed {pages_processed} pages",
            "file_id": txt_filename,
            "pages_processed": pages_processed
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Download the converted text file"""
    
    file_path = OUTPUT_FOLDER / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type='text/plain'
    )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "PDF OCR Converter"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
