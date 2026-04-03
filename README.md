# 📄 AI-Driven Resume Intelligence System
**Automated Information Extraction & Skill-Gap Analysis**

An intelligent recruitment tool designed to transform unstructured PDF/Docx resumes into standardized, actionable data. This project leverages **Natural Language Processing (NLP)** to understand context and extract key professional entities with high precision.

---

### ✨ Key Features
* **Named Entity Recognition (NER):** Extracts Names, Contact Info, Universities, and Job Titles using `spaCy`.
* **Skill-Gap Analysis:** Automatically compares extracted skills against Job Descriptions (JD) to provide a compatibility score.
* **Structured Data Output:** Converts messy resume text into clean, validated JSON format.
* **Interactive Dashboard:** Built with `Streamlit` for a seamless user experience for both recruiters and candidates.

---

### 🛠️ Tech Stack
* **Language:** Python 3.9+
* **NLP Engine:** spaCy (en_core_web_lg)
* **Framework:** Streamlit (Frontend & UI)
* **Libraries:** PyMuPDF (PDF parsing), Pandas (Data handling), Pydantic (Data validation)

---

### 📊 How it Works
1. **Document Ingestion:** Uses `PyMuPDF` to extract raw text from uploaded resumes.
2. **Entity Extraction:** Processes text through an NLP pipeline to identify professional entities.
3. **Keyword Matching:** Utilizes a custom skill-set dictionary to categorize technical and soft skills.
4. **Scoring Engine:** Calculates a match percentage based on JD requirements.

---

### 🚀 Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/AshitaSharma01/AI-Resume-Parser.git](https://github.com/AshitaSharma01/ResumeIQ.git)
