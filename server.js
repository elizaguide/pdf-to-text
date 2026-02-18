#!/usr/bin/env node

const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const os = require('os');

const app = express();
const port = process.env.PORT || 3000;

// Configure multer for file uploads
const upload = multer({
    dest: path.join(os.tmpdir(), 'pdf-uploads'),
    limits: { fileSize: 50 * 1024 * 1024 }, // 50MB limit
    fileFilter: (req, file, cb) => {
        if (file.mimetype === 'application/pdf') {
            cb(null, true);
        } else {
            cb(new Error('Only PDF files are allowed'));
        }
    }
});

// Serve static files from web directory
app.use(express.static(path.join(__dirname, 'web')));

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'PDF Converter API' });
});

// PDF conversion endpoint
app.post('/api/convert', upload.single('file'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file provided' });
    }

    const inputPath = req.file.path;
    const outputPath = path.join(os.tmpdir(), `${Date.now()}-output.txt`);

    try {
        // Call the Python converter
        await convertPDF(inputPath, outputPath);

        // Read the converted text
        const text = fs.readFileSync(outputPath, 'utf-8');

        // Clean up temp files
        fs.unlinkSync(inputPath);
        fs.unlinkSync(outputPath);

        res.json({
            success: true,
            text: text,
            fileName: req.file.originalname,
            size: text.length
        });
    } catch (error) {
        console.error('Conversion error:', error);
        
        // Clean up on error
        if (fs.existsSync(inputPath)) {
            fs.unlinkSync(inputPath);
        }
        if (fs.existsSync(outputPath)) {
            fs.unlinkSync(outputPath);
        }

        res.status(500).json({
            error: 'Failed to convert PDF: ' + error.message
        });
    }
});

// Run Python PDF converter
function convertPDF(inputPath, outputPath) {
    return new Promise((resolve, reject) => {
        const pythonScript = path.join(__dirname, 'pdf_converter.py');
        const venvPython = path.join(__dirname, 'venv', 'bin', 'python3');
        const pythonPath = fs.existsSync(venvPython) ? venvPython : 'python3';

        const child = spawn(pythonPath, [
            pythonScript,
            inputPath,
            '-o', outputPath
        ], {
            cwd: __dirname,
            timeout: 30000 // 30 second timeout
        });

        let stderr = '';
        
        child.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        child.on('close', (code) => {
            if (code === 0 && fs.existsSync(outputPath)) {
                resolve(outputPath);
            } else {
                reject(new Error(stderr || `Python process exited with code ${code}`));
            }
        });

        child.on('error', (error) => {
            reject(error);
        });
    });
}

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err);
    
    if (err instanceof multer.MulterError) {
        if (err.code === 'LIMIT_FILE_SIZE') {
            return res.status(413).json({ error: 'File is too large (max 50MB)' });
        }
    }
    
    res.status(500).json({
        error: err.message || 'Internal server error'
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Not found' });
});

// Start server
app.listen(port, () => {
    console.log(`
╔════════════════════════════════════════╗
║   PDF to Text Converter - Web Server   ║
╠════════════════════════════════════════╣
║  🌐 Server running at:                 ║
║     http://localhost:${port}${' '.repeat(Math.max(0, 27-port.toString().length))}║
║                                        ║
║  📤 Upload endpoint: /api/convert      ║
║  🌍 Web UI: http://localhost:${port}${' '.repeat(Math.max(0, 23-port.toString().length))}║
╚════════════════════════════════════════╝
    `);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('Shutting down gracefully...');
    process.exit(0);
});
