import streamlit as st
import json
from datetime import date

# -------------------------------
# IMPORT ML MODEL
# -------------------------------
try:
    from model import predict_category_ml
except:
    predict_category_ml = None

# -------------------------------
# RULE-BASED FALLBACK
# -------------------------------
def predict_category(description):
    description = description.lower()

    if any(x in description for x in ["food", "dosa", "idly", "pizza", "burger"]):
        return "Food"
    elif any(x in description for x in ["milk", "eggs", "vegetables", "rice"]):
        return "Groceries"
    elif any(x in description for x in ["bus", "uber", "train", "petrol"]):
        return "Travel"
    else:
        return "Other"

# -------------------------------
# FINAL PREDICTION
# -------------------------------
def final_prediction(description):
    try:
        if predict_category_ml:
            return predict_category_ml(description)
        else:
            return predict_category(description)
    except:
        return predict_category(description)

# -------------------------------
# DATA HANDLING
# -------------------------------
def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

expenses = load_data()

# -------------------------------
# CALCULATIONS
# -------------------------------
def calculate_total(expenses):
    return sum(e["amount"] for e in expenses)

def category_summary(expenses):
    summary = {}
    for e in expenses:
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]
    return summary

# -------------------------------
# UI
# -------------------------------
st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

st.title("💰 Smart Expense Tracker")

# -------------------------------
# ADD EXPENSE
# -------------------------------
st.subheader("Add Expense")

amount = st.number_input("Enter amount", min_value=0)
description = st.text_input("Enter description")
selected_date = st.date_input("Select date", value=date.today())

predicted_category = final_prediction(description) if description else ""

if description:
    st.info(f"Predicted Category: {predicted_category}")

    categories = ["Food", "Groceries", "Travel", "Shopping", "Other"]

    corrected_category = st.selectbox(
        "Correct Category (if needed):",
        categories,
        index=categories.index(predicted_category) if predicted_category in categories else 0
    )

if st.button("Add Expense"):
    if amount > 0 and description:

        expenses.append({
            "amount": amount,
            "category": corrected_category,
            "description": description,
            "date": str(selected_date)
        })

        save_data(expenses)
        st.success("Expense Added!")
        st.rerun()

# -------------------------------
# DASHBOARD
# -------------------------------
st.subheader("Dashboard")

total = calculate_total(expenses)
summary = category_summary(expenses)

today = str(date.today())
today_total = sum(e["amount"] for e in expenses if e["date"] == today)

top_category = max(summary, key=summary.get) if summary else "None"

# SMART CARDS
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total", f"₹{total}")
col2.metric("Today", f"₹{today_total}")
col3.metric("🏆 Top Category", top_category)
col4.metric("Entries", len(expenses))

# -------------------------------
# SMART INSIGHTS
# -------------------------------
st.subheader("Smart Insights")

if summary:
    max_cat = max(summary, key=summary.get)

    if max_cat == "Food":
        st.warning("High spending on Food. Try reducing outside eating.")
    elif max_cat == "Travel":
        st.warning("Travel cost is high. Consider optimizing routes.")
    elif max_cat == "Shopping":
        st.warning("Shopping is high. Avoid unnecessary purchases.")
    else:
        st.success("Spending looks balanced. Good job!")

# -------------------------------
# CATEGORY BREAKDOWN
# -------------------------------
st.subheader("📁 Category Breakdown")

if summary:
    for cat, amt in summary.items():
        st.write(f"{cat} → ₹{amt}")
else:
    st.info("No data yet")

# -------------------------------
# TABLE
# -------------------------------
st.subheader("📋 All Expenses")

st.dataframe(expenses)

# -------------------------------
# RESET
# -------------------------------
if st.button("🗑 Clear All Data"):
    save_data([])
    st.success("Data Cleared!")
    st.rerun()