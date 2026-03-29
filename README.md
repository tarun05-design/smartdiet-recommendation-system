# 🍎 SmartDiet — Your Personal Meal Guide

SmartDiet helps you find the right meals for your health situation.
Whether you're managing diabetes, high blood pressure, weight, or just want to eat better —
SmartDiet suggests real, authentic regional meals that match your daily calorie goal,
split across breakfast, lunch, snack, and dinner.

No confusing charts. No medical jargon. Just friendly, practical meal ideas — every day.

---

## What does SmartDiet do?

You tell SmartDiet your name, age, height, weight, and health situation.
It then:

1. Calculates your ideal daily calorie goal based on your health condition
2. Suggests 3 meal options for each part of your day — breakfast, lunch, snack, and dinner
3. Shows you what's in each meal in plain terms — energy, protein, carbs, fat, and salt
4. Gives you simple food tips that are specific to your health situation

All 214 meals in the app are authentic regional dishes with nutritional values calculated
using the Indian Food Composition Tables (IFCT 2017) — a trusted government database.

---

## Who is this for?

- People managing **diabetes** who want to keep their blood sugar steady
- People with **high blood pressure** who need to watch their salt intake
- People working on **weight management** who want satisfying, lower-calorie meals
- Anyone who simply wants to **eat healthier** with guidance

---

## How to use the app

### Step 1 — Fill in your details (left panel)

- Enter your **name** (optional, just makes it friendlier)
- Set your **age** using the slider
- Enter your **height** in centimetres and **weight** in kilograms
- The app will automatically show your fitness level

### Step 2 — Choose your health situation

Pick the option that best describes you:

| Option | Means |
|--------|-------|
| I'm Healthy | You're in good health and want to eat balanced |
| Managing Diabetes | You have pre-diabetes, type 1, or type 2 diabetes |
| Managing Blood Pressure | You have high blood pressure (hypertension) |
| Managing My Weight | You want to lose weight gradually and healthily |

### Step 3 — Select what you eat

Choose whether you prefer:
- **Only Vegetarian** — no meat or eggs
- **Non-Vegetarian** — includes meat, fish, and eggs
- **Both are fine** — you eat everything

### Step 4 — Click "Show My Meal Plan"

That's it! Your personalised meal plan will appear on the right side of the screen.

---

## Understanding your results

### Your Health Assessment

After you click the button, you'll see a coloured card that shows your health profile.
It includes a confidence bar — this tells you how sure the app is about its recommendation.
A higher number (like 90%) means the suggestion is very well matched to your profile.

### Your Meal Plan

Your meals are spread across the day like this:

| Meal | Share of your daily goal |
|------|--------------------------|
| Breakfast | 25% of your daily calories |
| Lunch | 35% of your daily calories |
| Snack | 10% of your daily calories |
| Dinner | 30% of your daily calories |

Each slot shows 3 options. The one marked **✅ Best match for you** is the most suitable
based on your condition. Click any meal to expand it and see the full nutritional breakdown.

### What the nutrients mean

| Label | What it means in simple terms |
|-------|-------------------------------|
| 🔥 Energy (kcal) | How much fuel this meal gives your body |
| 💪 Protein | Helps build and repair muscles — especially important for weight management |
| 🌾 Carbs | Your body's main energy source — high in rice-based meals |
| 🧈 Fat | Needed in small amounts for health — too much leads to weight gain |
| 🧂 Salt (sodium) | High amounts can raise blood pressure — watch this if you have hypertension |

### Today's Nutrition at a Glance

At the bottom, you'll see a summary of everything your four meals add up to.
If you're close to your daily goal, you'll see a green "You're on track!" message.
If you're a little over or under, you'll get a gentle suggestion to swap one meal.

### Your food tips

At the very bottom, you'll find 4 simple, practical tips for your health situation.
These are written in plain language — no medical terms — and are easy to follow every day.

---

## How to install and run SmartDiet

### What you need

- A computer with Python installed (version 3.8 or newer)
- Internet connection (only needed for the first setup)

### Step 1 — Download the project files

Download the SmartDiet folder and make sure it looks like this:

```
smartdiet/
├── app.py
├── requirements.txt
├── README.md
└── model/
    ├── rf_model.pkl
    ├── gb_model.pkl
    ├── scaler.pkl
    ├── le_target.pkl
    ├── le_diet.pkl
    ├── le_meal.pkl
    ├── le_dish.pkl
    ├── meals_extended_labelled.csv
    └── meta.json
```

### Step 2 — Open Terminal or Command Prompt

On **Windows**: Press `Win + R`, type `cmd`, press Enter
On **Mac**: Press `Cmd + Space`, type `Terminal`, press Enter

Navigate to your SmartDiet folder:
```
cd path/to/your/smartdiet
```

### Step 3 — Install the required libraries

Run this command once:
```
pip install -r requirements.txt
```

This will automatically install everything the app needs.

### Step 4 — Run the app

```
streamlit run app.py
```

Your browser will open automatically and you'll see the SmartDiet app.
If it doesn't open, go to: **http://localhost:8501**

### Step 5 — Use the app

Fill in your details on the left, and click **Show My Meal Plan**. That's it!

---

## List of libraries the app uses

| Library | What it does |
|---------|-------------|
| streamlit | Creates the web interface you see in your browser |
| scikit-learn | Powers the health assessment recommendation engine |
| pandas | Reads and manages the meal database |
| numpy | Does the number calculations behind the scenes |
| matplotlib | Draws the charts and nutrition graphs |
| joblib | Loads the trained recommendation model |

To install all of them at once, just run:
```
pip install streamlit scikit-learn pandas numpy matplotlib joblib
```

---

## Frequently asked questions

**Is this a medical app?**
No. SmartDiet is a meal guidance tool designed to help you make healthier food choices.
It is not a substitute for medical advice. Always consult your doctor or a registered
dietitian before making major changes to your diet, especially if you have a health condition.

**Can I use this every day?**
Yes! You can open the app every day and get a fresh set of meal suggestions.

**What if I don't see meals I like?**
Try switching your diet preference to "Both are fine" — this opens up more options.
We're continually working to add more meal variety.

**Why does the app sometimes adjust my condition?**
If you say you're healthy but your BMI suggests otherwise, the app gently adjusts
your meal plan to better support your actual health situation. This is done to give
you the most helpful recommendations possible.

**Can I share this with my family?**
Absolutely! Each family member can enter their own details and get a personalised plan.

---

## Credits

- Nutritional data from the **Indian Food Composition Tables (IFCT) 2017**
  published by the National Institute of Nutrition, Hyderabad
- Built with Streamlit, scikit-learn, and a lot of care 🍎

---

*SmartDiet is an academic project. It is not a certified medical product.*
