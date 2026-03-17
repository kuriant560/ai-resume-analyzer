"""
scorer.py
---------
Calculates the ATS (Applicant Tracking System) compatibility score
using TF-IDF vectorization and Cosine Similarity.

HOW THE SCORE WORKS:
    The final ATS score (0-100) is a weighted combination of:
    - Text Similarity Score (40%): How similar is the resume text to the JD?
    - Skill Match Score (50%):     How many required skills does the resume have?
    - Keyword Score (10%):         How well do the keywords overlap?

WHY TF-IDF + COSINE SIMILARITY (important for interviews):
    TF-IDF (Term Frequency - Inverse Document Frequency):
        - TF: How often a word appears in THIS document
        - IDF: How rare the word is across ALL documents
        - A word that appears often in resume but rarely elsewhere = important
        - Common words like "the" get low scores automatically

    Cosine Similarity:
        - Converts both texts into vectors (lists of numbers)
        - Measures the angle between the two vectors
        - Score of 1.0 = identical, 0.0 = completely different
        - Works well for text regardless of document length
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate cosine similarity between two texts using TF-IDF.

    This is the core NLP algorithm of the project.

    Args:
        text1: First text (resume)
        text2: Second text (job description)

    Returns:
        float: Similarity score between 0.0 and 1.0
    """
    if not text1 or not text2:
        return 0.0

    try:
        # Create TF-IDF vectorizer
        # ngram_range=(1,2) means we consider both single words AND pairs of words
        # "machine learning" as a phrase is more meaningful than "machine" + "learning" separately
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            max_features=5000,
        )

        # Fit and transform both texts into TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform([text1, text2])

        # Calculate cosine similarity between the two vectors
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        return round(float(similarity[0][0]), 4)

    except Exception as e:
        print(f"[scorer.py] Error calculating similarity: {e}")
        return 0.0


def calculate_keyword_score(resume_text: str, jd_text: str) -> float:
    """
    Calculate keyword overlap score between resume and job description.

    Extracts the most important keywords from the JD using TF-IDF
    and checks how many appear in the resume.

    Args:
        resume_text: Resume text
        jd_text: Job description text

    Returns:
        float: Keyword score between 0.0 and 1.0
    """
    if not resume_text or not jd_text:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=50,
        )

        # Get TF-IDF scores for JD to find its most important keywords
        jd_tfidf = vectorizer.fit_transform([jd_text])
        feature_names = vectorizer.get_feature_names_out()

        # Get top 20 keywords from JD by TF-IDF score
        scores = jd_tfidf.toarray()[0]
        top_indices = np.argsort(scores)[::-1][:20]
        top_keywords = [feature_names[i] for i in top_indices if scores[i] > 0]

        if not top_keywords:
            return 0.0

        # Check how many JD keywords appear in resume
        resume_lower = resume_text.lower()
        matched = sum(1 for kw in top_keywords if kw in resume_lower)

        return round(matched / len(top_keywords), 4)

    except Exception as e:
        print(f"[scorer.py] Error calculating keyword score: {e}")
        return 0.0


def calculate_ats_score(
        resume_text: str,
        jd_text: str,
        skill_match_percentage: float,
) -> dict:
    """
    Calculate the final ATS compatibility score (0-100).

    This is the main function that combines all scoring components
    into one final score with a detailed breakdown.

    Weights:
        - Skill Match:      50% (most important — do you have the skills?)
        - Text Similarity:  40% (does your resume language match the JD?)
        - Keyword Score:    10% (do you use the right keywords?)

    Args:
        resume_text: Raw or cleaned resume text
        jd_text: Raw or cleaned job description text
        skill_match_percentage: Percentage from skill_extractor (0-100)

    Returns:
        dict: {
            "ats_score": final score 0-100,
            "text_similarity": raw similarity 0-1,
            "skill_match_score": skill score 0-100,
            "keyword_score": keyword score 0-100,
            "breakdown": detailed score breakdown
        }
    """
    # Calculate individual components
    text_similarity = calculate_similarity(resume_text, jd_text)
    keyword_score = calculate_keyword_score(resume_text, jd_text)

    # Convert all scores to 0-100 scale
    similarity_score_100 = text_similarity * 100
    keyword_score_100 = keyword_score * 100

    # Weighted final score
    # Weights: skill match 50%, similarity 40%, keywords 10%
    ats_score = (
            (skill_match_percentage * 0.50) +
            (similarity_score_100 * 0.40) +
            (keyword_score_100 * 0.10)
    )

    ats_score = round(min(ats_score, 100), 1)

    # Determine score category for UI display
    if ats_score >= 80:
        category = "Excellent"
        color = "green"
    elif ats_score >= 60:
        category = "Good"
        color = "blue"
    elif ats_score >= 40:
        category = "Fair"
        color = "orange"
    else:
        category = "Poor"
        color = "red"

    return {
        "ats_score": ats_score,
        "category": category,
        "color": color,
        "text_similarity": round(text_similarity * 100, 1),
        "skill_match_score": round(skill_match_percentage, 1),
        "keyword_score": round(keyword_score_100, 1),
        "breakdown": {
            "skill_match_contribution": round(skill_match_percentage * 0.50, 1),
            "similarity_contribution": round(similarity_score_100 * 0.40, 1),
            "keyword_contribution": round(keyword_score_100 * 0.10, 1),
        }
    }


def generate_suggestions(
        missing_skills: list,
        ats_score: float,
        text_similarity: float,
        skill_match_percentage: float,
) -> list:
    """
    Generate personalized improvement suggestions based on the analysis.

    Args:
        missing_skills: Skills found in JD but not in resume
        ats_score: Final ATS score
        text_similarity: Text similarity score (0-100)
        skill_match_percentage: Skill match percentage (0-100)

    Returns:
        list: List of actionable suggestion strings
    """
    suggestions = []

    # Skill-based suggestions
    if missing_skills:
        top_missing = missing_skills[:5]
        suggestions.append(
            f"Add these missing skills to your resume: "
            f"{', '.join(top_missing)}"
        )

    if skill_match_percentage < 50:
        suggestions.append(
            "Your skill match is below 50%. Focus on adding more "
            "technical skills that match the job requirements."
        )

    # Similarity-based suggestions
    if text_similarity < 40:
        suggestions.append(
            "Your resume language does not closely match the job description. "
            "Try mirroring the exact keywords and phrases used in the JD."
        )

    if text_similarity < 60:
        suggestions.append(
            "Use more industry-specific terminology from the job description "
            "throughout your resume."
        )

    # ATS score suggestions
    if ats_score < 40:
        suggestions.append(
            "Your resume needs significant tailoring for this role. "
            "Rewrite your summary section to directly address the job requirements."
        )

    if ats_score < 60:
        suggestions.append(
            "Add a dedicated Skills section to your resume listing "
            "all relevant technical skills clearly."
        )

    # General suggestions always shown
    suggestions.append(
        "Use bullet points to describe achievements with measurable results "
        "(e.g., 'Improved model accuracy by 15%')."
    )

    suggestions.append(
        "Ensure your resume is in a clean, ATS-friendly format — "
        "avoid tables, columns, and images."
    )

    return suggestions