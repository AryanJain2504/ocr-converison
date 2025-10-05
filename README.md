# PDF OCR Converter

A modern web application to convert PDF documents to text using OCR (Optical Character Recognition) technology.

## 🌐 Live Demo

**GitHub Pages (Client-Side):** `https://aryanjain2504.github.io/ocr-converison/`

> The GitHub Pages version runs entirely in your browser - no server needed!

## Features

- � **FastAPI Backend** - High-performance async API
- 💅 **Modern UI** - Clean HTML/CSS/JavaScript interface
- � **Multi-language Support** - Hindi, English, Sanskrit, Marathi, Bengali, Tamil, Telugu
- 📤 **Drag & Drop Upload** - Easy file upload with drag-and-drop
- ⚡ **Fast Processing** - Process PDFs in batches
- 📥 **Direct Download** - Download converted text files instantly
- � **Page Limits** - Process specific number of pages for testing

## Prerequisites

Make sure you have the following installed:

1. **Python 3.8+**
2. **Poppler** (for PDF processing)
   ```bash
   brew install poppler
   ```

3. **Tesseract OCR** with language packs
   ```bash
   brew install tesseract
   brew install tesseract-lang
   ```

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/aryan/code/ocr
   ```

2. **Create a virtual environment (if not already created):**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Web Application (FastAPI)

1. **Start the FastAPI server:**
   ```bash
   python api.py
   ```
   
   Or use uvicorn directly:
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open your web browser and navigate to:**
   ```
   http://localhost:8000
   ```

3. **Upload and convert:**
   - Click the upload area or drag-and-drop a PDF file
   - Select your preferred language (Hindi, English, Sanskrit, etc.)
   - Optionally set a page limit for testing
   - Click "Convert to Text"
   - Wait for processing (may take a few minutes)
   - Download the extracted text file

4. **API Documentation:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Running the Command-Line Script

For direct command-line usage, use `main.py`:

```bash
python main.py
```

Edit the configuration in `main.py` to set your input/output paths and options.

## Configuration

### Web App Settings (app.py)

- `MAX_FILE_SIZE`: Maximum upload size (default: 50MB)
- `UPLOAD_FOLDER`: Temporary storage for uploaded PDFs
- `OUTPUT_FOLDER`: Storage for converted text files

### CLI Settings (main.py)

- `PDF_PATH`: Input PDF file path
- `OUTPUT_PATH`: Output text file path
- `LANG`: OCR language ('hin', 'eng', or 'hin+eng')
- `PAGES_PER_BATCH`: Pages to process at once (default: 5)
- `MAX_PAGES`: Limit pages for testing (set to None for all pages)

## Supported Languages

Current language options:
- `hin`: Hindi (हिन्दी)
- `eng`: English
- `hin+eng`: Hindi + English (both)

To see all installed languages:
```bash
tesseract --list-langs
```

## Project Structure

```
ocr/
├── app.py                 # Flask web application
├── main.py               # Command-line script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # HTML templates
│   └── index.html       # Web UI
├── uploads/             # Temporary PDF storage (auto-created)
├── outputs/             # Converted text files (auto-created)
└── venv/               # Virtual environment
```

## Troubleshooting

### "tesseract is not installed"
```bash
brew install tesseract tesseract-lang
```

### "poppler is not installed"
```bash
brew install poppler
```

### "Port 5000 already in use"
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Import errors
Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Performance Tips

- Start with `MAX_PAGES=10` for testing large PDFs
- Use `PAGES_PER_BATCH=5` for balanced memory/speed
- Clear `uploads/` and `outputs/` folders periodically
- For better accuracy, ensure PDF quality is good

## 🚀 GitHub Pages Deployment

### Enable GitHub Pages:

1. **Push your code:**
   ```bash
   git add .
   git commit -m "Add GitHub Pages version"
   git push origin master
   ```

2. **Configure GitHub Pages:**
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under **Source**, select branch: `master`
   - Under **Folder**, select: `/docs`
   - Click **Save**

3. **Access your site:**
   - URL: `https://aryanjain2504.github.io/ocr-converison/`
   - Wait 1-2 minutes for deployment

### Differences: Client-Side vs Server-Side

| Feature | GitHub Pages (Client) | Local Server |
|---------|----------------------|--------------|
| Processing | Browser (Tesseract.js) | Server (Python Tesseract) |
| Privacy | 100% local | Files uploaded to server |
| Speed | Slower | Faster |
| Installation | None needed | Requires Python, Tesseract, Poppler |
| Hosting | Free on GitHub | Requires server |

## 📁 Project Structure

```
ocr/
├── docs/                  # GitHub Pages version (client-side)
│   ├── index.html
│   ├── script.js         # Uses Tesseract.js
│   └── styles.css
├── static/               # Server version files
│   ├── index.html
│   ├── script.js         # Calls FastAPI
│   └── styles.css
├── api.py               # FastAPI backend
├── main.py              # Standalone script
└── requirements.txt
```

## 🙏 Technologies

- **Tesseract.js** - Client-side OCR
- **PDF.js** - PDF parsing
- **FastAPI** - Python backend
- **Tesseract OCR** - Server OCR engine

## 👤 Author

**Aryan Jain**  
GitHub: [@AryanJain2504](https://github.com/AryanJain2504)

## License

Free to use for personal and commercial projects.
