from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, jd_text):
    """
    Compute cosine similarity between resume and job description using TF-IDF.
    Returns:
        int: Match percentage (0-100)
    """
    if not resume_text or not jd_text:
        return 0

    # Vectorize the documents
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])

    # Compute similarity between the two documents
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    # Convert similarity (0 to 1) to percentage (0 to 100)
    return round(similarity[0][0] * 100)
