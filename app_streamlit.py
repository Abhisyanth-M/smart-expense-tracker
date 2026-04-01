import streamlit as st
import json
import matplotlib.pyplot as plt
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

    food_items = ["food", "hotel", "idly", "dosa", "biryani", "meal", "pizza", "burger", "roti"]
    grocery_items = ["milk", "eggs", "vegetables", "rice", "dal", "oil", "fruits", "atta", "sugar"]
    clothes_items = ["shirt", "pant", "jeans", "dress"]
    travel_items = ["bus", "uber", "train", "auto", "petrol"]
    sports_items = ["bat", "ball", "football"]

    if any(word in description for word in food_items):
        return "Food"
    elif any(word in description for word in grocery_items):
        return "Groceries"
    elif any(word in description for word in clothes_items):
        return "Clothes"
    elif any(word in description for word in travel_items):
        return "Travel"
    elif any(word in description for word in sports_items):
        return "Sports items"
    else:
        return "Other"

# -------------------------------
# FINAL PREDICTION (ML + FALLBACK)
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
# LOAD / SAVE DATA
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
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("⚙️ Controls")

if st.sidebar.button("🗑 Clear All Data"):
    save_data([])
    st.sidebar.success("Data Cleared!")
    st.rerun()

# -------------------------------
# TITLE
# -------------------------------
st.title("💰 Smart Expense Tracker")

# -------------------------------
# INPUT SECTION
# -------------------------------
st.subheader("Add Expense")

amount = st.number_input("Enter amount", min_value=0)
description = st.text_input("Enter description")
selected_date = st.date_input("Select date", value=date.today())

predicted_category = final_prediction(description) if description else ""

if description:
    st.info(f"Predicted Category: {predicted_category}")

    # SELF-LEARNING CORRECTION
    categories = ["Food", "Groceries", "Clothes", "Travel", "Sports items", "Shopping", "Other"]

    corrected_category = st.selectbox(
        "Change category if wrong:",
        categories,
        index=categories.index(predicted_category) if predicted_category in categories else 0
    )

# -------------------------------
# ADD EXPENSE
# -------------------------------
if st.button("Add Expense"):
    if amount > 0 and description:

        final_category = corrected_category if description else "Other"

        new_expense = {
            "amount": amount,
            "category": final_category,
            "description": description,
            "date": str(selected_date)
        }

        expenses.append(new_expense)
        save_data(expenses)

        st.success(f"Saved as: {final_category}")
        st.rerun()
    else:
        st.warning("Please enter valid details")

# -------------------------------
# DASHBOARD
# -------------------------------
st.subheader("Dashboard")

total = calculate_total(expenses)
summary = category_summary(expenses)

col1, col2 = st.columns(2)
col1.metric("Total Expense", f"₹{total}")
col2.metric("Categories", len(summary))

# -------------------------------
# CATEGORY SUMMARY
# -------------------------------
st.write("Category Breakdown")
st.json(summary)

# -------------------------------
# GRAPH
# -------------------------------
if summary:
    st.write("Expense Distribution")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(summary.keys(), summary.values())

    plt.xticks(rotation=30)
    ax.set_title("Expense Distribution")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")

    st.pyplot(fig)
else:
    st.info("No data to display")

# -------------------------------
# TABLE
# -------------------------------
st.write("📋 All Expenses")
st.dataframe(expenses)