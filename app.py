import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from utils.utils import extract_text_from_pdf, extract_text_from_docx
from core.nlp_engine import ResumeAnalyzer

app = Flask(__name__, template_folder='.')

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

analyzer = ResumeAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files or 'jd' not in request.form:
        return jsonify({"error": "Missing resume or job description"}), 400
    
    file = request.files['resume']
    jd_text = request.form['jd']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and jd_text:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        ext = filename.rsplit('.', 1)[1].lower()
        if ext == 'pdf':
            resume_text = extract_text_from_pdf(file_path)
        elif ext in ['docx', 'doc']:
            resume_text = extract_text_from_docx(file_path)
        else:
            return jsonify({"error": "Unsupported file format"}), 400
        
        score = analyzer.calculate_similarity(resume_text, jd_text)
        gap = analyzer.analyze_gap(resume_text, jd_text)
        explanation, suggestions, status = analyzer.generate_feedback(score, gap)
        
        os.remove(file_path)
        
        return jsonify({
            "score": score,
            "matched_skills": gap['matched'],
            "missing_skills": gap['missing'],
            "explanation": explanation,
            "suggestions": suggestions,
            "status": status
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

