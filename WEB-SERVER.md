# PDF to Text Web Server 🌐

Beautiful, browser-based PDF to text converter with drag-and-drop interface.

## Features ✨

- **Drag & Drop Upload** - Simply drop PDFs into the browser
- **Live Conversion** - Fast, client-side processing
- **Download as .txt** - Export converted text instantly
- **Dual Extraction Engines** - pdfplumber + PyPDF2 fallback
- **Encoding Cleanup** - Fixes PDF artifacts automatically
- **100% Private** - All processing happens on your machine
- **Responsive Design** - Works on desktop and mobile

## Quick Start 🚀

### 1. One-Command Setup

```bash
cd /Users/vishen/clawd/pdf-to-text
./setup-web.sh
```

This will:
- ✅ Check for Node.js (install from nodejs.org if needed)
- ✅ Install Node dependencies (express, multer)
- ✅ Setup Python virtual environment
- ✅ Install Python dependencies (PyPDF2, pdfplumber)

### 2. Start the Server

```bash
npm start
```

You'll see:
```
╔════════════════════════════════════════╗
║   PDF to Text Converter - Web Server   ║
╠════════════════════════════════════════╣
║  🌐 Server running at:                 ║
║     http://localhost:3000              ║
╚════════════════════════════════════════╝
```

### 3. Open in Browser

Navigate to: **http://localhost:3000**

## Usage 📖

### Browser Interface

1. **Drag and Drop** - Drag a PDF file onto the purple box
2. **Or Click** - Click to browse and select a PDF file
3. **Wait** - Conversion happens instantly
4. **Download** - Click "Download as .txt" to save the text

### Features

- **Live Preview** - See the first 500 characters as you convert
- **Character Count** - Shows total characters in converted text
- **Full Text** - Scroll to view the entire conversion
- **Convert Another** - Process multiple files in one session

## Advanced Usage 🔧

### API Endpoint

Convert PDFs programmatically via the API:

```bash
curl -X POST http://localhost:3000/api/convert \
  -F "file=@document.pdf"
```

Response:
```json
{
  "success": true,
  "text": "Extracted text...",
  "fileName": "document.pdf",
  "size": 5234
}
```

### Configuration

Set custom port:
```bash
PORT=8080 npm start
```

### Development Mode

```bash
npm run dev
```

## Troubleshooting 🆘

### Port Already in Use

If port 3000 is already in use:
```bash
PORT=3001 npm start
```

Then open: `http://localhost:3001`

### Python Dependencies Missing

Re-run the setup:
```bash
./setup-web.sh
```

### Large Files

Max file size is 50MB. For larger files, use the CLI:
```bash
/Users/vishen/clawd/pdf-to-text/convert-pdf huge-document.pdf
```

## Files 📁

```
pdf-to-text/
├── web/
│   └── index.html          # Web UI (drag & drop interface)
├── server.js               # Express server
├── pdf_converter.py        # Python PDF extraction
├── package.json            # Node dependencies
├── requirements.txt        # Python dependencies
├── setup-web.sh            # Auto-setup script
└── venv/                   # Python virtual environment
```

## Technical Details 🛠️

**Frontend:**
- Pure HTML/CSS/JavaScript (no frameworks)
- Responsive design with gradient UI
- Drag & drop file handling
- Real-time character counting

**Backend:**
- Node.js + Express server
- Multer for file uploads
- Python subprocess for PDF parsing
- Temp file cleanup

**PDF Processing:**
- Dual extraction engines (pdfplumber first, PyPDF2 fallback)
- Encoding artifact cleanup
- Support for complex PDF layouts
- Error recovery and graceful fallbacks

## Deployment 🌍

### Deploy to Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Deploy to Heroku

```bash
heroku login
heroku create
git push heroku main
```

### Docker

Create a `Dockerfile`:
```dockerfile
FROM node:18-slim
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY . .
RUN npm install
RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["npm", "start"]
```

Build and run:
```bash
docker build -t pdf-converter .
docker run -p 3000:3000 pdf-converter
```

## License

MIT - Created for Vishen Lakhiani

---

**Questions?** Check out the main [README.md](./README.md) or reach out! 💜
