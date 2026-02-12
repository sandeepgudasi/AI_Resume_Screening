# AI Resume Fit Analyzer 🚀

A professional tool to analyze how well a resume matches a job description using Machine Learning (TF-IDF & Cosine Similarity).

## 📂 Project Structure
```text
Screening_Bot/
├── core/               # AI & ML components (Similarity Scoring)
├── utils/              # Text extraction & preprocessing
├── static/             # Frontend assets (CSS, JS)
├── templates/          # UI Layouts (HTML)
├── app.py              # Main Flask server entry point
├── requirements.txt    # Project dependencies
└── README.md           # This guide
```

## 🛠️ Tech Stack
- **Backend**: Python (Flask)
- **ML Engine**: Scikit-Learn (TF-IDF Vectorization)
- **NLP**: NLTK (Text Preprocessing)
- **Frontend**: Glassmorphism CSS, Chart.js, Vanilla JS

## 🚀 Deployment Instructions

### 1. Local Run
```bash
pip install -r requirements.txt
python app.py
```

### 2. GitHub Upload
1. Initialize git: `git init`
2. Add files: `git add .`
3. Commit: `git commit -m "Initial commit"`
4. Push to your repository.

### 3. Netlify/Vercel/Render
- **Frontend**: Netlify and Vercel are great for the `static/` and `templates/` parts.
- **Backend (Recommended)**: For the full Python experience (NLP), I recommend **Render.com** or **Railway.app**. 
- Simply connect your GitHub and use the start command: `gunicorn app:app`

## 🧩 How the AI Logic Works (Hybrid Mode)
The system uses a weighted scoring method:
- **80% Weight**: Direct Keyword Matching (ensures high accuracy for technical skills).
- **20% Weight**: Semantic Cosine Similarity (evaluates the depth and context of the resume).
