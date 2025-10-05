// Set up PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

// Get DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const uploadForm = document.getElementById('uploadForm');
const submitBtn = document.getElementById('submitBtn');
const status = document.getElementById('status');
const loader = document.getElementById('loader');
const downloadBtn = document.getElementById('downloadBtn');
const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

let selectedFile = null;
let extractedText = '';

// Click to select file
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// File selection handler
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        selectedFile = e.target.files[0];
        fileName.textContent = `Selected: ${selectedFile.name}`;
        hideStatus();
        downloadBtn.style.display = 'none';
    }
});

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'application/pdf') {
            selectedFile = file;
            fileInput.files = files;
            fileName.textContent = `Selected: ${file.name}`;
            hideStatus();
            downloadBtn.style.display = 'none';
        } else {
            showStatus('Please select a PDF file', 'error');
        }
    }
});

// Update progress
function updateProgress(percent, text) {
    progressFill.style.width = percent + '%';
    progressText.textContent = text || (percent + '%');
}

// Form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
        showStatus('Please select a PDF file', 'error');
        return;
    }

    const language = document.getElementById('language').value;
    const maxPages = document.getElementById('maxPages').value;

    // Show processing status
    showStatus('Processing your PDF... This may take a few minutes.', 'processing');
    loader.style.display = 'block';
    progressContainer.style.display = 'block';
    submitBtn.disabled = true;
    downloadBtn.style.display = 'none';
    extractedText = '';

    try {
        // Read PDF file
        const arrayBuffer = await selectedFile.arrayBuffer();
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        const totalPages = pdf.numPages;
        const pagesToProcess = maxPages ? Math.min(parseInt(maxPages), totalPages) : totalPages;

        updateProgress(0, 'Loading Tesseract...');

        // Initialize Tesseract
        const worker = await Tesseract.createWorker(language);

        // Add header to extracted text
        extractedText = `OCR Extraction Results\n`;
        extractedText += `Total pages in PDF: ${totalPages}\n`;
        extractedText += `Pages processed: ${pagesToProcess}\n`;
        extractedText += `Language: ${language}\n`;
        extractedText += `Date: ${new Date().toLocaleString()}\n`;
        extractedText += '='.repeat(80) + '\n\n';

        // Process each page
        for (let pageNum = 1; pageNum <= pagesToProcess; pageNum++) {
            const percent = Math.round((pageNum / pagesToProcess) * 100);
            updateProgress(percent, `Processing page ${pageNum} of ${pagesToProcess}...`);

            const page = await pdf.getPage(pageNum);
            
            // Render page to canvas
            const scale = 2.0;
            const viewport = page.getViewport({ scale });
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            await page.render({
                canvasContext: context,
                viewport: viewport
            }).promise;

            // Perform OCR on the canvas
            const { data: { text } } = await worker.recognize(canvas);
            
            extractedText += `\n--- Page ${pageNum} ---\n\n`;
            extractedText += text + '\n';

            // Clean up canvas
            canvas.remove();
        }

        // Terminate worker
        await worker.terminate();

        // Success
        updateProgress(100, 'Complete!');
        showStatus(`✅ Successfully processed ${pagesToProcess} pages!`, 'success');
        downloadBtn.style.display = 'block';

    } catch (error) {
        console.error('Error:', error);
        showStatus(`❌ Error: ${error.message}`, 'error');
    } finally {
        loader.style.display = 'none';
        submitBtn.disabled = false;
        setTimeout(() => {
            progressContainer.style.display = 'none';
        }, 2000);
    }
});

// Download button handler
downloadBtn.addEventListener('click', () => {
    if (extractedText) {
        const blob = new Blob([extractedText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = selectedFile.name.replace('.pdf', '_extracted.txt');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showStatus('✅ Download started!', 'success');
    }
});

// Helper functions
function showStatus(message, type) {
    status.textContent = message;
    status.className = 'status ' + type;
}

function hideStatus() {
    status.className = 'status';
    status.style.display = 'none';
}
