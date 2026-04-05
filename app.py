import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import warnings
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="SmartDiet — Your Personal Meal Guide",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS: warm, friendly, non-clinical feel ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

h1, h2, h3 {
    font-family: 'Lora', serif;
}

/* ── Main background ── */
.stApp {
    background: #F4F7F4 !important;
}

/* Base text color for light areas */
.stApp p, .stApp span, .stApp label,
.stApp li, .stApp small {
    color: #1A2F2A;
}

/* ── Force white text inside all dark gradient cards ── */
.hero-banner, .hero-banner *,
.profile-card, .profile-card *,
.assessment-card, .assessment-card *,
.summary-card, .summary-card * {
    color: white !important;
}

/* Re-override stApp rule specifically for dark card p and span tags */
.hero-banner p, .hero-banner span,
.profile-card p, .profile-card span,
.assessment-card p, .assessment-card span,
.summary-card p, .summary-card span {
    color: white !important;
}

.profile-card h2, .summary-card h2  { color: #C8E6C9 !important; }
.profile-pill                        { color: white !important; }

/* ── Streamlit tab labels — force dark text on light bg ── */
.stTabs [data-baseweb="tab-list"] {
    background: #E8F5E9 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #2E7D32 !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
}

.stTabs [aria-selected="true"] {
    background: white !important;
    color: #1A2F2A !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}

/* ── Expander: force white background + dark text, override all themes ── */
.streamlit-expanderHeader,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] > div:first-child {
    background: white !important;
    background-color: white !important;
    color: #1A2F2A !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border-radius: 12px !important;
    border: 1.5px solid #C8E6C9 !important;
}

.streamlit-expanderHeader:hover,
[data-testid="stExpander"] summary:hover {
    background: #F0FFF0 !important;
    background-color: #F0FFF0 !important;
    border-color: #4CAF50 !important;
}

.streamlit-expanderHeader p,
.streamlit-expanderHeader span,
.streamlit-expanderHeader svg,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary svg {
    color: #1A2F2A !important;
    fill: #1A2F2A !important;
}

.streamlit-expanderContent,
[data-testid="stExpander"] > div:last-child {
    background: #FAFFFE !important;
    background-color: #FAFFFE !important;
    border: 1.5px solid #C8E6C9 !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    color: #1A2F2A !important;
}

.streamlit-expanderContent *,
[data-testid="stExpander"] > div:last-child * {
    color: #1A2F2A !important;
}

/* ── st.dataframe / table text ── */
.stDataFrame, .stTable {
    color: #1A2F2A !important;
}

/* ── st.metric ── */
[data-testid="stMetricValue"] {
    color: #1A2F2A !important;
    font-weight: 800 !important;
}

[data-testid="stMetricLabel"] {
    color: #555 !important;
}

/* ── st.caption ── */
.stApp .stCaption, .stApp small {
    color: #777 !important;
}

/* ── st.info / success / warning ── */
.stAlert {
    border-radius: 12px !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1A2F2A !important;
}

section[data-testid="stSidebar"] * {
    color: #E8F5E9 !important;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] select {
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    border-color: rgba(255,255,255,0.2) !important;
}

section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stNumberInput label,
section[data-testid="stSidebar"] .stTextInput label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label {
    color: #A5D6A7 !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

section[data-testid="stSidebar"] .stButton button {
    background: #4CAF50 !important;
    color: white !important;
    border-radius: 50px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    padding: 0.6rem 1.2rem !important;
    border: none !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
    transition: background 0.2s !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: #388E3C !important;
}

.hero-banner {
    background: linear-gradient(135deg, #1A2F2A 0%, #2E7D32 60%, #388E3C 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    color: white;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.hero-banner::after {
    content: '🍎';
    font-size: 120px;
    position: absolute;
    right: 2.5rem;
    top: 50%;
    transform: translateY(-50%);
    opacity: 0.18;
}

.hero-title {
    font-family: 'Lora', serif;
    font-size: 2.8rem;
    font-weight: 600;
    margin: 0 0 0.3rem 0;
    line-height: 1.2;
}

.hero-sub {
    font-size: 1.1rem;
    opacity: 0.85;
    margin: 0;
    font-weight: 400;
}

.welcome-step {
    background: white;
    border-radius: 16px;
    padding: 1.6rem 2rem;
    border-left: 5px solid #4CAF50;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}

.welcome-step h3 {
    margin: 0 0 0.4rem 0;
    color: #1A2F2A !important;
    font-size: 1.1rem;
}

.welcome-step p {
    margin: 0;
    color: #444 !important;
    font-size: 0.95rem;
    line-height: 1.6;
}

.profile-card {
    background: linear-gradient(135deg, #1A2F2A, #2E7D32);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    color: white;
    margin-bottom: 1.5rem;
}

.profile-card h2 {
    font-family: 'Lora', serif;
    font-size: 1.6rem;
    margin: 0 0 1rem 0;
    color: #C8E6C9;
}

.profile-pill {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border-radius: 50px;
    padding: 0.35rem 1rem;
    margin: 0.25rem 0.2rem;
    font-size: 0.9rem;
    font-weight: 600;
    backdrop-filter: blur(4px);
}

.fitness-badge {
    display: inline-block;
    border-radius: 12px;
    padding: 0.8rem 1.4rem;
    font-weight: 700;
    font-size: 1rem;
    margin-top: 0.5rem;
}

.assessment-card {
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    color: white;
    font-family: 'Lora', serif;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.assessment-icon {
    font-size: 3.5rem;
    display: block;
    margin-bottom: 0.6rem;
}

.assessment-title {
    font-size: 1.8rem;
    font-weight: 600;
    margin: 0 0 0.3rem 0;
}

.assessment-msg {
    font-size: 0.95rem;
    opacity: 0.9;
    margin: 0;
    font-family: 'Nunito', sans-serif;
    line-height: 1.5;
}

.confidence-bar-wrap {
    background: rgba(255,255,255,0.25);
    border-radius: 50px;
    height: 10px;
    margin: 1rem auto 0.3rem;
    width: 80%;
    overflow: hidden;
}

.confidence-bar-fill {
    height: 100%;
    border-radius: 50px;
    background: white;
}

.confidence-label {
    font-size: 0.85rem;
    opacity: 0.85;
    font-family: 'Nunito', sans-serif;
}

.meal-plan-header {
    background: white;
    border-radius: 20px;
    padding: 1.4rem 2rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border: 2px solid #E8F5E9;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.meal-target-badge {
    background: #E8F5E9;
    color: #2E7D32;
    border-radius: 50px;
    padding: 0.3rem 1rem;
    font-weight: 700;
    font-size: 0.9rem;
    white-space: nowrap;
}

.meal-card {
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    border: 1.5px solid #E8F5E9;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    margin-bottom: 0.8rem;
    transition: box-shadow 0.2s;
}

.meal-card:hover {
    box-shadow: 0 6px 20px rgba(0,0,0,0.09);
}

.meal-card-title {
    font-family: 'Lora', serif;
    font-size: 1.15rem;
    color: #1A2F2A;
    font-weight: 600;
    margin: 0 0 0.2rem 0;
}

.meal-card-sub {
    font-size: 0.88rem;
    color: #777;
    margin: 0 0 0.8rem 0;
}

.nutrient-pill {
    display: inline-block;
    background: #E8F5E9;
    border: 1.5px solid #A5D6A7;
    border-radius: 8px;
    padding: 0.3rem 0.7rem;
    margin: 0.2rem;
    font-size: 0.83rem;
    color: #1B5E20 !important;
    font-weight: 700;
}

.best-pick-banner {
    background: linear-gradient(90deg, #2E7D32, #4CAF50);
    color: white !important;
    border-radius: 8px;
    padding: 0.3rem 1rem;
    font-size: 0.78rem;
    font-weight: 800;
    display: inline-block;
    margin-bottom: 0.6rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.summary-card {
    background: linear-gradient(135deg, #1A2F2A, #2E7D32);
    border-radius: 20px;
    padding: 2rem;
    color: white !important;
    margin-top: 1.5rem;
}

.summary-card h2 {
    font-family: 'Lora', serif;
    color: #C8E6C9 !important;
    margin: 0 0 1.2rem 0;
    font-size: 1.5rem;
}

.summary-num {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    color: white !important;
}

.summary-label {
    font-size: 0.8rem;
    color: #A5D6A7 !important;
    margin-top: 0.2rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.guideline-card {
    background: white;
    border-radius: 16px;
    padding: 1.6rem 2rem;
    border-left: 5px solid #4CAF50;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-top: 1.2rem;
}

.guideline-card h3 {
    color: #1A2F2A !important;
    font-size: 1.1rem;
    margin: 0 0 0.8rem 0;
}

.guideline-tip {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    margin-bottom: 0.6rem;
    font-size: 0.95rem;
    color: #333 !important;
    line-height: 1.5;
}

/* ── Stat cards: nuclear option to prevent any override ── */
.stat-card p {
    color: inherit !important;
}

/* Fix p tags inside ALL Streamlit markdown areas */
.stMarkdown p {
    color: #1A2F2A !important;
}

/* Re-override for dark cards — higher specificity, must come AFTER stMarkdown */
div.hero-banner p,
div.hero-banner .stMarkdown p,
div.profile-card p,
div.profile-card .stMarkdown p,
div.summary-card p,
div.summary-card .stMarkdown p,
div.assessment-card p,
div.assessment-card .stMarkdown p {
    color: white !important;
}

.disclaimer {
    text-align: center;
    color: #999;
    font-size: 0.82rem;
    margin-top: 2rem;
    padding: 1rem;
    border-top: 1px solid #E8F0E8;
}

.progress-track {
    background: rgba(255,255,255,0.2);
    border-radius: 50px;
    height: 8px;
    width: 100%;
    margin: 0.4rem 0;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    border-radius: 50px;
    background: #69F0AE;
    transition: width 0.6s ease;
}
</style>
""", unsafe_allow_html=True)


# ── Backend: load models (unchanged) ─────────────────────────────────────────
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")

@st.cache_resource
def load_all():
    rf        = joblib.load(f"{MODEL_DIR}/rf_model.pkl")
    gb        = joblib.load(f"{MODEL_DIR}/gb_model.pkl")
    scaler    = joblib.load(f"{MODEL_DIR}/scaler.pkl")
    le_target = joblib.load(f"{MODEL_DIR}/le_target.pkl")
    le_diet   = joblib.load(f"{MODEL_DIR}/le_diet.pkl")
    le_meal   = joblib.load(f"{MODEL_DIR}/le_meal.pkl")
    le_dish   = joblib.load(f"{MODEL_DIR}/le_dish.pkl")
    df        = pd.read_csv(f"{MODEL_DIR}/meals_extended_labelled.csv")
    with open(f"{MODEL_DIR}/meta.json") as f:
        meta = json.load(f)
    return rf, gb, scaler, le_target, le_diet, le_meal, le_dish, df, meta

rf, gb, scaler, le_target, le_diet, le_meal, le_dish, meals_df, meta = load_all()

# ── BMR-based daily calorie calculator (Mifflin-St Jeor + condition adjustment) ──
def calculate_daily_calories(weight, height, age, gender, condition):
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    tdee = round(bmr * 1.2)

    min_cal = 1500 if gender == "Male" else 1200

    if condition == "diabetes":
        target = max(tdee - 500, min_cal)
    elif condition == "hypertension":
        target = tdee
    elif condition == "obesity":
        target = max(tdee - 600, min_cal)
    else:
        target = tdee

    return round(target)

SLOT_CALORIE_SPLIT = {
    "breakfast": 0.25,
    "lunch":     0.35,
    "snack":     0.10,
    "dinner":    0.30,
}

SLOT_MEAL_TIME = {
    "breakfast": ["breakfast", "breakfast/dinner"],
    "lunch":     ["lunch", "lunch/dinner"],
    "snack":     ["snack"],
    "dinner":    ["dinner", "lunch/dinner", "breakfast/dinner"],
}

SLOT_CARB_LIMITS = {"diabetes": 55, "hypertension": 65, "obesity": 50, "healthy": 75}
SLOT_FAT_LIMITS  = {"diabetes": 15, "hypertension": 15, "obesity": 10, "healthy": 20}

# ── Friendly UI mappings ──────────────────────────────────────────────────────
CONDITION_DISPLAY = {
    "healthy":      ("Healthy",              "🌿", "#2E7D32", "#E8F5E9"),
    "diabetes":     ("Managing Diabetes",    "🩸", "#C62828", "#FFEBEE"),
    "hypertension": ("Managing Blood Pressure", "💙", "#1565C0", "#E3F2FD"),
    "obesity":      ("Managing Weight",      "⚖️", "#6A1B9A", "#F3E5F5"),
}

FITNESS_DISPLAY = {
    "Slightly Slim": ("You're on the leaner side", "🌱", "#0277BD", "#E1F5FE"),
    "Fit":           ("You're in great shape!",    "💪", "#2E7D32", "#E8F5E9"),
    "Overweight":    ("A little above ideal weight","🌻", "#E65100", "#FFF3E0"),
    "Obese":         ("Weight management recommended","🌸","#6A1B9A","#F3E5F5"),
}

CONDITION_TIPS = {
    "diabetes": [
        ("🌾", "Choose ragi, oats, or brown rice instead of white rice — they digest slowly and keep your sugar steady."),
        ("⏰", "Eat smaller meals every 3–4 hours rather than two big meals — this keeps your blood sugar level throughout the day."),
        ("🚫", "Avoid sugary drinks, sweets, and packaged snacks. Even 'fruit juices' can spike your sugar quickly."),
        ("💧", "Drink plenty of water and unsweetened buttermilk throughout the day."),
    ],
    "hypertension": [
        ("🧂", "Go easy on salt. Avoid pickles, papadams, packaged chips, and processed foods — they're hidden salt bombs."),
        ("🍌", "Eat potassium-rich foods daily — bananas, tender coconut water, and leafy greens help balance blood pressure."),
        ("🚶", "Even a 20-minute walk daily can meaningfully reduce blood pressure over time."),
        ("☕", "Limit tea and coffee to 1–2 cups a day. Too much caffeine can raise pressure."),
    ],
    "obesity": [
        ("🍽️", "Use a smaller plate and eat slowly — it takes 20 minutes for your brain to realise you're full."),
        ("🥚", "Include protein in every meal (eggs, dal, fish, paneer) — protein keeps you feeling full longer."),
        ("🚫", "Cut down on deep-fried snacks, maida items, and sugary drinks — these are the biggest calorie sources."),
        ("🚶", "Aim for at least 30 minutes of walking daily. It's free and very effective."),
    ],
    "healthy": [
        ("🥗", "Fill half your plate with vegetables and dal — they're packed with nutrients and fibre."),
        ("🥛", "Have a glass of buttermilk or a small bowl of curd daily — great for digestion."),
        ("🌿", "Eat seasonal fruits and vegetables as much as possible — they're fresher, cheaper, and more nutritious."),
        ("💧", "Drink at least 8 glasses of water a day. Staying hydrated keeps your energy up."),
    ],
}

SLOT_FRIENDLY = {
    "breakfast": ("🌅", "Morning Breakfast"),
    "lunch":     ("☀️", "Afternoon Lunch"),
    "snack":     ("🍵", "Evening Snack"),
    "dinner":    ("🌙", "Night Dinner"),
}

# ── Backend helper functions (unchanged logic) ────────────────────────────────
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Slightly Slim"
    elif bmi < 25.0:
        return "Fit"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"

def get_diet_options(preference):
    if preference == "Vegetarian":
        return ["vegetarian"]
    elif preference == "Non-Vegetarian":
        return ["non_vegetarian"]
    else:
        return ["vegetarian", "non_vegetarian"]

def recommend_for_slot(condition, diet_pref, slot, target_cal, tolerance=50):
    diet_opts     = get_diet_options(diet_pref)
    allowed_times = SLOT_MEAL_TIME[slot]

    subset = meals_df[
        meals_df["meal_time"].isin(allowed_times) &
        meals_df["diet"].isin(diet_opts)
    ].copy()

    if subset.empty:
        return []

    within = subset[
        (subset["calories_slot"] >= target_cal - tolerance) &
        (subset["calories_slot"] <= target_cal + tolerance)
    ].copy()

    if within.empty:
        subset["cal_diff"] = abs(subset["calories_slot"] - target_cal)
        within = subset.nsmallest(5, "cal_diff").copy()

    def score(row):
        s = abs(row["calories_slot"] - target_cal) * 0.5
        if condition == "diabetes":
            s += max(0, row["carbs_slot"] - 60) * 1.5
            s += max(0, row["sodium_slot_mg"] - 500) * 0.02
        elif condition == "hypertension":
            s += max(0, row["sodium_slot_mg"] - 400) * 0.05
        elif condition == "obesity":
            s += max(0, row["fat_slot"] - 15) * 2.0
        return s

    within["score"] = within.apply(score, axis=1)
    top3 = within.nsmallest(3, "score")
    cols = ["title", "diet", "calories_slot", "protein_slot",
            "fat_slot", "carbs_slot", "sodium_slot_mg", "slot_portion_g"]
    return top3[cols].to_dict("records")

def run_ml_prediction(condition, diet_pref):
    sample_meals = meals_df[meals_df["condition"] == condition]
    if sample_meals.empty:
        sample_meals = meals_df
    rep = sample_meals[["calories_slot","protein_slot","fat_slot",
                         "carbs_slot","sodium_slot_mg","slot_portion_g"]].median()
    try:
        d_enc = le_diet.transform([get_diet_options(diet_pref)[0]])[0]
        m_enc = le_meal.transform(["breakfast"])[0]
        t_enc = le_dish.transform(["main"])[0]
    except Exception:
        d_enc, m_enc, t_enc = 0, 0, 0

    x_sample = np.array([[rep["calories_slot"], rep["protein_slot"], rep["fat_slot"],
                           rep["carbs_slot"], rep["sodium_slot_mg"], rep["slot_portion_g"],
                           d_enc, m_enc, t_enc]])
    proba     = rf.predict_proba(scaler.transform(x_sample))[0]
    pred      = le_target.classes_[np.argmax(proba)]
    confidence = float(proba.max())
    return pred, confidence


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Conversational input flow
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 0.5rem 0;'>
        <span style='font-size:1.8rem;'>🍎</span>
        <span style='font-family: Lora, serif; font-size:1.3rem; font-weight:600;
                     color:#C8E6C9; margin-left:0.4rem;'>SmartDiet</span>
    </div>
    <p style='color:#81C784; font-size:0.82rem; margin:0 0 1.2rem 0;'>
        Your personal meal guide
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#A5D6A7; font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.2rem;'>👋 Tell us about yourself</p>", unsafe_allow_html=True)

    name   = st.text_input("What's your name?", placeholder="e.g. Priya")
    age    = st.slider("How old are you?", 10, 90, 35)
    gender = st.radio("", ["Female", "Male"], horizontal=True, label_visibility="collapsed")

    st.markdown("<p style='color:#A5D6A7; font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin: 0.8rem 0 0.2rem 0;'>📏 Your measurements</p>", unsafe_allow_html=True)

    height = st.number_input("Height (cm)", 100.0, 220.0, 165.0, step=0.5)
    weight = st.number_input("Weight (kg)", 20.0, 200.0, 65.0, step=0.5)

    bmi     = weight / ((height / 100) ** 2)
    bmi_cat = get_bmi_category(bmi)
    fit_msg, fit_icon, fit_color, _ = FITNESS_DISPLAY[bmi_cat]

    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.08); border-radius:12px;
                padding:0.8rem 1rem; margin:0.5rem 0 1rem 0;'>
        <span style='font-size:1.3rem;'>{fit_icon}</span>
        <span style='color:#C8E6C9; font-weight:700; font-size:0.95rem;
                     margin-left:0.4rem;'>{bmi:.1f}</span>
        <p style='color:#A5D6A7; font-size:0.82rem; margin:0.2rem 0 0 0;'>{fit_msg}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#A5D6A7; font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.2rem;'>🏥 Your health situation</p>", unsafe_allow_html=True)

    condition_options = ["I'm Healthy", "Managing Diabetes", "Managing Blood Pressure", "Managing My Weight"]
    condition_sel = st.selectbox("Which best describes you?", condition_options)

    condition_map = {
        "I'm Healthy":              "healthy",
        "Managing Diabetes":        "diabetes",
        "Managing Blood Pressure":  "hypertension",
        "Managing My Weight":       "obesity",
    }
    condition = condition_map[condition_sel]

    diabetes_type = None
    if condition == "diabetes":
        st.markdown("<p style='color:#A5D6A7; font-size:0.78rem; margin-top:0.4rem;'>Which stage?</p>", unsafe_allow_html=True)
        diabetes_type = st.radio("", ["Pre-Diabetic", "Type 1", "Type 2"],
                                  horizontal=True, label_visibility="collapsed")

    st.markdown("<p style='color:#A5D6A7; font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin: 0.8rem 0 0.2rem 0;'>🥗 What do you eat?</p>", unsafe_allow_html=True)

    diet_options = ["Only Vegetarian", "Non-Vegetarian", "Both are fine"]
    diet_sel = st.radio("", diet_options, horizontal=False, label_visibility="collapsed")

    diet_map = {
        "Only Vegetarian": "Vegetarian",
        "Non-Vegetarian":  "Non-Vegetarian",
        "Both are fine":   "Balanced",
    }
    diet_pref = diet_map[diet_sel]

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    go = st.button("✨ Show My Meal Plan", use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# MAIN PAGE
# ════════════════════════════════════════════════════════════════════════════

# ── Hero banner ───────────────────────────────────────────────────────────────
greeting = f"Hello, {name}!" if name else "Welcome to SmartDiet"
st.markdown(f"""
<div class='hero-banner' style='background:linear-gradient(135deg,#1A2F2A 0%,#2E7D32 60%,#388E3C 100%);
     border-radius:20px; padding:2.5rem 3rem; color:white; margin-bottom:1.5rem;
     position:relative; overflow:hidden;'>
    <p style='font-family:Lora,serif; font-size:2.6rem; font-weight:600;
              color:white !important; margin:0 0 0.4rem 0; line-height:1.2;
              text-shadow: 0 1px 3px rgba(0,0,0,0.3);'>
        {greeting}
    </p>
    <p style='font-size:1.05rem; color:rgba(255,255,255,0.92) !important;
              margin:0; font-weight:400; line-height:1.6;
              text-shadow: 0 1px 2px rgba(0,0,0,0.2);'>
        Your personalised meal guide for a healthier, happier life —<br>
        built around the foods you already love.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Welcome / landing state ───────────────────────────────────────────────────
if not go:
    st.markdown("### How it works")
    steps = [
        ("1️⃣ Tell us about yourself",
         "Share your name, age, height, and weight using the panel on the left. It only takes a minute."),
        ("2️⃣ Choose your health situation",
         "Select what best describes you — whether you're healthy or managing a condition like diabetes or blood pressure."),
        ("3️⃣ Get your personal meal plan",
         "We'll suggest breakfast, lunch, snack, and dinner options from 214 authentic regional meals, matched to your daily calorie goal."),
        ("4️⃣ Read your tips",
         "We'll share simple, actionable food tips that are specific to your health situation — no medical jargon, just friendly advice."),
    ]
    for title, desc in steps:
        st.markdown(f"""
        <div class='welcome-step'>
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; color:#888; font-size:0.88rem;'>
        🍎 &nbsp; 214 regional meals &nbsp;|&nbsp;
        ✅ &nbsp; Calorie-balanced plans &nbsp;|&nbsp;
        🌿 &nbsp; All 4 health conditions covered
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ════════════════════════════════════════════════════════════════════════════
# RESULTS PAGE
# ════════════════════════════════════════════════════════════════════════════

# ── BMI correction ────────────────────────────────────────────────────────────
if condition == "healthy" and bmi_cat == "Obese":
    st.markdown("""
    <div style='background:#FFF3E0; border-left:5px solid #FF9800; border-radius:12px;
                padding:1rem 1.4rem; margin-bottom:1rem;'>
        <strong>⚠️ A small adjustment</strong><br>
        Based on your height and weight, we've switched your plan to focus on
        <strong>weight management</strong>. This will help you reach a healthier range gradually.
    </div>
    """, unsafe_allow_html=True)
    condition = "obesity"

# ── Your Profile card ─────────────────────────────────────────────────────────
cond_label, cond_icon, cond_color, cond_bg = CONDITION_DISPLAY[condition]
fit_msg, fit_icon, fit_color, fit_bg = FITNESS_DISPLAY[bmi_cat]
daily_cal = calculate_daily_calories(weight, height, age, gender, condition)

st.markdown(f"""
<div style='background:linear-gradient(135deg,#1A2F2A,#2E7D32); border-radius:20px;
            padding:1.8rem 2rem; color:white; margin-bottom:1.5rem;'>
    <p style='font-family:Lora,serif; font-size:1.6rem; font-weight:600;
              color:#C8E6C9 !important; margin:0 0 1rem 0;'>Your Profile</p>
    <span style='display:inline-block; background:rgba(255,255,255,0.15);
                 border-radius:50px; padding:0.35rem 1rem; margin:0.2rem;
                 font-size:0.9rem; font-weight:600; color:white !important;'>{fit_icon} {age} years old · {gender}</span>
    <span style='display:inline-block; background:rgba(255,255,255,0.15);
                 border-radius:50px; padding:0.35rem 1rem; margin:0.2rem;
                 font-size:0.9rem; font-weight:600; color:white !important;'>📏 {height:.0f} cm &nbsp; {weight:.0f} kg</span>
    <span style='display:inline-block; background:rgba(255,255,255,0.15);
                 border-radius:50px; padding:0.35rem 1rem; margin:0.2rem;
                 font-size:0.9rem; font-weight:600; color:white !important;'>⚖️ BMI {bmi:.1f} — {fit_msg}</span>
    <span style='display:inline-block; background:rgba(255,255,255,0.15);
                 border-radius:50px; padding:0.35rem 1rem; margin:0.2rem;
                 font-size:0.9rem; font-weight:600; color:white !important;'>{cond_icon} {cond_label}{" (" + diabetes_type + ")" if diabetes_type else ""}</span>
    <span style='display:inline-block; background:rgba(255,255,255,0.15);
                 border-radius:50px; padding:0.35rem 1rem; margin:0.2rem;
                 font-size:0.9rem; font-weight:600; color:white !important;'>🥗 {diet_sel}</span>
    <br><br>
    <p style='color:rgba(255,255,255,0.85) !important; font-size:0.9rem; margin:0;'>
        Your daily calorie goal: &nbsp;
        <strong style='color:white !important; font-size:1.15rem;'>{daily_cal} kcal</strong>
        &nbsp; — calculated for your body using the Mifflin-St Jeor formula
    </p>
</div>
""", unsafe_allow_html=True)


# ── Health Assessment ─────────────────────────────────────────────────────────
pred_condition, confidence = run_ml_prediction(condition, diet_pref)
pred_label, pred_icon, pred_color, pred_bg = CONDITION_DISPLAY.get(
    pred_condition, CONDITION_DISPLAY["healthy"]
)

confidence_pct = int(confidence * 100)

ASSESSMENT_MESSAGES = {
    "healthy":      "Great news! Your nutritional profile looks well-balanced. Keep up the good habits!",
    "diabetes":     "Your meal plan is carefully designed to keep your blood sugar steady throughout the day.",
    "hypertension": "Your meals are chosen to be low in salt and gentle on your blood pressure.",
    "obesity":      "Your plan focuses on satisfying, lower-calorie meals to support your weight goals.",
}

col_assess, col_space = st.columns([2, 1])
with col_assess:
    st.markdown(f"""
    <div class='assessment-card' style='background: linear-gradient(135deg, {pred_color}CC, {pred_color});'>
        <span class='assessment-icon'>{pred_icon}</span>
        <p class='assessment-title'>Your Health Assessment</p>
        <p class='assessment-msg'>{ASSESSMENT_MESSAGES.get(pred_condition, "")}</p>
        <div class='confidence-bar-wrap'>
            <div class='confidence-bar-fill' style='width:{confidence_pct}%'></div>
        </div>
        <p class='confidence-label'>Our assessment is <strong>{confidence_pct}% confident</strong> for your profile</p>
    </div>
    """, unsafe_allow_html=True)

with col_space:
    st.markdown(f"""
    <div style='background:{cond_bg}; border-radius:16px; padding:1.4rem;
                height:100%; display:flex; flex-direction:column; justify-content:center;
                border: 2px solid {cond_color}33;'>
        <p style='color:{cond_color}; font-weight:800; font-size:1.1rem; margin:0 0 0.5rem 0;'>
            {cond_icon} {cond_label}
        </p>
        <p style='color:#555; font-size:0.9rem; margin:0; line-height:1.6;'>
            Daily goal: <strong>{daily_cal} kcal</strong><br>
            Fitness level: <strong>{bmi_cat}</strong><br>
            Diet: <strong>{diet_sel}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# MEAL PLAN
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style='background:white; border-radius:20px; padding:1.4rem 2rem;
            box-shadow:0 2px 10px rgba(0,0,0,0.05); border:2px solid #E8F5E9;
            margin-bottom:1.2rem;'>
    <h2 style='font-family: Lora, serif; color:#1A2F2A; margin:0 0 0.4rem 0;
               font-size:1.5rem;'>🍽️ Your Personal Meal Plan</h2>
    <p style='color:#666; margin:0; font-size:0.95rem;'>
        Each meal below is chosen to fit within your daily goal of <strong>{daily_cal} kcal</strong>.
        We allow ±50 kcal flexibility per meal so you have real options to choose from.
    </p>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["🌅 Breakfast", "☀️ Lunch", "🍵 Snack", "🌙 Dinner"])
best_per_slot = {}
slots = ["breakfast", "lunch", "snack", "dinner"]

for tab, slot in zip(tabs, slots):
    target_cal = int(daily_cal * SLOT_CALORIE_SPLIT[slot])
    recs = recommend_for_slot(condition, diet_pref, slot, target_cal)
    slot_icon, slot_label = SLOT_FRIENDLY[slot]

    with tab:
        st.markdown(f"""
        <div style='background:#E8F5E9; border-radius:12px; padding:0.9rem 1.2rem;
                    margin-bottom:1rem; border:1.5px solid #A5D6A7;'>
            <span style='color:#1B5E20 !important; font-weight:800; font-size:1rem;'>Aim for around {target_cal} kcal</span>
            <span style='color:#388E3C !important; font-size:0.88rem;'>
                &nbsp; (anything between {target_cal - 50} and {target_cal + 50} kcal is perfect)
            </span>
        </div>
        """, unsafe_allow_html=True)

        if not recs:
            st.markdown("""
            <div style='background:#FFF3E0; border-radius:12px; padding:1rem 1.4rem;'>
                ⚠️ We couldn't find matching meals for this slot with your preferences.
                Try switching to "Both are fine" for more options.
            </div>
            """, unsafe_allow_html=True)
            continue

        best_per_slot[slot] = recs[0]

        for i, meal in enumerate(recs):
            diff = meal["calories_slot"] - target_cal
            diff_label = f"+{diff:.0f} kcal" if diff > 5 else (f"{diff:.0f} kcal" if diff < -5 else "right on target ✓")
            diet_tag = "🥗 Vegetarian" if meal["diet"] == "vegetarian" else "🍗 Non-Vegetarian"

            with st.expander(
                f"{'⭐ ' if i == 0 else '  '}{meal['title']}   —   {meal['calories_slot']:.0f} kcal   •   {diet_tag}",
                expanded=(i == 0)
            ):
                if i == 0:
                    st.markdown("<span class='best-pick-banner'>✅ Best match for you</span>", unsafe_allow_html=True)

                c1, c2 = st.columns([1, 1])

                with c1:
                    st.markdown("<p style='font-weight:700; color:#1A2F2A; margin-bottom:0.4rem;'>What's in this meal:</p>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style='margin-top:0.2rem;'>
                        <span class='nutrient-pill'>🔥 {meal['calories_slot']:.0f} kcal energy</span>
                        <span class='nutrient-pill'>💪 {meal['protein_slot']:.1f}g protein</span>
                        <span class='nutrient-pill'>🌾 {meal['carbs_slot']:.1f}g carbs</span>
                        <span class='nutrient-pill'>🧈 {meal['fat_slot']:.1f}g fat</span>
                        <span class='nutrient-pill'>🧂 {meal['sodium_slot_mg']:.0f}mg salt</span>
                    </div>
                    <p style='color:#555 !important; font-size:0.82rem; margin-top:0.6rem;'>
                        Portion size: <strong style='color:#1A2F2A;'>{meal['slot_portion_g']}g</strong>
                        &nbsp;|&nbsp; {diff_label}
                    </p>
                    """, unsafe_allow_html=True)

                with c2:
                    st.markdown("<p style='font-weight:700; color:#1A2F2A; margin-bottom:0.4rem;'>How this meal compares to your goal:</p>", unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(4, 2.6))
                    fig.patch.set_facecolor("#FDFAF6")
                    ax.set_facecolor("#FDFAF6")

                    bar_labels  = ["Energy\n(kcal)", "Carbs\n(g)", "Fat\n(g)"]
                    meal_vals   = [meal["calories_slot"], meal["carbs_slot"], meal["fat_slot"]]
                    limit_vals  = [target_cal, SLOT_CARB_LIMITS[condition], SLOT_FAT_LIMITS[condition]]
                    xp = np.arange(3)

                    ax.bar(xp - 0.2, meal_vals,  0.35, label="This meal",   color="#4CAF50", alpha=0.85)
                    ax.bar(xp + 0.2, limit_vals, 0.35, label="Your target", color="#BDBDBD", alpha=0.7)
                    ax.set_xticks(xp)
                    ax.set_xticklabels(bar_labels, fontsize=8, color="#555")
                    ax.tick_params(colors="#555")
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)
                    ax.spines["left"].set_color("#DDD")
                    ax.spines["bottom"].set_color("#DDD")
                    ax.legend(fontsize=7, framealpha=0)
                    plt.tight_layout(pad=0.5)
                    st.pyplot(fig)
                    plt.close()

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# DAILY SUMMARY
# ════════════════════════════════════════════════════════════════════════════
if best_per_slot:
    total_cal  = sum(m["calories_slot"]  for m in best_per_slot.values())
    total_prot = sum(m["protein_slot"]   for m in best_per_slot.values())
    total_fat  = sum(m["fat_slot"]       for m in best_per_slot.values())
    total_carb = sum(m["carbs_slot"]     for m in best_per_slot.values())
    total_sod  = sum(m["sodium_slot_mg"] for m in best_per_slot.values())
    diff       = total_cal - daily_cal

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#1A2F2A,#2E7D32);
                border-radius:20px; padding:1.6rem 2rem; margin-top:1.5rem;'>
        <p style='font-family:Lora,serif; color:#C8E6C9 !important;
                  margin:0; font-size:1.5rem; font-weight:600;
                  text-shadow:0 1px 3px rgba(0,0,0,0.3);'>
            📊 Today's Nutrition at a Glance
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    summary_items = [
        (c1, f"{total_cal:.0f}", "Total calories today", "🔥"),
        (c2, f"{total_prot:.0f}g", "Protein (builds muscle)", "💪"),
        (c3, f"{total_fat:.0f}g", "Fat (healthy fats)", "🧈"),
        (c4, f"{total_carb:.0f}g", "Carbohydrates (energy)", "🌾"),
        (c5, f"{total_sod:.0f}mg", "Salt (keep it low)", "🧂"),
    ]

    for col, val, lbl, icon in summary_items:
        col.markdown(f"""
        <div style='background:#FFFFFF; border-radius:14px; padding:1rem 0.6rem;
                    text-align:center; border:2px solid #A5D6A7;
                    box-shadow:0 3px 10px rgba(46,125,50,0.12); margin-top:0.6rem;'>
            <p style='font-size:1.6rem; line-height:1; margin:0; padding:0;
                      color:#1A2F2A !important;'>{icon}</p>
            <p style='font-size:1.4rem; font-weight:800; margin:0.3rem 0 0.1rem 0;
                      padding:0; color:#1A2F2A !important; line-height:1.2;'>{val}</p>
            <p style='font-size:0.72rem; color:#2E7D32 !important; margin:0; padding:0;
                      line-height:1.4; font-weight:700;'>{lbl}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if abs(diff) <= 100:
        st.markdown(f"""
        <div style='background:#E8F5E9; border-left:5px solid #4CAF50; border-radius:12px;
                    padding:1rem 1.4rem; color:#1B5E20 !important;'>
            <strong style='color:#1B5E20;'>✅ You're on track!</strong>
            <span style='color:#2E7D32;'> Your total today is
            <strong style='color:#1A2F2A;'>{total_cal:.0f} kcal</strong>,
            which is very close to your goal of {daily_cal} kcal. Well done!</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        direction = "a bit over" if diff > 0 else "a bit under"
        st.markdown(f"""
        <div style='background:#FFF3E0; border-left:5px solid #FF9800; border-radius:12px;
                    padding:1rem 1.4rem; color:#E65100 !important;'>
            <strong style='color:#E65100;'>⚠️ Heads up!</strong>
            <span style='color:#BF360C;'> Your total today is
            <strong style='color:#1A2F2A;'>{total_cal:.0f} kcal</strong> — {direction} your goal of {daily_cal} kcal
            by {abs(diff):.0f} kcal. Try swapping one meal for a lighter option.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Nutrition balance chart
    col_pie, col_bar = st.columns(2)

    with col_pie:
        st.markdown("**Nutrition Balance**")
        st.caption("How your energy is split between the three main nutrients")
        fig, ax = plt.subplots(figsize=(4, 3.5))
        fig.patch.set_facecolor("#FDFAF6")
        macro_vals   = [total_prot * 4, total_fat * 9, total_carb * 4]
        macro_labels = [f"Protein\n{total_prot:.0f}g", f"Fat\n{total_fat:.0f}g", f"Carbs\n{total_carb:.0f}g"]
        wedges, texts, autotexts = ax.pie(
            macro_vals, labels=macro_labels, autopct="%1.0f%%", startangle=90,
            colors=["#4CAF50", "#FF9800", "#42A5F5"],
            wedgeprops=dict(edgecolor="white", linewidth=2)
        )
        for t in autotexts:
            t.set_fontsize(9)
            t.set_color("white")
            t.set_fontweight("bold")
        plt.tight_layout(pad=0.5)
        st.pyplot(fig)
        plt.close()

    with col_bar:
        st.markdown("**How your meals compare to your goal**")
        st.caption("Green = what we recommend, Grey = your daily target")
        fig, ax = plt.subplots(figsize=(4, 3.5))
        fig.patch.set_facecolor("#FDFAF6")
        ax.set_facecolor("#FDFAF6")

        snames = list(best_per_slot.keys())
        scals  = [best_per_slot[s]["calories_slot"] for s in snames]
        stargs = [int(daily_cal * SLOT_CALORIE_SPLIT[s]) for s in snames]
        xp     = np.arange(len(snames))
        friendly_names = ["Breakfast", "Lunch", "Snack", "Dinner"][:len(snames)]

        ax.bar(xp - 0.2, scals,  0.35, label="Recommended", color="#4CAF50", alpha=0.85)
        ax.bar(xp + 0.2, stargs, 0.35, label="Your target",  color="#BDBDBD", alpha=0.7)
        ax.set_xticks(xp)
        ax.set_xticklabels(friendly_names, fontsize=9, color="#555")
        ax.set_ylabel("Calories (kcal)", fontsize=8, color="#777")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#DDD")
        ax.spines["bottom"].set_color("#DDD")
        ax.legend(fontsize=8, framealpha=0)
        plt.tight_layout(pad=0.5)
        st.pyplot(fig)
        plt.close()


# ════════════════════════════════════════════════════════════════════════════
# DIETARY TIPS
# ════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
tips = CONDITION_TIPS.get(condition, CONDITION_TIPS["healthy"])

st.markdown(f"""
<div class='guideline-card'>
    <h3>💡 Simple tips for {cond_label}</h3>
    {"".join(f"<div class='guideline-tip'><span style='font-size:1.2rem;'>{icon}</span><span>{tip}</span></div>" for icon, tip in tips)}
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='disclaimer'>
    🩺 SmartDiet is a meal guidance tool, not a medical prescription.<br>
    Always talk to your doctor or a registered dietitian before making big changes to your diet.
</div>
""", unsafe_allow_html=True)
