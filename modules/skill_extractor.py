"""
skill_extractor.py
------------------
Extracts skills from resume and job description text by matching
against our curated skills database.

HOW IT WORKS:
    1. Takes cleaned text as input
    2. Checks if each skill from our database appears in the text
    3. Returns matched skills as a list

WHY KEYWORD MATCHING INSTEAD OF ML:
    For a portfolio project, keyword matching is transparent and explainable.
    You can tell an interviewer exactly how it works.
    A future improvement would be using word embeddings for fuzzy matching.
"""

import sys
import os

# Add the project root to path so we can import from data/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.skills_db import TECHNICAL_SKILLS, SOFT_SKILLS, ALL_SKILLS


def extract_skills(text: str, skill_list: list = None) -> list:
    """
    Extract skills from text by matching against a skills database.

    Args:
        text: Cleaned or raw text to search through
        skill_list: Custom list of skills to match against.
                   Defaults to ALL_SKILLS from skills_db.

    Returns:
        list: Sorted list of skills found in the text
    """
    if not text:
        return []

    if skill_list is None:
        skill_list = ALL_SKILLS

    text_lower = text.lower()
    found_skills = []

    for skill in skill_list:
        # Check if skill appears as a whole word/phrase in the text
        # This prevents "r" matching "research" for example
        if f" {skill} " in f" {text_lower} ":
            found_skills.append(skill)

    return sorted(found_skills)


def extract_technical_skills(text: str) -> list:
    """Extract only technical skills from text."""
    return extract_skills(text, TECHNICAL_SKILLS)


def extract_soft_skills(text: str) -> list:
    """Extract only soft skills from text."""
    return extract_skills(text, SOFT_SKILLS)


def get_skill_match(resume_text: str, jd_text: str) -> dict:
    """
    Compare skills between resume and job description.

    This is the core comparison function. It finds:
    - Skills in BOTH resume and JD (matched skills)
    - Skills in JD but NOT in resume (missing skills = skill gap)
    - Skills in resume but NOT in JD (extra skills)

    Args:
        resume_text: Raw or cleaned resume text
        jd_text: Raw or cleaned job description text

    Returns:
        dict: {
            "resume_skills": all skills found in resume,
            "jd_skills": all skills required by job description,
            "matched_skills": skills present in both,
            "missing_skills": skills in JD but not in resume,
            "extra_skills": skills in resume but not in JD,
            "match_percentage": percentage of JD skills covered
        }
    """
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills - resume_skills
    extra_skills = resume_skills - jd_skills

    # Calculate match percentage
    # How many of the JD's required skills does the resume cover?
    if len(jd_skills) > 0:
        match_percentage = (len(matched_skills) / len(jd_skills)) * 100
    else:
        match_percentage = 0.0

    return {
        "resume_skills": sorted(list(resume_skills)),
        "jd_skills": sorted(list(jd_skills)),
        "matched_skills": sorted(list(matched_skills)),
        "missing_skills": sorted(list(missing_skills)),
        "extra_skills": sorted(list(extra_skills)),
        "match_percentage": round(match_percentage, 2),
    }