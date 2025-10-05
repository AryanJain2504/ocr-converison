// Get DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const uploadForm = document.getElementById('uploadForm');
const submitBtn = document.getElementById('submitBtn');
const status = document.getElementById('status');
const loader = document.getElementById('loader');
const downloadBtn = document.getElementById('downloadBtn');

let selectedFile = null;
let downloadFileId = null;

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

// Form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
        showStatus('Please select a PDF file', 'error');
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('language', document.getElementById('language').value);
    
    const maxPages = document.getElementById('maxPages').value;
    if (maxPages) {
        formData.append('max_pages', maxPages);
    }

    // Show processing status
    showStatus('Processing your PDF... This may take a few minutes.', 'processing');
    loader.style.display = 'block';
    submitBtn.disabled = true;
    downloadBtn.style.display = 'none';

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            downloadFileId = data.file_id;
            showStatus(`✅ ${data.message}`, 'success');
            downloadBtn.style.display = 'block';
        } else {
            // Error from server
            showStatus(`❌ Error: ${data.detail}`, 'error');
        }
    } catch (error) {
        showStatus(`❌ Network error: ${error.message}`, 'error');
    } finally {
        loader.style.display = 'none';
        submitBtn.disabled = false;
    }
});

// Download button handler
downloadBtn.addEventListener('click', () => {
    if (downloadFileId) {
        window.location.href = `/api/download/${downloadFileId}`;
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
