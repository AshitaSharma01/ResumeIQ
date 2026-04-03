# 🧠 AI-Resume-Parser
### Intelligent Resume Parsing & Skill Analytics — Powered by spaCy NLP

> Transform unstructured PDF/DOCX resumes into clean, structured data with AI-driven entity extraction and skill frequency analysis.

---

## ✨ Features

- **Named Entity Recognition** — Extracts candidate names using spaCy's NLP pipeline
- **Smart Contact Extraction** — Detects emails and phone numbers with precision regex
- **Skill Detection** — Matches 20+ technical skills across Python, ML, AI, Cloud, and more
- **Skill Frequency Analytics** — Visual bar and pie charts showing skill distribution
- **Batch Processing** — Upload and parse multiple resumes at once
- **CSV Export** — Download all parsed data as a structured report
- **Interactive Dashboard** — Clean, dark-themed Streamlit UI for recruiters

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.9+ |
| NLP Engine | spaCy (`en_core_web_sm`) |
| PDF Parsing | pdfplumber |
| DOCX Parsing | docx2txt |
| Frontend/UI | Streamlit |
| Data Handling | Pandas |
| Charts | Plotly |

---

## 📸 Demo

![Dashboard Preview](https://via.placeholder.com/800x400?text=ResumeIQ+Dashboard)

Upload resumes → AI parses instantly → View skill analytics → Export CSV

---

## 🚀 Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/AshitaSharma01/AI-Resume-Parser.git
cd AI-Resume-Parser
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Download spaCy model**
```bash
python -m spacy download en_core_web_sm
```

**5. Run the app**
```bash
streamlit run streamlit_app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 📂 Project Structure

```
AI-Resume-Parser/
│
├── streamlit_app.py      # Main Streamlit UI
├── resume_parser.py      # Core NLP parsing logic
├── requirements.txt      # Dependencies
├── parsed_resumes.csv    # Sample output
└── resumes/              # Sample resume files
```

---

## 🎯 How It Works

```
PDF/DOCX Resume
      ↓
Text Extraction (pdfplumber / docx2txt)
      ↓
NLP Pipeline (spaCy NER)
      ↓
Entity Extraction → Name, Email, Phone, Skills
      ↓
Analytics Dashboard + CSV Export
```

---

## 📊 Skills Detected

`Python` `Java` `C++` `C#` `JavaScript` `TypeScript` `Machine Learning` `Deep Learning` `Data Science` `AI` `TensorFlow` `Keras` `PyTorch` `SQL` `Pandas` `NumPy` `React` `Node.js` `Django` `Flask` `Docker` `AWS` `Git`

---

## 🙋‍♀️ Author

**Ashita Sharma**  
[GitHub](https://github.com/AshitaSharma01) • [LinkedIn](https://linkedin.com/in/ashita-sharma)

---

<p align="center">Built with ❤️ using Python & spaCy</p>
