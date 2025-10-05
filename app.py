from flask import Flask, render_template, request, send_file, jsonify
import os
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pdf_to_images(pdf_path, start_page, end_page):
    return convert_from_path(pdf_path, first_page=start_page, last_page=end_page)

def extract_text_from_pdf(pdf_path, output_path, lang='hin', pages_per_batch=5, max_pages=None):
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
        
        return True, pages_to_process
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed'}), 400
    
    try:
        # Get form parameters
        language = request.form.get('language', 'hin')
        max_pages = request.form.get('max_pages', None)
        max_pages = int(max_pages) if max_pages and max_pages.strip() else None
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        original_filename = secure_filename(file.filename)
        pdf_filename = f"{file_id}_{original_filename}"
        txt_filename = f"{file_id}_{original_filename.rsplit('.', 1)[0]}.txt"
        
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], txt_filename)
        
        # Save uploaded file
        file.save(pdf_path)
        
        # Process the PDF
        success, result = extract_text_from_pdf(
            pdf_path, 
            output_path, 
            lang=language, 
            pages_per_batch=5, 
            max_pages=max_pages
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Successfully processed {result} pages',
                'file_id': file_id,
                'download_filename': txt_filename
            })
        else:
            # Clean up on error
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            return jsonify({'error': f'Processing failed: {result}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup/<file_id>')
def cleanup_files(file_id):
    """Clean up uploaded and processed files"""
    try:
        # Find and remove files with this file_id
        for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
            for filename in os.listdir(folder):
                if filename.startswith(file_id):
                    os.remove(os.path.join(folder, filename))
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
