import streamlit as st
import pandas as pd
import tempfile
import re
import pdfplumber
import docx2txt
import spacy
from collections import Counter
import time
import plotly.express as px

# Load SpaCy model safely
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        import en_core_web_sm
        return en_core_web_sm.load()

nlp = load_spacy_model()

skills_list = [
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript",
    "Machine Learning", "Deep Learning", "Data Science", "AI",
    "TensorFlow", "Keras", "PyTorch", "SQL", "Pandas", "NumPy",
    "React", "Node.js", "Django", "Flask", "Docker", "AWS", "Git"
]

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text
    elif file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    return ""

def parse_resume(text):
    clean_text = re.sub(r'Email:|Phone:|Contact:', '', text, flags=re.IGNORECASE)
    doc = nlp(clean_text)

    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = re.sub(r'\S+@\S+', '', ent.text.strip().replace("\n", " ")).strip()
            break

    email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phone = re.findall(r'\+?\d[\d\s-]{8,}\d', text)
    skills = [skill for skill in skills_list if skill.lower() in text.lower()]

    return {
        "Name": name if name else "Not found",
        "Email": email[0] if email else "Not found",
        "Phone": phone[0].strip() if phone else "Not found",
        "Skills": ", ".join(skills) if skills else "None detected",
        "Skill Count": len(skills)
    }

# --- Page Config ---
st.set_page_config(
    page_title="ResumeIQ — AI Resume Parser",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background: #080d1a;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0d1528 !important;
        border-right: 1px solid rgba(0, 200, 150, 0.15);
    }

    /* Hero Header */
    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
        position: relative;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(0, 200, 150, 0.1);
        border: 1px solid rgba(0, 200, 150, 0.3);
        color: #00c896;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 6px 16px;
        border-radius: 20px;
        margin-bottom: 16px;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.1;
        margin-bottom: 12px;
    }
    .hero-title span {
        background: linear-gradient(135deg, #00c896, #0096ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-sub {
        color: #8892a4;
        font-size: 1.05rem;
        max-width: 520px;
        margin: 0 auto;
    }

    /* Stat cards */
    .stat-card {
        background: linear-gradient(135deg, #0d1528, #111c35);
        border: 1px solid rgba(0, 200, 150, 0.2);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        text-align: center;
        margin-bottom: 12px;
    }
    .stat-number {
        font-size: 2.4rem;
        font-weight: 700;
        color: #00c896;
        font-family: 'JetBrains Mono', monospace;
    }
    .stat-label {
        color: #8892a4;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    /* Result card */
    .result-card {
        background: #0d1528;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 12px;
        transition: border-color 0.2s;
    }
    .result-card:hover {
        border-color: rgba(0, 200, 150, 0.3);
    }
    .result-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 6px;
    }
    .result-detail {
        font-size: 0.85rem;
        color: #8892a4;
        margin-bottom: 4px;
        font-family: 'JetBrains Mono', monospace;
    }
    .skill-tag {
        display: inline-block;
        background: rgba(0, 150, 255, 0.1);
        border: 1px solid rgba(0, 150, 255, 0.25);
        color: #4db8ff;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin: 3px 3px 3px 0;
    }

    /* Section headers */
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffffff;
        margin: 1.8rem 0 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: rgba(255,255,255,0.07);
        margin-left: 8px;
    }

    /* Success banner */
    .success-banner {
        background: linear-gradient(135deg, rgba(0,200,150,0.1), rgba(0,150,255,0.1));
        border: 1px solid rgba(0,200,150,0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: #00c896;
        font-weight: 600;
        font-size: 1rem;
        margin: 1rem 0;
        text-align: center;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: #0d1528;
        border: 2px dashed rgba(0,200,150,0.25) !important;
        border-radius: 16px;
        padding: 1rem;
    }

    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #00c896, #0096ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 0.95rem !important;
        width: 100%;
    }

    /* Sidebar styling */
    .sidebar-section {
        background: rgba(0,200,150,0.05);
        border: 1px solid rgba(0,200,150,0.15);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .sidebar-title {
        color: #00c896;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    .sidebar-item {
        color: #8892a4;
        font-size: 0.88rem;
        padding: 4px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
        <div style='font-size:2.5rem;'>🧠</div>
        <div style='color:#ffffff; font-weight:700; font-size:1.2rem; margin-top:8px;'>ResumeIQ</div>
        <div style='color:#8892a4; font-size:0.8rem;'>AI-Powered Parser</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='sidebar-section'>
        <div class='sidebar-title'>📋 How to use</div>
        <div class='sidebar-item'>① Upload PDF or DOCX files</div>
        <div class='sidebar-item'>② AI extracts key info</div>
        <div class='sidebar-item'>③ View skill analytics</div>
        <div class='sidebar-item'>④ Download CSV report</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='sidebar-section'>
        <div class='sidebar-title'>⚙️ Tech Stack</div>
        <div class='sidebar-item'>🐍 Python 3</div>
        <div class='sidebar-item'>🔬 spaCy NLP</div>
        <div class='sidebar-item'>📊 Streamlit</div>
        <div class='sidebar-item'>📈 Plotly</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='sidebar-section'>
        <div class='sidebar-title'>🎯 Detects Skills</div>
        <div style='color:#4db8ff; font-size:0.82rem; line-height:1.8;'>
        Python • Java • C++ • ML • AI<br>
        TensorFlow • SQL • React • AWS<br>
        Docker • Django • Flask • Git
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class='hero'>
    <div class='hero-badge'>✦ Powered by spaCy NLP</div>
    <div class='hero-title'>Parse Resumes with <span>AI Precision</span></div>
    <div class='hero-sub'>Upload multiple resumes and instantly extract names, contacts, and skills with intelligent analysis.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- File Upload ---
uploaded_files = st.file_uploader(
    "Drop your resumes here",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    help="Supports PDF and DOCX formats"
)

# --- Processing ---
if uploaded_files:
    progress_bar = st.progress(0, text="Initializing AI parser...")
    results = []

    for i, file in enumerate(uploaded_files):
        pct = int((i + 1) / len(uploaded_files) * 100)
        progress_bar.progress(pct, text=f"Parsing {file.name}... ({i+1}/{len(uploaded_files)})")
        time.sleep(0.3)

        with tempfile.NamedTemporaryFile(delete=False, suffix=file.name) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        text = extract_text(tmp_path)
        parsed = parse_resume(text)
        parsed["File"] = file.name
        results.append(parsed)

    progress_bar.empty()

    st.markdown("<div class='success-banner'>✅ Parsing Complete — All resumes processed successfully!</div>", unsafe_allow_html=True)

    df = pd.DataFrame(results)

    # --- Metrics ---
    all_skills = []
    for s in df["Skills"]:
        if s and s != "None detected":
            all_skills.extend(s.split(", "))

    top_skill = Counter(all_skills).most_common(1)[0][0] if all_skills else "N/A"
    unique_skills = len(set(all_skills))
    avg_skills = round(df["Skill Count"].mean(), 1)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(df)}</div><div class='stat-label'>Resumes Parsed</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{unique_skills}</div><div class='stat-label'>Unique Skills Found</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{avg_skills}</div><div class='stat-label'>Avg Skills/Resume</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{top_skill}</div><div class='stat-label'>Most Common Skill</div></div>", unsafe_allow_html=True)

    # --- Candidate Cards ---
    st.markdown("<div class='section-title'>👤 Parsed Candidates</div>", unsafe_allow_html=True)

    cols = st.columns(2)
    for i, row in df.iterrows():
        with cols[i % 2]:
            skills_html = "".join([f"<span class='skill-tag'>{s.strip()}</span>" for s in row['Skills'].split(',') if s.strip() and s.strip() != 'None detected'])
            st.markdown(f"""
            <div class='result-card'>
                <div class='result-name'>👤 {row['Name']}</div>
                <div class='result-detail'>✉️ {row['Email']}</div>
                <div class='result-detail'>📞 {row['Phone']}</div>
                <div style='margin-top:8px;'>{skills_html if skills_html else "<span style='color:#8892a4;font-size:12px;'>No skills detected</span>"}</div>
            </div>
            """, unsafe_allow_html=True)

    # --- Charts ---
    if all_skills:
        st.markdown("<div class='section-title'>📊 Skill Analytics</div>", unsafe_allow_html=True)

        skill_counts = pd.Series(all_skills).value_counts().reset_index()
        skill_counts.columns = ["Skill", "Count"]

        col_chart1, col_chart2 = st.columns([3, 2])

        with col_chart1:
            fig_bar = px.bar(
                skill_counts,
                x="Skill", y="Count",
                color="Count",
                color_continuous_scale=["#0096ff", "#00c896"],
                title="Skill Frequency Across All Resumes"
            )
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(13,21,40,1)',
                font_color='#8892a4',
                title_font_color='#ffffff',
                coloraxis_showscale=False,
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_chart2:
            fig_pie = px.pie(
                skill_counts.head(6),
                names="Skill", values="Count",
                title="Top Skills Distribution",
                color_discrete_sequence=px.colors.sequential.Teal
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(13,21,40,1)',
                font_color='#8892a4',
                title_font_color='#ffffff'
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- Full Data Table ---
    with st.expander("🗂️ View Full Data Table"):
        display_df = df.drop(columns=["Skill Count"])
        st.dataframe(display_df, use_container_width=True, height=300)

    # --- Download ---
    st.markdown("<div class='section-title'>⬇️ Export</div>", unsafe_allow_html=True)
    csv_data = df.drop(columns=["Skill Count"]).to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download Full Report as CSV",
        csv_data,
        "resumeiq_parsed_data.csv",
        "text/csv"
    )

else:
    # Empty state
    st.markdown("""
    <div style='text-align:center; padding:3rem; background:#0d1528; border:2px dashed rgba(0,200,150,0.2); border-radius:20px; margin-top:1rem;'>
        <div style='font-size:3rem; margin-bottom:1rem;'>📂</div>
        <div style='color:#ffffff; font-size:1.1rem; font-weight:600; margin-bottom:8px;'>No resumes uploaded yet</div>
        <div style='color:#8892a4; font-size:0.9rem;'>Upload PDF or DOCX files above to begin parsing</div>
    </div>
    """, unsafe_allow_html=True)