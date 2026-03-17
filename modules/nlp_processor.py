import spacy
from collections import Counter

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise OSError("Run: python -m spacy download en_core_web_sm")


def clean_text(text: str) -> str:
    if not text:
        return ""
    doc = nlp(text.lower())
    cleaned_tokens = []
    for token in doc:
        if (
            not token.is_stop
            and not token.is_punct
            and not token.is_space
            and len(token.lemma_) > 1
        ):
            cleaned_tokens.append(token.lemma_)
    return " ".join(cleaned_tokens)


def extract_keywords(text: str, top_n: int = 20) -> list:
    if not text:
        return []
    doc = nlp(text.lower())
    keywords = []
    for token in doc:
        if (
            token.pos_ in ("NOUN", "PROPN")
            and not token.is_stop
            and not token.is_punct
            and len(token.lemma_) > 2
        ):
            keywords.append(token.lemma_)
    keyword_counts = Counter(keywords)
    return [word for word, count in keyword_counts.most_common(top_n)]


def get_text_statistics(text: str) -> dict:
    if not text:
        return {}
    doc = nlp(text)
    return {
        "word_count": len([token for token in doc if not token.is_space]),
        "sentence_count": len(list(doc.sents)),
        "unique_words": len(set([
            token.lemma_.lower()
            for token in doc
            if not token.is_stop and not token.is_punct
        ])),
    }
