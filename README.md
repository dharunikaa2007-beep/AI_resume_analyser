# AI Resume Analyzer & Role Matcher

An AI-driven career advisor and automated resume evaluation system. The application parses candidate resumes, strips Personally Identifiable Information (PII) to ensure algorithmic fairness, extracts technical competencies, and calculates hybrid match scores against predefined industry role profiles.

---

## Key Features

- **Document Parsing & Ingestion:** Supports single and multi-page resumes in PDF or plain text formats.
- **PII Scrubbing:** Neutralizes personal identifiers (e.g., email addresses, phone numbers, protected demographic metadata) prior to model evaluation.
- **Lexical & Semantic Matching:** Computes a hybrid score combining exact domain skill coverage (60%) and dense TF-IDF cosine similarity (40%).
- **Skill Gap Analysis:** Displays matched proficiencies and identifies missing competencies required for target tracks.
- **Interactive Visualizations:** Renders comparative match scores and candidate insights using Streamlit and Plotly.

---

## Directory Structure

```text
resume-analyzer/
├── app.py                     # Streamlit web application & core pipeline
├── requirements.txt           # Project dependencies
├── data/
│   ├── job_roles.json         # Predefined target role descriptions & skills
│   └── skills.json            # Master skill dictionary taxonomy
├── sample_resumes/            # Anonymized sample resumes for testing
│   ├── Resume_A_Data_Analyst.pdf
│   ├── Resume_B_ML_Engineer.pdf
│   └── Resume_C_NLP_Engineer.pdf
└── docs/
    ├── Architecture_Workflow_Diagram.png
    └── Testing_Evaluation_Sheet.xlsx
