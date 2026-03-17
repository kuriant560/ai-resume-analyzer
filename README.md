# 📄 AI Resume Analyzer

An intelligent web application that analyzes your resume against a job description using NLP to provide ATS scoring, skill gap analysis, and improvement suggestions.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![spaCy](https://img.shields.io/badge/spaCy-3.7-green)

---

## 🚀 Features

- ✅ PDF resume parsing
- ✅ ATS compatibility score (0–100)
- ✅ Skill match & gap analysis
- ✅ Keyword analysis (TF-IDF)
- ✅ Visual dashboard with charts
- ✅ Personalized improvement suggestions

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| UI Framework | Streamlit |
| NLP | spaCy |
| Similarity | TF-IDF + Cosine Similarity |
| PDF Parsing | PyPDF2 |
| Visualization | Plotly / Matplotlib |

---

## ⚙️ Setup
```bash
git clone https://github.com/kuriant560/ai-resume-analyzer.git
cd ai-resume-analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

---

## 📁 Project Structure
```
ai-resume-analyzer/
├── app.py                  # Streamlit UI entry point
├── requirements.txt        # Dependencies
├── modules/
│   ├── parser.py           # PDF text extraction
│   ├── nlp_processor.py    # spaCy text processing
│   ├── skill_extractor.py  # Skill matching
│   ├── scorer.py           # ATS score calculation
│   ├── gap_analyzer.py     # Skill gap analysis
│   └── visualizer.py       # Charts and plots
└── data/
    └── skills_db.py        # Skills database
```

---

## 👤 Author

**Kurian** · [GitHub](https://github.com/kuriant560)

---

## 📄 License

MIT License