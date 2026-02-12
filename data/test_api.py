import requests
import os

def test_analyze():
    url = "http://127.0.0.1:5000/analyze"
    jd = "We are looking for a Software Engineer with skills in Python, Flask, and AWS. Experience with machine learning is a plus."
    
    # Test with PDF
    resume_path = "sample_resume.pdf"
    if not os.path.exists(resume_path):
        print(f"File {resume_path} not found")
        return

    with open(resume_path, "rb") as f:
        files = {"resume": f}
        data = {"jd": jd}
        response = requests.post(url, files=files, data=data)
        
    print("PDF Analysis Result:")
    print(response.json())
    print("-" * 20)

if __name__ == "__main__":
    try:
        test_analyze()
    except Exception as e:
        print(f"Test failed: {e}")
