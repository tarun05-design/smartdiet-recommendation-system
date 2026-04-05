import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="SmartDiet — Personal Meal Planner",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=DM+Serif+Display&display=swap');

:root {
    --bg: #F6F8F7;
    --surface: #FFFFFF;
    --surface-2: #F4F8F6;
    --text: #15221B;
    --muted: #67766F;
    --line: #E3EBE7;
    --primary: #1DB954;
    --primary-dark: #159447;
    --primary-soft: #EAF8EF;
    --shadow-soft: 0 4px 14px rgba(20, 34, 27, 0.05);
    --shadow: 0 10px 28px rgba(20, 34, 27, 0.08);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #F7FAF8 0%, #F3F7F5 100%) !important;
    color: var(--text);
}

div.block-container {
    max-width: 1220px;
    padding-top: 1.15rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0;
    position: fixed;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F1E18 0%, #153126 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
    width: 370px !important;
}

section[data-testid="stSidebar"] * {
    color: #F4FCF7 !important;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.1rem;
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stTextInput label,
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stNumberInput label {
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    color: #B9D9C7 !important;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] [data-baseweb="input"] > div,
section[data-testid="stSidebar"] [data-baseweb="base-input"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] input {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] .stButton button {
    width: 100%;
    height: 52px;
    border: none;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--primary) 0%, #41C96C 100%) !important;
    color: white !important;
    font-weight: 800;
    font-size: 1rem;
    box-shadow: 0 10px 24px rgba(29, 185, 84, 0.26);
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: linear-gradient(90deg, var(--primary-dark) 0%, #2FB85A 100%) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 0.6rem;
    border-bottom: 1px solid var(--line);
    padding-bottom: 0.75rem;
}

.stTabs [data-baseweb="tab"] {
    padding: 0.7rem 1.15rem;
    background: #EDF3EF !important;
    border-radius: 999px !important;
    color: #355044 !important;
    font-weight: 700;
}

.stTabs [aria-selected="true"] {
    background: #14221B !important;
    color: #FFFFFF !important;
}

[data-testid="stExpander"] {
    border: none !important;
    background: transparent !important;
}

[data-testid="stExpander"] summary {
    background: #FFFFFF !important;
    border: 1px solid var(--line) !important;
    border-radius: 18px !important;
    padding: 0.8rem 1rem !important;
    box-shadow: var(--shadow-soft);
}

[data-testid="stExpander"] > div:last-child {
    background: #FFFFFF !important;
    border: 1px solid var(--line) !important;
    border-top: none !important;
    border-radius: 0 0 18px 18px !important;
    padding: 0.4rem 0.35rem 0.8rem 0.35rem;
}

.sd-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 24px;
    box-shadow: var(--shadow-soft);
}

.sd-hero {
    position: relative;
    overflow: hidden;
    padding: 1.6rem 1.8rem;
    background: linear-gradient(135deg, #14221B 0%, #1B3D2E 52%, #1DB954 100%);
    border-radius: 28px;
    color: white;
    box-shadow: 0 18px 40px rgba(20, 34, 27, 0.20);
}

.sd-hero::after {
    content: '🍎';
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.12;
}

.sd-eyebrow {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.15);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    margin-bottom: 0.8rem;
}

.sd-hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.25rem;
    line-height: 1.12;
    margin: 0 0 0.45rem 0;
}

.sd-hero-sub {
    max-width: 760px;
    font-size: 1rem;
    line-height: 1.7;
    color: rgba(255,255,255,0.88);
    margin: 0;
}

.sd-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1rem;
}

.sd-card-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--text);
    margin: 0 0 0.9rem 0;
}

.sd-mini-box {
    padding: 0.9rem 1rem;
    background: #F6FAF8;
    border: 1px solid #E3EBE7;
    border-radius: 18px;
    color: #31493F;
    line-height: 1.65;
    font-size: 0.96rem;
}

.sd-profile {
    padding: 1.2rem;
    background: linear-gradient(180deg, #FFFFFF 0%, #F9FCFA 100%);
}

.sd-pill-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    margin-bottom: 1rem;
}

.sd-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.55rem 0.9rem;
    background: var(--surface-2);
    color: #244236;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 700;
}

.sd-goal {
    background: linear-gradient(180deg, #F3FBF5 0%, #ECF8F0 100%);
    border: 1px solid #DCEFE3;
    border-radius: 18px;
    padding: 1rem;
}

.sd-goal-big {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1;
}

.sd-goal-sub {
    margin-top: 0.35rem;
    font-size: 0.92rem;
    color: var(--muted);
    line-height: 1.55;
}

.sd-assessment {
    padding: 1.2rem;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.sd-assessment h3 {
    margin: 0;
    font-size: 1.05rem;
    font-weight: 800;
}

.sd-assessment-main {
    margin-top: 0.7rem;
    font-size: 1.85rem;
    font-weight: 800;
    line-height: 1.1;
}

.sd-assessment-text {
    margin-top: 0.55rem;
    font-size: 0.95rem;
    line-height: 1.6;
    opacity: 0.96;
}

.sd-progress {
    width: 100%;
    height: 10px;
    border-radius: 999px;
    background: rgba(255,255,255,0.24);
    overflow: hidden;
    margin-top: 1rem;
}

.sd-progress > div {
    height: 100%;
    border-radius: 999px;
    background: rgba(255,255,255,0.95);
}

.sd-section-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-top: 1.1rem;
    margin-bottom: 0.9rem;
}

.sd-section-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--text);
    margin: 0;
}

.sd-section-sub {
    font-size: 0.94rem;
    color: var(--muted);
    margin-top: 0.22rem;
}

.sd-badge {
    background: var(--primary-soft);
    color: #177A3F;
    border-radius: 999px;
    padding: 0.55rem 0.9rem;
    font-weight: 800;
    font-size: 0.85rem;
}

.sd-meal-banner {
    padding: 0.9rem 1rem;
    border-radius: 18px;
    background: linear-gradient(90deg, #F1F9F4 0%, #FFFFFF 100%);
    border: 1px solid #DCEFE3;
    margin-bottom: 1rem;
}

.sd-metric-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.9rem;
    margin-top: 0.65rem;
}

.sd-stat {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 1rem 0.9rem;
    text-align: center;
    box-shadow: var(--shadow-soft);
}

.sd-stat-icon {
    font-size: 1.6rem;
    line-height: 1;
}

.sd-stat-value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text);
    margin-top: 0.45rem;
    line-height: 1;
}

.sd-stat-label {
    font-size: 0.82rem;
    color: var(--muted);
    font-weight: 700;
    margin-top: 0.42rem;
    line-height: 1.45;
}

.sd-alert {
    border-radius: 18px;
    padding: 1rem 1.1rem;
    font-size: 1rem;
    line-height: 1.65;
    border-left: 6px solid;
    margin-top: 1rem;
}

.sd-tips {
    padding: 1.2rem;
}

.sd-tip {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    padding: 0.8rem 0;
    border-bottom: 1px dashed var(--line);
    font-size: 0.95rem;
    color: #29463A;
    line-height: 1.65;
}

.sd-tip:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.sd-footer-note {
    margin-top: 1.5rem;
    text-align: center;
    font-size: 0.85rem;
    color: #728078;
}

@media (max-width: 1100px) {
    .sd-grid-2 {
        grid-template-columns: 1fr;
    }

    .sd-metric-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 700px) {
    div.block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .sd-hero {
        padding: 1.3rem;
    }

    .sd-hero-title {
        font-size: 2rem;
    }

    .sd-metric-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")

@st.cache_resource
def load_all():
    rf = joblib.load(f"{MODEL_DIR}/rf_model.pkl")
    gb = joblib.load(f"{MODEL_DIR}/gb_model.pkl")
    scaler = joblib.load(f"{MODEL_DIR}/scaler.pkl")
    le_target = joblib.load(f"{MODEL_DIR}/le_target.pkl")
    le_diet = joblib.load(f"{MODEL_DIR}/le_diet.pkl")
    le_meal = joblib.load(f"{MODEL_DIR}/le_meal.pkl")
    le_dish = joblib.load(f"{MODEL_DIR}/le_dish.pkl")
    df = pd.read_csv(f"{MODEL_DIR}/meals_extended_labelled.csv")
    with open(f"{MODEL_DIR}/meta.json") as f:
        meta = json.load(f)
    return rf, gb, scaler, le_target, le_diet, le_meal, le_dish, df, meta

rf, gb, scaler, le_target, le_diet, le_meal, le_dish, meals_df, meta = load_all()

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
    "lunch": 0.35,
    "snack": 0.10,
    "dinner": 0.30,
}

SLOT_MEAL_TIME = {
    "breakfast": ["breakfast", "breakfast/dinner"],
    "lunch": ["lunch", "lunch/dinner"],
    "snack": ["snack"],
    "dinner": ["dinner", "lunch/dinner", "breakfast/dinner"],
}

SLOT_CARB_LIMITS = {"diabetes": 55, "hypertension": 65, "obesity": 50, "healthy": 75}
SLOT_FAT_LIMITS = {"diabetes": 15, "hypertension": 15, "obesity": 10, "healthy": 20}

CONDITION_DISPLAY = {
    "healthy": ("Healthy", "🌿", "#1DB954", "#EAF8EF"),
    "diabetes": ("Managing Diabetes", "🩸", "#E6492D", "#FFF2EE"),
    "hypertension": ("Managing Blood Pressure", "💙", "#2D7DF6", "#EDF4FF"),
    "obesity": ("Managing Weight", "⚖️", "#8E44EC", "#F6F0FF"),
}

FITNESS_DISPLAY = {
    "Slightly Slim": ("Lean profile", "🌱", "#2D7DF6", "#EDF6FF"),
    "Fit": ("Great shape", "💪", "#1DB954", "#EAF8EF"),
    "Overweight": ("Above ideal range", "🌤️", "#FF9F1C", "#FFF7E9"),
    "Obese": ("Weight support recommended", "🌸", "#8E44EC", "#F6F0FF"),
}

CONDITION_TIPS = {
    "diabetes": [
        ("🌾", "Choose slower-digesting carbs like ragi, oats, and brown rice more often than polished rice."),
        ("⏰", "Keep meal timing regular. Smaller, balanced meals help avoid sharp glucose spikes."),
        ("🚫", "Limit sweets, packaged snacks, and fruit juices because they can raise blood sugar quickly."),
        ("💧", "Stay hydrated with water, buttermilk, and other unsweetened drinks."),
    ],
    "hypertension": [
        ("🧂", "Reduce pickles, papad, chips, and processed foods because most hidden sodium comes from these."),
        ("🍌", "Add potassium-rich foods like banana, curd, greens, and coconut water when suitable."),
        ("🚶", "A short daily walk can support healthier blood pressure over time."),
        ("☕", "Moderate caffeine if you notice it affects your blood pressure."),
    ],
    "obesity": [
        ("🍽️", "Use portion-friendly plates and eat a little slower so fullness catches up naturally."),
        ("🥚", "Include protein in each meal to stay full longer and reduce overeating."),
        ("🚫", "Cut down deep-fried foods, sugar drinks, and heavily refined snacks first."),
        ("🚶", "Pair your food plan with simple movement like walking or light exercise."),
    ],
    "healthy": [
        ("🥗", "Build meals around vegetables, dal, curd, fruit, and consistent hydration."),
        ("🥛", "Add a fermented dairy option like curd or buttermilk when it suits you."),
        ("🌿", "Choose seasonal produce often because it is usually fresher, cheaper, and nutrient-dense."),
        ("💧", "Good hydration improves energy, digestion, and appetite control."),
    ],
}

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Slightly Slim"
    elif bmi < 25.0:
        return "Fit"
    elif bmi < 30.0:
        return "Overweight"
    return "Obese"

def get_diet_options(preference):
    if preference == "Vegetarian":
        return ["vegetarian"]
    elif preference == "Non-Vegetarian":
        return ["non_vegetarian"]
    return ["vegetarian", "non_vegetarian"]

def recommend_for_slot(condition, diet_pref, slot, target_cal, tolerance=50):
    diet_opts = get_diet_options(diet_pref)
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
    cols = [
        "title", "diet", "calories_slot", "protein_slot", "fat_slot",
        "carbs_slot", "sodium_slot_mg", "slot_portion_g"
    ]
    return top3[cols].to_dict("records")

def run_ml_prediction(condition, diet_pref):
    sample_meals = meals_df[meals_df["condition"] == condition]
    if sample_meals.empty:
        sample_meals = meals_df

    rep = sample_meals[[
        "calories_slot", "protein_slot", "fat_slot",
        "carbs_slot", "sodium_slot_mg", "slot_portion_g"
    ]].median()

    try:
        d_enc = le_diet.transform([get_diet_options(diet_pref)[0]])[0]
        m_enc = le_meal.transform(["breakfast"])[0]
        t_enc = le_dish.transform(["main"])[0]
    except Exception:
        d_enc, m_enc, t_enc = 0, 0, 0

    x_sample = np.array([[
        rep["calories_slot"], rep["protein_slot"], rep["fat_slot"],
        rep["carbs_slot"], rep["sodium_slot_mg"], rep["slot_portion_g"],
        d_enc, m_enc, t_enc
    ]])

    proba = rf.predict_proba(scaler.transform(x_sample))[0]
    pred = le_target.classes_[np.argmax(proba)]
    confidence = float(proba.max())
    return pred, confidence

def render_hero(name):
    greeting = f"Hey {name}, your SmartDiet plan is ready" if name else "Your SmartDiet plan is ready"
    st.markdown(f"""
    <div class='sd-hero'>
        <div class='sd-eyebrow'>Personalized meal planning</div>
        <div class='sd-hero-title'>{greeting}</div>
        <p class='sd-hero-sub'>
            Here are simple meal suggestions based on your age, height, weight, health condition, and food preference.
            The goal is to help you choose meals more easily throughout the day.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_profile_card(age, gender, height, weight, bmi, fit_msg, fit_icon, condition_label, condition_icon, diet_label, daily_cal):
    st.markdown(f"""
    <div class='sd-card sd-profile'>
        <div class='sd-card-title'>Your profile</div>
        <div class='sd-pill-wrap'>
            <span class='sd-pill'>{fit_icon} {age} years · {gender}</span>
            <span class='sd-pill'>📏 {height:.0f} cm · {weight:.0f} kg</span>
            <span class='sd-pill'>⚖️ BMI {bmi:.1f} · {fit_msg}</span>
            <span class='sd-pill'>{condition_icon} {condition_label}</span>
            <span class='sd-pill'>🥗 {diet_label}</span>
        </div>
        <div class='sd-goal'>
            <div class='sd-goal-big'>{daily_cal} kcal</div>
            <div class='sd-goal-sub'>Estimated daily calorie goal based on your profile and selected condition.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_assessment_card(pred_label, pred_icon, pred_color, confidence_pct, assessment_message):
    st.markdown(f"""
    <div class='sd-card sd-assessment' style='background: linear-gradient(135deg, {pred_color} 0%, {pred_color}DD 100%);'>
        <div>
            <h3>{pred_icon} Health assessment</h3>
            <div class='sd-assessment-main'>{pred_label}</div>
            <div class='sd-assessment-text'>{assessment_message}</div>
        </div>
        <div>
            <div class='sd-progress'><div style='width:{confidence_pct}%;'></div></div>
            <div style='margin-top:0.55rem; font-size:0.88rem; font-weight:700;'>Confidence: {confidence_pct}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if "show_plan" not in st.session_state:
    st.session_state.show_plan = False

with st.sidebar:
    st.markdown("""
    <div style='padding: 0.3rem 0 1rem 0;'>
        <div style='display:flex; align-items:center; gap:0.7rem;'>
            <div style='width:46px; height:46px; border-radius:14px; background:linear-gradient(135deg,#1DB954,#6BE28E); display:flex; align-items:center; justify-content:center; font-size:1.35rem;'>🍎</div>
            <div>
                <div style='font-size:1.25rem; font-weight:800;'>SmartDiet</div>
                <div style='font-size:0.84rem; color:#B9D9C7;'>Personal meal planner</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.78rem; font-weight:800; color:#8EC9A8; margin-bottom:0.5rem;'>PERSONAL PROFILE</div>", unsafe_allow_html=True)
    name = st.text_input("Your name", placeholder="e.g. Priya")

    age_col, gender_col = st.columns(2)
    with age_col:
        age = st.slider("Age", 10, 90, 35)
    with gender_col:
        gender = st.selectbox("Gender", ["Female", "Male"])

    height = st.slider("Height (cm)", 120, 220, 165)
    weight = st.slider("Weight (kg)", 30, 180, 65)

    bmi = weight / ((height / 100) ** 2)
    bmi_cat = get_bmi_category(bmi)
    fit_msg, fit_icon, fit_color, fit_bg = FITNESS_DISPLAY[bmi_cat]

    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.06); border-radius:18px; padding:0.9rem 1rem; margin:0.65rem 0 1rem 0;'>
        <div style='display:flex; align-items:center; justify-content:space-between;'>
            <div style='font-size:0.83rem; color:#B9D9C7;'>Current BMI</div>
            <div style='font-size:0.83rem; color:#DDF7E6; font-weight:800;'>{bmi_cat}</div>
        </div>
        <div style='font-size:2rem; font-weight:800; margin-top:0.25rem;'>{bmi:.1f}</div>
        <div style='font-size:0.9rem; color:#DDF7E6; margin-top:0.25rem;'>{fit_icon} {fit_msg}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.78rem; font-weight:800; color:#8EC9A8; margin-bottom:0.5rem;'>HEALTH GOAL</div>", unsafe_allow_html=True)
    condition_options = ["I'm Healthy", "Managing Diabetes", "Managing Blood Pressure", "Managing My Weight"]
    condition_sel = st.selectbox("Which best describes you?", condition_options)
    condition_map = {
        "I'm Healthy": "healthy",
        "Managing Diabetes": "diabetes",
        "Managing Blood Pressure": "hypertension",
        "Managing My Weight": "obesity",
    }
    condition = condition_map[condition_sel]

    diabetes_type = None
    if condition == "diabetes":
        diabetes_type = st.selectbox("Diabetes type", ["Pre-Diabetic", "Type 1", "Type 2"])

    st.markdown("<div style='font-size:0.78rem; font-weight:800; color:#8EC9A8; margin:0.95rem 0 0.5rem 0;'>FOOD PREFERENCE</div>", unsafe_allow_html=True)
    diet_sel = st.radio("Diet preference", ["Only Vegetarian", "Non-Vegetarian", "Both are fine"])
    diet_map = {
        "Only Vegetarian": "Vegetarian",
        "Non-Vegetarian": "Non-Vegetarian",
        "Both are fine": "Balanced",
    }
    diet_pref = diet_map[diet_sel]

    st.markdown("<div style='height:0.55rem'></div>", unsafe_allow_html=True)
    if st.button("✨ Generate Smart Plan", use_container_width=True):
        st.session_state.show_plan = True

render_hero(name)

if not st.session_state.show_plan:
    st.markdown("""
    <div class='sd-grid-2' style='margin-top:0.9rem;'>
        <div class='sd-card' style='padding:1rem;'>
            <div class='sd-card-title' style='margin-bottom:0.75rem;'>Why we built SmartDiet</div>
            <div style='display:flex; flex-direction:column; gap:0.7rem;'>
                <div class='sd-mini-box'>
                    Many people want healthier food choices, but they are often unsure what to eat for each part of the day.
                </div>
                <div class='sd-mini-box'>
                    SmartDiet turns personal health details into practical meal recommendations so daily planning feels simpler and more useful.
                </div>
                <div class='sd-mini-box'>
                    It combines body profile, calorie needs, health condition, and food preference to create a more personalized meal plan.
                </div>
            </div>
        </div>
        <div class='sd-card' style='padding:1rem;'>
            <div class='sd-card-title' style='margin-bottom:0.75rem;'>How to use it</div>
            <div style='display:flex; flex-direction:column; gap:0.7rem;'>
                <div class='sd-mini-box'>1. Enter your details in the left panel, including age, gender, height, weight, and food preference.</div>
                <div class='sd-mini-box'>2. Choose the health condition that best matches you and click <strong>Generate Smart Plan</strong>.</div>
                <div class='sd-mini-box'>3. Review your recommended meals, nutrition summary, and helpful daily tips.</div>
            </div>
        </div>
    </div>
    <div class='sd-card' style='padding:0.9rem 1rem; margin-top:0.9rem;'>
        <div style='font-size:0.95rem; color:#31493F; line-height:1.7;'>
            <strong>What you get after generating the plan:</strong> a daily calorie target, meal suggestions for breakfast, lunch, snack, and dinner, a nutrition summary, and simple food guidance based on your selected condition.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if condition == "healthy" and bmi_cat == "Obese":
    st.markdown("""
    <div class='sd-alert' style='background:#FFF8E8; border-left-color:#FFB020; color:#8A4B00;'>
        <strong>Smart adjustment:</strong> based on your BMI, the plan has been shifted toward weight management for more suitable recommendations.
    </div>
    """, unsafe_allow_html=True)
    condition = "obesity"

cond_label, cond_icon, cond_color, cond_bg = CONDITION_DISPLAY[condition]
fit_msg, fit_icon, fit_color, fit_bg = FITNESS_DISPLAY[bmi_cat]
daily_cal = calculate_daily_calories(weight, height, age, gender, condition)

pred_condition, confidence = run_ml_prediction(condition, diet_pref)
pred_label, pred_icon, pred_color, pred_bg = CONDITION_DISPLAY.get(pred_condition, CONDITION_DISPLAY["healthy"])
confidence_pct = int(confidence * 100)

ASSESSMENT_MESSAGES = {
    "healthy": "Your nutritional profile looks balanced. Keep your routine consistent and hydrated.",
    "diabetes": "Meals are chosen to support steadier blood sugar and better carbohydrate control.",
    "hypertension": "The plan prefers lower-sodium choices that are friendlier for blood pressure management.",
    "obesity": "Meals are selected to stay satisfying while keeping daily energy intake more controlled.",
}

left_col, right_col = st.columns([1.15, 0.85])
with left_col:
    render_profile_card(
        age=age,
        gender=gender,
        height=height,
        weight=weight,
        bmi=bmi,
        fit_msg=fit_msg,
        fit_icon=fit_icon,
        condition_label=cond_label + (f" · {diabetes_type}" if diabetes_type else ""),
        condition_icon=cond_icon,
        diet_label=diet_sel,
        daily_cal=daily_cal,
    )
with right_col:
    render_assessment_card(
        pred_label=pred_label,
        pred_icon=pred_icon,
        pred_color=pred_color,
        confidence_pct=confidence_pct,
        assessment_message=ASSESSMENT_MESSAGES.get(pred_condition, ""),
    )

st.markdown("""
<div class='sd-section-head'>
    <div>
        <div class='sd-section-title'>Meal planner</div>
        <div class='sd-section-sub'>Breakfast, lunch, snack, and dinner recommendations matched to your daily calorie target.</div>
    </div>
    <div class='sd-badge'>Personalized suggestions</div>
</div>
""", unsafe_allow_html=True)

best_per_slot = {}
slots = ["breakfast", "lunch", "snack", "dinner"]
tabs = st.tabs(["🌅 Breakfast", "☀️ Lunch", "🍵 Snack", "🌙 Dinner"])

for tab, slot in zip(tabs, slots):
    target_cal = int(daily_cal * SLOT_CALORIE_SPLIT[slot])
    recs = recommend_for_slot(condition, diet_pref, slot, target_cal)

    with tab:
        st.markdown(f"""
        <div class='sd-meal-banner'>
            <strong style='color:#17442F;'>Target for this meal:</strong>
            <span style='color:#3A5A4D;'> around <strong>{target_cal} kcal</strong> with a flexibility of ±50 kcal</span>
        </div>
        """, unsafe_allow_html=True)

        if not recs:
            st.markdown("""
            <div class='sd-alert' style='background:#FFF8E8; border-left-color:#FFB020; color:#8A4B00;'>
                No close meal match was found for this slot with the current diet preference.
            </div>
            """, unsafe_allow_html=True)
            continue

        best_per_slot[slot] = recs[0]

        for i, meal in enumerate(recs):
            diff = meal["calories_slot"] - target_cal
            diff_label = f"+{diff:.0f} kcal" if diff > 5 else (f"{diff:.0f} kcal" if diff < -5 else "on target")
            diet_tag = "Veg" if meal["diet"] == "vegetarian" else "Non-veg"

            with st.expander(f"{'⭐ ' if i == 0 else ''}{meal['title']} · {meal['calories_slot']:.0f} kcal · {diet_tag}", expanded=(i == 0)):
                if i == 0:
                    st.markdown("<div style='display:inline-block; margin-bottom:0.75rem; background:#14221B; color:#FFFFFF; padding:0.38rem 0.8rem; border-radius:999px; font-size:0.78rem; font-weight:800;'>Best fit for this slot</div>", unsafe_allow_html=True)

                c1, c2 = st.columns([1, 1])

                with c1:
                    st.markdown(f"""
                    <div style='padding:0.3rem 0.2rem 0.1rem 0.2rem;'>
                        <div style='font-size:0.95rem; font-weight:800; color:#22392F; margin-bottom:0.55rem;'>Nutrition snapshot</div>
                        <div style='display:flex; flex-wrap:wrap; gap:0.45rem;'>
                            <span class='sd-pill'>🔥 {meal['calories_slot']:.0f} kcal</span>
                            <span class='sd-pill'>💪 {meal['protein_slot']:.1f}g protein</span>
                            <span class='sd-pill'>🌾 {meal['carbs_slot']:.1f}g carbs</span>
                            <span class='sd-pill'>🧈 {meal['fat_slot']:.1f}g fat</span>
                            <span class='sd-pill'>🧂 {meal['sodium_slot_mg']:.0f} mg sodium</span>
                            <span class='sd-pill'>🥄 {meal['slot_portion_g']:.0f} g portion</span>
                        </div>
                        <div style='margin-top:0.7rem; color:#66756E; font-size:0.9rem;'>Meal vs target: <strong style='color:#22392F;'>{diff_label}</strong></div>
                    </div>
                    """, unsafe_allow_html=True)

                with c2:
                    fig, ax = plt.subplots(figsize=(4.1, 2.65))
                    fig.patch.set_facecolor("#FFFFFF")
                    ax.set_facecolor("#FFFFFF")

                    bar_labels = ["Energy", "Carbs", "Fat"]
                    meal_vals = [meal["calories_slot"], meal["carbs_slot"], meal["fat_slot"]]
                    limit_vals = [target_cal, SLOT_CARB_LIMITS[condition], SLOT_FAT_LIMITS[condition]]
                    xp = np.arange(3)

                    ax.bar(xp - 0.2, meal_vals, 0.35, label="Meal", color="#1DB954", alpha=0.9)
                    ax.bar(xp + 0.2, limit_vals, 0.35, label="Target", color="#C8D3CD", alpha=0.95)
                    ax.set_xticks(xp)
                    ax.set_xticklabels(bar_labels, fontsize=8.5, color="#4D6258")
                    ax.tick_params(axis='y', labelsize=8, colors="#6A7A73")
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)
                    ax.spines["left"].set_color("#DFE8E2")
                    ax.spines["bottom"].set_color("#DFE8E2")
                    ax.legend(frameon=False, fontsize=8)
                    plt.tight_layout(pad=0.6)
                    st.pyplot(fig)
                    plt.close()

if best_per_slot:
    total_cal = sum(m["calories_slot"] for m in best_per_slot.values())
    total_prot = sum(m["protein_slot"] for m in best_per_slot.values())
    total_fat = sum(m["fat_slot"] for m in best_per_slot.values())
    total_carb = sum(m["carbs_slot"] for m in best_per_slot.values())
    total_sod = sum(m["sodium_slot_mg"] for m in best_per_slot.values())
    diff = total_cal - daily_cal

    st.markdown("""
    <div class='sd-section-head'>
        <div>
            <div class='sd-section-title'>Today's nutrition summary</div>
            <div class='sd-section-sub'>A simple summary of your daily calories and macronutrients.</div>
        </div>
        <div class='sd-badge'>Daily overview</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='sd-metric-grid'>
        <div class='sd-stat'><div class='sd-stat-icon'>🔥</div><div class='sd-stat-value'>{total_cal:.0f}</div><div class='sd-stat-label'>Total calories</div></div>
        <div class='sd-stat'><div class='sd-stat-icon'>💪</div><div class='sd-stat-value'>{total_prot:.0f}g</div><div class='sd-stat-label'>Protein</div></div>
        <div class='sd-stat'><div class='sd-stat-icon'>🧈</div><div class='sd-stat-value'>{total_fat:.0f}g</div><div class='sd-stat-label'>Fat</div></div>
        <div class='sd-stat'><div class='sd-stat-icon'>🌾</div><div class='sd-stat-value'>{total_carb:.0f}g</div><div class='sd-stat-label'>Carbohydrates</div></div>
        <div class='sd-stat'><div class='sd-stat-icon'>🧂</div><div class='sd-stat-value'>{total_sod:.0f}mg</div><div class='sd-stat-label'>Sodium</div></div>
    </div>
    """, unsafe_allow_html=True)

    if abs(diff) <= 100:
        st.markdown(f"""
        <div class='sd-alert' style='background:#ECF8F0; border-left-color:#1DB954; color:#1F5B34;'>
            <strong>You're on track.</strong> Your plan totals <strong>{total_cal:.0f} kcal</strong>, which is close to your target of <strong>{daily_cal} kcal</strong>.
        </div>
        """, unsafe_allow_html=True)
    else:
        direction = "above" if diff > 0 else "below"
        st.markdown(f"""
        <div class='sd-alert' style='background:#FFF8E8; border-left-color:#FFB020; color:#8A4B00;'>
            <strong>Adjustment suggested.</strong> Your plan is <strong>{abs(diff):.0f} kcal {direction}</strong> your current target of <strong>{daily_cal} kcal</strong>.
        </div>
        """, unsafe_allow_html=True)

    chart_col_1, chart_col_2 = st.columns(2)

    with chart_col_1:
        st.markdown("<div class='sd-card' style='padding:1rem 1rem 0.35rem 1rem;'><div class='sd-card-title' style='font-size:1.05rem;'>Nutrition balance</div></div>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4.3, 3.6))
        fig.patch.set_facecolor("#FFFFFF")

        macro_vals = [total_prot * 4, total_fat * 9, total_carb * 4]
        macro_labels = [f"Protein\\n{total_prot:.0f}g", f"Fat\\n{total_fat:.0f}g", f"Carbs\\n{total_carb:.0f}g"]
        wedges, texts, autotexts = ax.pie(
            macro_vals,
            labels=macro_labels,
            autopct="%1.0f%%",
            startangle=90,
            colors=["#1DB954", "#FF9F1C", "#2D7DF6"],
            wedgeprops=dict(edgecolor="white", linewidth=2)
        )
        for t in autotexts:
            t.set_fontsize(9)
            t.set_color("white")
            t.set_fontweight("bold")

        plt.tight_layout(pad=0.65)
        st.pyplot(fig)
        plt.close()

    with chart_col_2:
        st.markdown("<div class='sd-card' style='padding:1rem 1rem 0.35rem 1rem;'><div class='sd-card-title' style='font-size:1.05rem;'>Meal vs target comparison</div></div>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4.3, 3.6))
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        snames = list(best_per_slot.keys())
        scals = [best_per_slot[s]["calories_slot"] for s in snames]
        stargs = [int(daily_cal * SLOT_CALORIE_SPLIT[s]) for s in snames]
        xp = np.arange(len(snames))
        friendly_names = ["Breakfast", "Lunch", "Snack", "Dinner"][:len(snames)]

        ax.bar(xp - 0.2, scals, 0.35, label="Meal", color="#1DB954", alpha=0.9)
        ax.bar(xp + 0.2, stargs, 0.35, label="Target", color="#C8D3CD", alpha=0.95)
        ax.set_xticks(xp)
        ax.set_xticklabels(friendly_names, fontsize=9, color="#4D6258")
        ax.set_ylabel("Calories", fontsize=8.5, color="#6A7A73")
        ax.tick_params(axis='y', labelsize=8, colors="#6A7A73")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#DFE8E2")
        ax.spines["bottom"].set_color("#DFE8E2")
        ax.legend(frameon=False, fontsize=8)
        plt.tight_layout(pad=0.65)
        st.pyplot(fig)
        plt.close()

tips = CONDITION_TIPS.get(condition, CONDITION_TIPS["healthy"])

tips_html = "".join(
    f"""
    <div class='sd-tip'>
        <div style='font-size:1.25rem;'>{icon}</div>
        <div>{tip}</div>
    </div>
    """
    for icon, tip in tips
)

st.markdown(f"""
<div class='sd-section-head'>
    <div>
        <div class='sd-section-title'>Diet tips</div>
        <div class='sd-section-sub'>Simple guidance based on the selected health condition.</div>
    </div>
    <div class='sd-badge'>Helpful tips</div>
</div>

<div class='sd-card sd-tips'>
    {tips_html}
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='sd-footer-note'>
    SmartDiet is a meal guidance tool and should not replace advice from a qualified doctor or dietitian.
</div>
""", unsafe_allow_html=True)