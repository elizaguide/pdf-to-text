# GitHub Setup Instructions

This project is ready to be pushed to GitHub. Follow these steps to publish it.

## Prerequisites

- GitHub account (github.com)
- Git configured on your machine:
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ```

## Setup Steps

### 1. Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `pdf-to-text`
3. Description: "Simple, reliable tool for converting PDFs to clean readable text"
4. Choose: **Public** (for open source)
5. DO NOT initialize with README (we already have one)
6. Click **Create repository**

### 2. Add Remote and Push

```bash
cd ~/Projects/pdf-to-text

# Add remote origin
git remote add origin https://github.com/YOUR_USERNAME/pdf-to-text.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### 3. Add GitHub Topics (Optional)

On GitHub repository page:
1. Click ⚙️ Settings
2. Scroll to "Repository topics"
3. Add topics:
   - `pdf`
   - `text-extraction`
   - `python`
   - `cli`
   - `pdf-parsing`

## Troubleshooting

### Authentication Issues

If you get authentication errors:

**Option A: HTTPS Token (Recommended)**
```bash
git remote set-url origin https://YOUR_GITHUB_TOKEN@github.com/YOUR_USERNAME/pdf-to-text.git
```

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when prompted

**Option B: SSH**
```bash
# Generate SSH key if needed
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to GitHub
cat ~/.ssh/id_ed25519.pub  # Copy and add to GitHub settings

# Use SSH URL
git remote set-url origin git@github.com:YOUR_USERNAME/pdf-to-text.git
```

### Verification

After pushing, verify on GitHub:
```bash
# Check remote
git remote -v
git branch -vv
```

Visit: https://github.com/YOUR_USERNAME/pdf-to-text

## Next Steps

After pushing:

1. ✅ Add repository description and URL to GitHub settings
2. ✅ Enable GitHub Actions (optional, for CI/CD)
3. ✅ Add shields/badges to README.md:
   ```markdown
   [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
   ```
4. ✅ Consider adding GitHub Issues template
5. ✅ Add Contributing guidelines (optional)

## Project Structure on GitHub

After setup, your GitHub repository will have:

```
pdf-to-text/
├── .gitignore              # Git ignore rules
├── README.md               # Project overview
├── USAGE_GUIDE.md          # Detailed usage instructions
├── CHANGELOG.md            # Version history
├── LICENSE                 # MIT License
├── GITHUB_SETUP.md         # This file
├── QUICKSTART.sh           # Setup script
├── pdf_to_text.py          # Main converter tool
├── setup.py                # Package configuration
└── requirements.txt        # Python dependencies
```

## CI/CD Setup (Optional)

To add automated testing with GitHub Actions:

1. Create `.github/workflows/test.yml`:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: python pdf_to_text.py --help
```

2. Commit and push:
```bash
git add .github/workflows/test.yml
git commit -m "Add GitHub Actions CI"
git push
```

## Sharing Your Project

Once published, share with:

- LinkedIn: "Built a PDF to text converter using Python and pdfplumber"
- Twitter/X: Share GitHub link with #python #pdf #tools
- GitHub Discussions: Invite feedback and contributions

---

**Questions?** See GitHub Docs: https://docs.github.com/en/github
