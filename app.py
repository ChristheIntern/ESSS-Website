import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from PIL import Image
import io

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI-Guided Catalyst Selection | CO₂-to-CO",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+3:wght@300;400;500;600&family=Source+Code+Pro:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

/* Header banner */
.hero {
    background: #0f1923;
    color: #f7f4ef;
    padding: 2.5rem 2.5rem 2rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-tag {
    display: inline-block;
    background: #1a6b4a;
    color: white;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.2rem 0.7rem;
    border-radius: 2px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.2rem;
    font-weight: 700;
    color: #f7f4ef !important;
    line-height: 1.25;
    margin-bottom: 0.6rem;
}
.hero .subtitle {
    font-size: 1rem;
    color: rgba(247,244,239,0.65);
    margin-bottom: 0.8rem;
}
.hero .authors {
    font-size: 0.85rem;
    color: rgba(247,244,239,0.45);
}
.hero .authors span { color: rgba(247,244,239,0.85); font-weight: 500; }

/* Section labels */
.section-label {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #1a6b4a;
    display: block;
    margin-bottom: 0.3rem;
    font-weight: 500;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: #0f1923;
    margin-bottom: 0.8rem;
}

/* Abstract box */
.abstract-box {
    background: white;
    border-left: 3px solid #1a6b4a;
    padding: 1.2rem 1.5rem;
    border-radius: 0 4px 4px 0;
    box-shadow: 0 1px 10px rgba(0,0,0,0.05);
    font-size: 0.96rem;
    line-height: 1.75;
    color: #2a2a2a;
}

/* Callout */
.callout {
    background: #e8f4ee;
    border: 1px solid #b5ddc7;
    border-radius: 4px;
    padding: 0.9rem 1.2rem;
    font-size: 0.9rem;
    color: #1a3a2a;
    margin: 0.8rem 0;
}

/* Metric card */
.metric-card {
    background: white;
    border: 1px solid #d4cfc8;
    border-radius: 6px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.metric-card.winner {
    border-color: #1a6b4a;
    background: #e8f4ee;
}
.metric-model {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b6560;
    margin-bottom: 0.4rem;
}
.metric-r2 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #1a6b4a;
    line-height: 1;
}
.metric-label { font-size: 0.72rem; color: #6b6560; margin-bottom: 0.4rem; }
.metric-mse { font-size: 0.8rem; color: #6b6560; }
.metric-mse b { color: #0f1923; font-family: 'Source Code Pro', monospace; }

/* Winner badge */
.winner-badge {
    display: inline-block;
    background: #1a6b4a;
    color: white;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 0.15rem 0.5rem;
    border-radius: 2px;
    margin-left: 0.4rem;
    font-family: 'Source Code Pro', monospace;
    letter-spacing: 0.06em;
}

/* Feature bar */
.feat-row { display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem; }
.feat-name { font-family:'Source Code Pro',monospace; font-size:0.78rem; width:130px; flex-shrink:0; }
.feat-bg { flex:1; height:9px; background:#e5e1da; border-radius:99px; overflow:hidden; }
.feat-fill { height:100%; background:linear-gradient(90deg,#1a6b4a,#2da868); border-radius:99px; }
.feat-val { font-size:0.75rem; font-family:'Source Code Pro',monospace; color:#6b6560; width:40px; text-align:right; }

/* Candidate box */
.candidate-box {
    background: #0f1923;
    color: #f7f4ef;
    padding: 1.4rem 2rem;
    border-radius: 6px;
    display: flex;
    align-items: center;
    gap: 2rem;
    margin: 1rem 0;
}
.cand-num {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #2da868;
    line-height: 1;
}
.cand-label { font-size:0.7rem; letter-spacing:0.12em; text-transform:uppercase; color:rgba(247,244,239,0.45); }
.cand-desc { font-size:0.87rem; color:rgba(247,244,239,0.7); line-height:1.5; }

/* Equation */
.equation {
    background: #0f1923;
    color: #a8f0c6;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.93rem;
    padding: 0.9rem 1.3rem;
    border-radius: 4px;
    letter-spacing: 0.04em;
    margin: 0.7rem 0;
}

/* Divider */
.divider { border: none; border-top: 1px solid #d4cfc8; margin: 2rem 0; }

/* QR box */
.qr-box {
    background: white;
    border: 1px solid #d4cfc8;
    border-radius: 6px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Helper: generate QR code image ───────────────────────────────────────────
def make_qr(url: str, size: int = 200) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0f1923", back_color="white")
    img = img.resize((size, size), Image.LANCZOS)
    return img


def img_to_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">Research Poster · European School Karlsruhe</div>
  <h1>AI-Guided Catalyst Selection<br>for CO₂-to-CO Conversion</h1>
  <div class="subtitle">Using Random Forest Regression to Accelerate Sustainable Catalyst Screening</div>
  <div class="authors"><span>Shivansh Mahajan &amp; Cristian Roca</span> &nbsp;·&nbsp; European School Karlsruhe</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ABSTRACT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<span class="section-label">§ 00 — Overview</span>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Abstract</div>', unsafe_allow_html=True)
st.markdown("""
<div class="abstract-box">
The electrochemical reduction of carbon dioxide (CO₂) into carbon monoxide (CO) is an important first step
toward sustainable carbon utilization and synthetic fuel or glucose production. Traditional catalyst discovery
is extremely slow and expensive due to the large number of possible atomic configurations and complex chemical interactions.
<br><br>
In this project, we developed and compared three machine learning models — <strong>Linear Regression,
Ridge Regression, and Random Forest Regression</strong> — to predict catalyst performance for CO₂-to-CO conversion.
Feature-engineered atomic data from open catalyst datasets were used as inputs, and predictive capabilities were
evaluated using performance metrics. Random Forest showed the strongest performance, but comparing algorithms
provided insight into how linear vs. non-linear methods handle atomic feature interactions.
<br><br>
Although experimental validation was not conducted, this project demonstrates the potential of AI-assisted catalyst
screening to accelerate sustainable chemistry research. By predicting promising catalysts computationally,
researchers can focus laboratory efforts on only the most likely candidates, saving time, resources, and costs.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INTRODUCTION
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<span class="section-label">§ 01 — Background</span>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Introduction</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("##### 1. The Problem")
    st.markdown("CO₂ conversion is vital for climate mitigation. Traditional catalyst discovery is slow and costly because:")
    st.markdown("""
- Thousands of atomic configurations exist
- Experimental testing is time-consuming
- High-level simulations such as DFT take hours per frame
""")

with col2:
    st.markdown("##### 2. The Solution & Scope")
    st.markdown("Machine learning can learn patterns linking atomic composition and geometry to predicted catalytic efficiency.")
    st.markdown("""
- Focus on CO₂ → CO conversion (first step toward synthetic glucose)
- Train and compare Linear, Ridge, and Random Forest Regression
- Select the most accurate model to rank candidate catalysts
""")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# METHODOLOGY
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<span class="section-label">§ 02 — Methods</span>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Methodology</div>', unsafe_allow_html=True)

st.markdown("##### 1. Atomic Data Source")
st.markdown("Catalyst structures were represented as atomic simulation frames containing atomic positions, element types (As, Al, Co, H, Si, Pt), and geometric arrangements.")

st.markdown("##### 2. Feature Engineering")

fe_col1, fe_col2 = st.columns(2, gap="large")
with fe_col1:
    st.markdown("**2.1 Atomic Fingerprinting**")
    st.markdown("Automated counting of each element (C, H, O, Cu, Zr, As, Al, Co, Si, Pt) to capture elemental composition and relative ratios.")
    st.markdown("**2.2 Adsorbate Isolation**")
    st.markdown("Identification of atoms directly involved in CO₂ reduction to ensure the model focuses on chemically relevant parts of each frame.")
with fe_col2:
    st.markdown("**2.3 Structural & Geometric Descriptors**")
    st.markdown("""
- Classification of atoms as dispersed or clustered
- Measurement of surface roughness and spatial properties
- Geometric indicators influencing catalytic activity
""")
    st.markdown("**2.4 Robust Data Cleaning**")
    st.markdown("Imputation of missing values, outlier removal, and normalization to stabilize the dataset for machine learning.")

st.markdown("""
<div class="callout">
  These steps produced a clean, structured dataset serving as input for all three regression models.
  By combining chemical insight with numerical representation, the model could learn meaningful patterns
  between atomic features and predicted CO₂-to-CO catalytic performance.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MACHINE LEARNING MODELS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<span class="section-label">§ 03 — Algorithms</span>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Machine Learning Models</div>', unsafe_allow_html=True)
st.markdown("We applied three regression models with an **80% train / 20% test** split for all.")

model_data = {
    "Model": ["Linear Regression", "Ridge Regression", "Random Forest Regression ★"],
    "Why Used?": [
        "Simple baseline",
        "Adds regularization to prevent overfitting",
        "Ensemble method; captures non-linear interactions",
    ],
    "Observation": [
        "Captures linear relationships but struggles with non-linear interactions",
        "Slight improvement over Linear Regression, still limited with complex features",
        "Highest accuracy and lowest prediction error",
    ],
}
st.dataframe(model_data, use_container_width=True, hide_index=True)

# Model explanations
with st.expander("📐 What is Linear Regression?"):
    st.markdown("""
Linear regression is a basic supervised learning algorithm that assumes a straight-line relationship
between features and labels. In machine learning with multiple features, the equation becomes:
""")
    st.markdown('<div class="equation">y = w₁x₁ + w₂x₂ + w₃x₃ + ... + b</div>', unsafe_allow_html=True)
    st.markdown("""
- **w (weights):** The "knobs" the model adjusts during training — each weight controls how strongly a feature influences the prediction.
- **b (bias/intercept):** The starting value of y when all feature values are zero.
- The algorithm minimizes **Mean Squared Error (MSE)** to find the line that best fits the data.
""")

with st.expander("🔧 What is Ridge Regression?"):
    st.markdown("""
Ridge Regression is an improved version of Linear Regression. It uses the same equation but adds
**regularization** — a penalty term to prevent overfitting by discouraging large weight values.
Controlled by the parameter **alpha (α)**:
- Small alpha → behaves like normal linear regression
- Large alpha → stronger penalty, more weight shrinkage

Useful when you have many correlated features and want a more stable, generalizable model.
""")

with st.expander("🌲 What is Random Forest Regression?"):
    st.markdown("""
Random Forest Regression builds **many decision trees** and combines their results. Each tree works by
asking a series of "if–then" questions to split data into groups, e.g.:
- If num_adsorbates > 2 → go left
- If count_Ni > 5 → go right

A **Random Forest** builds many trees using random subsets of data and features, then averages all predictions.
This enables modelling **non-linear relationships** and reduces overfitting compared to a single tree.
""")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<span class="section-label">§ 04 — Results &amp; Discussion</span>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Results</div>', unsafe_allow_html=True)

# Metric cards
st.markdown("##### Performance Metrics")
mc1, mc2, mc3 = st.columns(3, gap="medium")
with mc1:
    st.markdown("""
<div class="metric-card">
  <div class="metric-model">Linear Regression</div>
  <div class="metric-r2">0.933</div>
  <div class="metric-label">R² Score</div>
  <div class="metric-mse">MSE: <b>8.061</b></div>
</div>""", unsafe_allow_html=True)
with mc2:
    st.markdown("""
<div class="metric-card">
  <div class="metric-model">Ridge Regression</div>
  <div class="metric-r2">0.999</div>
  <div class="metric-label">R² Score</div>
  <div class="metric-mse">MSE: <b>8.061</b></div>
</div>""", unsafe_allow_html=True)
with mc3:
    st.markdown("""
<div class="metric-card winner">
  <div class="metric-model" style="color:#1a6b4a;">Random Forest ★</div>
  <div class="metric-r2">0.990</div>
  <div class="metric-label">R² Score</div>
  <div class="metric-mse">MSE: <b>261,070</b></div>
</div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Metrics explained
exp1, exp2 = st.columns(2, gap="large")
with exp1:
    st.markdown("**R² Score (Coefficient of Determination)**")
    st.markdown("Tells us how well the model's predictions match actual data. Ranges 0–1, where 1 = perfect. R² = 0.99 means 99% of variation in catalyst performance is explained by the model.")
with exp2:
    st.markdown("**MSE (Mean Squared Error)**")
    st.markdown("Measures how far predictions are from actual values. Calculated by squaring the differences between predicted and actual values. Smaller MSE → predictions closer to reality.")

st.markdown("---")

# Feature importance
st.markdown("##### Feature Importance (Random Forest)")

features = [
    ("num_adsorbates", 84),
    ("count_Re", 6),
    ("count_Pt", 4),
    ("count_In", 3),
    ("count_Co", 3),
]

for name, pct in features:
    bar_html = f"""
<div class="feat-row">
  <div class="feat-name">{name}</div>
  <div class="feat-bg"><div class="feat-fill" style="width:{pct}%"></div></div>
  <div class="feat-val">~{pct}%</div>
</div>"""
    st.markdown(bar_html, unsafe_allow_html=True)

st.markdown("""
<div class="callout" style="margin-top:0.8rem;">
  <strong>num_adsorbates</strong> dominates feature importance (~84%), showing the number of active sites
  is the primary driver of predicted catalytic activity.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Observations
obs_col, feat_col = st.columns(2, gap="large")

with obs_col:
    st.markdown("##### Key Observations")
    st.markdown("""
1. **Linear & Ridge Regression**: Very high R² (>0.999) because some relationships are almost linear. Feature weights indicate which elements are most influential.
2. **Random Forest Regression**: Slightly lower R² (0.99) but captures **non-linear interactions** between atoms and adsorbates.
3. **Model Selection**: Random Forest chosen for final predictions — it models complex chemical interactions that linear models cannot.
""")

with feat_col:
    st.markdown("##### Feature Significance")
    feat_data = {
        "Feature": ["Pt concentration", "Co clustering", "Surface roughness", "Si content"],
        "Significance": ["High impact", "Medium impact", "Medium impact", "Low impact"],
    }
    st.dataframe(feat_data, use_container_width=True, hide_index=True)

st.markdown("---")

# Computational advantage
st.markdown("##### Computational Advantage")
comp1, comp2 = st.columns(2, gap="medium")
with comp1:
    st.markdown("""
<div class="metric-card">
  <div class="metric-model">DFT Simulation</div>
  <div class="metric-r2" style="color:#c14b0a; font-size:1.6rem;">Hours</div>
  <div class="metric-label">per configuration</div>
  <div class="metric-mse">Slow &amp; expensive</div>
</div>""", unsafe_allow_html=True)
with comp2:
    st.markdown("""
<div class="metric-card winner">
  <div class="metric-model" style="color:#1a6b4a;">ML Prediction ★</div>
  <div class="metric-r2" style="font-size:1.6rem;">Milliseconds</div>
  <div class="metric-label">per configuration</div>
  <div class="metric-mse">Fast, scalable for thousands of candidates</div>
</div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Top candidate
st.markdown("##### Top Candidate")
st.markdown("""
<div class="candidate-box">
  <div>
    <div class="cand-label">Top Candidate Frame</div>
    <div class="cand-num">1526</div>
  </div>
  <div class="cand-desc">
    Selected by Random Forest Regression as the most promising catalyst candidate for
    CO₂-to-CO conversion based on atomic composition and structural features.
  </div>
</div>
""", unsafe_allow_html=True)

# Limitations
st.markdown("##### Limitations")
st.markdown("""
- No experimental validation performed
- Only CO₂ → CO conversion modeled
- Model accuracy depends on quality and diversity of input data
- Safety considerations: As is toxic; H is difficult to detect experimentally
""")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CONCLUSION
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<span class="section-label">§ 05 — Summary</span>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Conclusion</div>', unsafe_allow_html=True)
st.markdown("""
- Comparing multiple algorithms shows that **non-linear methods outperform linear models** for predicting catalyst efficiency
- Random Forest Regression effectively ranks CO₂-to-CO catalysts, identifying promising candidates like **Frame 1526**
- ML-assisted screening accelerates the first stage of catalyst design, reducing computational and experimental costs
- The methodology could be extended for later stages in CO₂ conversion toward multi-carbon compounds
""")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# QR CODE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<span class="section-label">§ 06 — Access</span>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Scan to View This Page</div>', unsafe_allow_html=True)

qr_col, info_col = st.columns([1, 2], gap="large")

with qr_col:
    # Default URL — users can override it
    default_url = "http://localhost:8501"
    qr_url = st.text_input(
        "URL to encode in QR code",
        value=default_url,
        help="Enter the URL where this Streamlit app is hosted (e.g. your deployed URL).",
    )
    if qr_url:
        qr_img = make_qr(qr_url, size=220)
        st.image(qr_img, caption="Scan with your phone camera", width=220)

        # Download button
        qr_bytes = img_to_bytes(qr_img)
        st.download_button(
            label="⬇ Download QR Code",
            data=qr_bytes,
            file_name="poster_qr_code.png",
            mime="image/png",
        )

with info_col:
    st.markdown("""
<div class="qr-box">
  <strong style="font-family:'Playfair Display',serif; font-size:1.1rem;">Quick Access via QR Code</strong>
  <p style="margin-top:0.6rem; font-size:0.9rem; color:#6b6560; line-height:1.6;">
    Point your phone camera at the QR code to open this research poster website instantly.
    Share with conference attendees, peers, or supervisors.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-family:'Source Code Pro',monospace; font-size:0.75rem; color:#aaa; padding:1rem 0;">
  Shivansh Mahajan &amp; Cristian Roca · European School Karlsruhe · AI-Guided Catalyst Selection for CO₂-to-CO Conversion
</div>
""", unsafe_allow_html=True)