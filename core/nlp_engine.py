from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from utils.utils import clean_text

class ResumeAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def calculate_similarity(self, resume_text, jd_text):
        """
        Calculates a hybrid similarity score between resume and job description.
        Combines keyword matching (80%) and TF-IDF cosine similarity (20%).
        """
        cleaned_resume = clean_text(resume_text)
        cleaned_jd = clean_text(jd_text)
        
        if not cleaned_resume or not cleaned_jd:
            return 0.0

        tfidf_matrix = self.vectorizer.fit_transform([cleaned_resume, cleaned_jd])
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        gap = self.analyze_gap(resume_text, jd_text)
        jd_skills = self.extract_skills(jd_text)
        
        if not jd_skills:
            return round(float(cosine_sim) * 100, 2)
            
        keyword_score = len(gap['matched']) / len(jd_skills)
        hybrid_score = (keyword_score * 0.8) + (cosine_sim * 0.2)
        
        return round(float(hybrid_score) * 100, 2)

    def extract_skills(self, text):
        common_skills = {
            "python", "java", "javascript", "react", "angular", "vue", "node.js", 
            "express", "flask", "django", "sql", "nosql", "mongodb", "postgresql",
            "aws", "azure", "docker", "kubernetes", "machine learning", "nlp",
            "data science", "tableau", "power bi", "excel", "html", "css",
            "typescript", "c++", "c#", "php", "swift", "kotlin", "ruby", "rails",
            "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy", "git",
            "ci/cd", "agile", "scrum", "project management", "leadership",
            "communication", "problem solving", "teamwork", "analytical", "fastapi",
            "rest api", "graphql", "devops", "cloud computing", "linux", "snowflake",
            "databricks", "spark", "hadoop", "c", "mysql", "oracle", "redux", "tailwinds"
        }
        
        text = text.lower()
        found_skills = []
        for skill in common_skills:
            if re.search(rf'\b{re.escape(skill)}\b', text):
                found_skills.append(skill)
        return found_skills

    def analyze_gap(self, resume_text, jd_text):
        jd_skills = self.extract_skills(jd_text)
        resume_skills = self.extract_skills(resume_text)
        matched_skills = [s for s in jd_skills if s in resume_skills]
        missing_skills = [s for s in jd_skills if s not in resume_skills]
        return {"matched": matched_skills, "missing": missing_skills}

    def generate_feedback(self, score, gap_analysis):
        missing_count = len(gap_analysis['missing'])
        explanation = ""
        suggestions = []
        status = ""
        
        if score > 70:
            status = "SELECTED"
            explanation = f"Great news! With a match score of {score}%, your resume is highly compatible with this role."
            suggestions = ["Prepare for technical interviews.", "Highlight your achievements."]
        elif score > 40:
            status = "THINKING"
            explanation = f"Your resume has a decent match ({score}%), but it might not stand out."
            suggestions = [f"Add experience with: {', '.join(gap_analysis['missing'][:2])}."]
        else:
            status = "REJECTED"
            explanation = f"Unfortunately, your match score is quite low ({score}%)."
            suggestions = ["Work on projects that use the missing skills."]
            
        if missing_count > 0 and status != "SELECTED":
            suggestions.append(f"Add {', '.join(gap_analysis['missing'][:2])} to your skills section.")
            
        return explanation, suggestions, status
