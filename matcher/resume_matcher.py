import fitz  # PyMuPDF
import pandas as pd
from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize KeyBERT once
kw_model = KeyBERT()

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file."""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_keywords_text(text, num_keywords=30):
    """
    Extracts top keywords from text using KeyBERT and joins them into a single string.
    This is used for TF-IDF + Cosine similarity matching.
    """
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=num_keywords
    )
    return " ".join([kw[0] for kw in keywords])

def match_resume_with_jobs(resume_text, jobs_df=None, jobs_csv="data/rozee_jobs.csv", top_n=5):
    """
    Matches resume against job postings using a hybrid of:
    - TF-IDF on full text
    - Cosine similarity on extracted KeyBERT keywords
    """
    # Load job data
    if jobs_df is not None:
        df = jobs_df.copy()
    else:
        df = pd.read_csv(jobs_csv)

    df["combined"] = df["title"].fillna("") + " " + df["description"].fillna("")

    # -------- TF-IDF on full text --------
    documents_full = [resume_text] + df["combined"].tolist()
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents_full)
    tfidf_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # -------- KeyBERT similarity --------
    resume_keywords_text = extract_keywords_text(resume_text)
    job_keywords_texts = df["combined"].apply(extract_keywords_text).tolist()
    documents_keywords = [resume_keywords_text] + job_keywords_texts
    tfidf_kw = TfidfVectorizer()
    tfidf_kw_matrix = tfidf_kw.fit_transform(documents_keywords)
    keybert_scores = cosine_similarity(tfidf_kw_matrix[0:1], tfidf_kw_matrix[1:]).flatten()

    # -------- Combine Scores --------
    df["match_score"] = (tfidf_scores * 0.5 + keybert_scores * 0.5) * 100

    top_matches = df.sort_values(by="match_score", ascending=False).head(top_n)

    return top_matches[["title", "company", "location", "description", "match_score", "link"]]
