// Sidebar opening/closing
const toggler = document.querySelector('.toggler');

toggler.addEventListener('click', () => {
  document.querySelector('.skeleton').classList.toggle('active');
})


// Dropdown
const dropdownBtn = document.querySelector(".dropdown-btn");
const pBoxReveal = document.querySelector(".p-box-reveal");

dropdownBtn.addEventListener("click", () => {
  pBoxReveal.classList.toggle("hidden");
  dropdownBtn.classList.toggle("spin");
});


// Reusable file upload modal
const modal = document.getElementById('data-ingestion-modal');
const openModalBtn = document.getElementById('open-modal-btn');
const fileInput = document.getElementById('file-input');
const uploadArea = document.getElementById('upload-area');
const uploadMessage = document.getElementById('upload-message');
const resetButton = document.getElementById('reset-button');
const dynamic_upload_state = document.querySelector('.dynamic_upload_state');
openModalBtn.addEventListener('click', openModal);

function openModal() {
  modal.showModal();
}

function closeModal() {
  modal.close();
}

// Reset functionality
function resetUploadArea() {
  fileInput.value = ''; // Clear file input
  resetButton.style.display = 'none'; // Hide the reset button
  uploadMessage.textContent = 'Drag & Drop your file(s) here'; // Reset message
}

uploadArea.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadArea.classList.remove('dragging');
  const files = e.dataTransfer.files;
  handleFileSelection({ target: { files } });
});

// Track selected files
let selectedFiles = [];

function resetUploadArea() {
  fileInput.value = ''; // Clear file input
  selectedFiles = []; // Clear selected files
  resetButton.style.display = 'none'; // Hide the reset button
  uploadMessage.textContent = 'Drag & Drop your file(s) here'; // Reset message
  dynamic_upload_state.innerHTML = `
    <p id="upload-message">Drag & Drop your file(s) here</p>
    <button class="browse_local" onclick="document.getElementById('file-input').click()">Browse Files</button>
  `;
  dynamic_upload_state.style = `margin-top: 1.25rem`;
}

function handleFileSelection(event) {
  const files = event.target.files;
  if (files.length === 0) return;

  selectedFiles = [...files]; // Store selected files
  resetButton.style.display = 'block'; // Show the reset button
  renderFileList();
}

function renderFileList() {
  const fileList = document.createElement('ol');
  fileList.style = `
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: start;
    padding: .75rem .5rem;
    border: 1.5px solid #ccc;
    border-radius: 8px;
    width: 95%;
    margin-top: .75rem;
  `;

  selectedFiles.forEach((file, index) => {
    const listItem = document.createElement('li');
    listItem.style = `
      margin: .35rem 0;
      font-size: 14px;
      opacity: .75;
      display: flex;
      justify-content: space-between;
      align-items: center;
    `;
    listItem.innerHTML = `
      ${file.name}
      <button 
        onclick="removeFile(${index})" 
        style="background: none; border: none; color: red; cursor: pointer; font-size: 12px; margin-left: 10px;">
        Remove
      </button>
    `;
    fileList.appendChild(listItem);
  });

  dynamic_upload_state.innerHTML = ''; // Clear upload area
  dynamic_upload_state.appendChild(fileList);
  dynamic_upload_state.style = `margin-top: 0`;
}

function removeFile(index) {
  selectedFiles.splice(index, 1); // Remove file at index
  if (selectedFiles.length === 0) {
    resetUploadArea(); // Reset if no files remain
  } else {
    renderFileList(); // Re-render list
  }
}

uploadArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadArea.classList.add('dragging');
});

uploadArea.addEventListener('dragleave', () => {
  uploadArea.classList.remove('dragging');
});

uploadArea.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadArea.classList.remove('dragging');
  const files = e.dataTransfer.files;
  handleFileSelection({ target: { files } });
});

async function uploadFiles() {
  if (selectedFiles.length === 0) {
    alert('Please select files to upload');
    return;
  }

  const formData = new FormData();
  selectedFiles.forEach((file) => formData.append('files', file));

  try {
    const response = await fetch('http://localhost:3000/upload', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      alert('Files uploaded successfully');
      closeModal();
    } else {
      alert('Failed to upload files');
    }
  } catch (error) {
    console.error(error);
    alert('An error occurred during file upload');
  }
}