# Quick Start Guide

## PDF OCR Converter - FastAPI Web App

### Server is Running! 🎉

The FastAPI server is now running at: **http://localhost:8000**

### What You Can Do:

1. **Web Interface**
   - Open your browser: http://localhost:8000
   - Upload a PDF file (drag & drop or click to browse)
   - Select language (Hindi, English, etc.)
   - Set max pages for testing (optional)
   - Click "Convert to Text"
   - Download your converted text file

2. **API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### API Endpoints:

- `GET /` - Main web interface
- `POST /api/upload` - Upload and process PDF
- `GET /api/download/{filename}` - Download converted text file
- `GET /api/health` - Health check endpoint

### Supported Languages:

- English (eng)
- Hindi (hin) - Default
- English + Hindi (eng+hin)
- Sanskrit (san)
- Marathi (mar)
- Bengali (ben)
- Tamil (tam)
- Telugu (tel)

### Testing Tips:

- Start with a small page limit (e.g., 5-10 pages) for testing
- Larger PDFs will take longer to process
- Files are automatically cleaned up after processing

### Tech Stack:

- **Backend**: FastAPI + Uvicorn
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **OCR Engine**: Tesseract OCR
- **PDF Processing**: pdf2image, PyPDF2

---

**To stop the server**: Press `CTRL+C` in the terminal

**To restart**: Run `python api.py` again
