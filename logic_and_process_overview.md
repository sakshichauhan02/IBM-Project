AI Hiring Copilot: Logic & Process Overview

This document provides a detailed breakdown of the internal logic, data flow, and processing steps used by the AI Hiring Copilot to rank resumes against job descriptions (JDs).

---

1. System Architecture
The application is built with a modular architecture, separating the UI from the core processing logic:

| Component | Responsibility | Key File |
| :--- | :--- | :--- |
| **Frontend** | Streamlit-based UI for file uploads, JD input, and results display. | [`app.py`](file:///c:/Users/dell/OneDrive/Desktop/IBM/app.py) |
| **Extraction** | Converts raw PDF content into searchable text using `pdfplumber`. | [`utils/parser.py`](file:///c:/Users/dell/OneDrive/Desktop/IBM/utils/parser.py) |
| **Preprocessing** | Cleans and normalizes text for NLP tasks using `spaCy`. | [`utils/preprocess.py`](file:///c:/Users/dell/OneDrive/Desktop/IBM/utils/preprocess.py) |
| **Matching** | Calculates semantic similarity using TF-IDF and Cosine Similarity. | [`utils/matcher.py`](file:///c:/Users/dell/OneDrive/Desktop/IBM/utils/matcher.py) |
| **Skill Engine** | Extracts, compares, and scores predefined technical skills. | [`utils/skills.py`](file:///c:/Users/dell/OneDrive/Desktop/IBM/utils/skills.py) |

---
2. The Processing Pipeline
Every time a user uploads resumes and provides a Job Description, the following sequence occurs:

Phase A: Job Description (JD) Analysis
1. **Cleaning**: The JD text is passed through the NLP preprocessor.
   - Stopwords (e.g., "and", "the") are removed.
   - Punctuation and extra whitespace are stripped.
   - Words are **lemmatized** (e.g., "working" → "work") to ensure consistency.
2. **Skill Extraction**: The system scans the JD for predefined technical keywords (Python, SQL, Machine Learning, etc.) using case-insensitive regex matching.

Phase B: Candidate Processing (Per Resume)
For each uploaded PDF, the system performs:
1. **Text Extraction**: Extracts all readable text from the PDF pages.
2. **Text Cleaning**: Applies the same lemmatization and cleaning used for the JD.
3. **Semantic Scoring**:
   - Converts both the cleaned Resume and JD into **TF-IDF Vectors**.
   - Calculates the **Cosine Similarity** between these vectors (0.0 to 1.0).
   - This represents how well the *context* and *language* of the resume match the JD.
4. **Skill Matching**:
   - Extracts technical skills found in the resume.
   - Compares them against the list of skills required by the JD.
   - Identifies "Matched Skills" and "Missing Skills".

---

 3. Scoring & Ranking Logic

Core Scoring Mechanism
The final ranking is determined by a **Hybrid Score** (0-100%), calculated as follows:

$$ \text{Final Score} = (\text{Semantic Score} \times 0.7) + (\text{Skill Match Score} \times 0.3) $$

*   **70% Weight (Semantic):** Focuses on the overall profile relevance, experience depth, and context.
*   **30% Weight (Skills):** Focuses on the specific technical keywords required for the role.

---

4. Explanation Generation
The "AI Explanation" for each candidate is generated using a rule-based engine:

1. **Skill Evaluation**:
   - `> 70%`: "Strong alignment in core skills"
   - `> 40%`: "Moderate alignment in skills"
   - `< 40%`: "Limited skill match"
2. **Context Evaluation**: Refines the explanation based on whether the Semantic Score is high (contextual relevance) or low.
3. **Specific Highlights**: The top 2 matched skills and top 2 missing skills are explicitly named to provide actionable feedback.

---- **PDF Processing**: [pdfplumber](https://github.com/jsvine/pdfplumber)
- **Regex**: [re](https://docs.python.org/3/library/re.html) (for precision keyword matching)
