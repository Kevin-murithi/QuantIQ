const multer = require('multer');
const path = require('path');

// Configure Multer for file uploads
const upload = multer({
  dest: path.join(__dirname, '../uploads'),
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB max file size
});

// Upload handler
const uploadFiles = async (req, res) => {
  try {
    if (!req.files || req.files.length === 0) {
      return res.status(400).json({ message: 'No files uploaded' });
    }

    const uploadedFiles = req.files.map((file) => ({
      filename: file.originalname,
      filepath: file.path,
      size: file.size,
    }));

    res.status(200).json({
      message: 'Files uploaded successfully',
      files: uploadedFiles,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error uploading files', error });
  }
};

module.exports = {
  upload,
  uploadFiles,
};