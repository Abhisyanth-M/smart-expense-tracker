import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
import plotly.express as px

# -------------------------------
# DATABASE
# -------------------------------
conn = sqlite3.connect("expenses.db", check_same_thread=False)
c = conn.cursor()

# USERS TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# EXPENSES TABLE (USER LINKED)
c.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    amount REAL,
    category TEXT,
    description TEXT,
    date TEXT
)
""")

conn.commit()

# -------------------------------
# SESSION
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -------------------------------
# AUTH FUNCTIONS
# -------------------------------
def create_user(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone()

# -------------------------------
# ML CATEGORY
# -------------------------------
def predict_category(text):
    text = text.lower()

    keywords = {
        "Food": ["idli", "idly", "dosa", "food", "hotel", "meal", "biryani", "chapati", "breakfast", "lunch", "dinner", "roti", "naan", "pizza", "burger", "sandwich"],
        "Travel": ["uber", "bus", "train", "petrol", "flight"],
        "Bills": ["rent", "electricity", "bill", "wifi"],
        "Shopping": ["shirt", "clothes", "amazon", "flipkart"],
        "Groceries": ["milk", "vegetables", "rice", "dal", "eggs"],
        "Entertainment": ["movie", "netflix", "spotify"]
    }

    for category, words in keywords.items():
        if any(word in text for word in words):
            return category

    return "Other"

# -------------------------------
# DB FUNCTIONS
# -------------------------------
def add_expense(user, amount, category, description, date):
    c.execute("INSERT INTO expenses (user, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
              (user, amount, category, description, date))
    conn.commit()

def get_data(user):
    return pd.read_sql("SELECT * FROM expenses WHERE user=?", conn, params=(user,))

def delete_expense(expense_id):
    c.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()

def update_expense(expense_id, amount, description):
    category = predict_category(description)
    c.execute("""
        UPDATE expenses 
        SET amount=?, description=?, category=? 
        WHERE id=?
    """, (amount, description, category, expense_id))
    conn.commit()

def clear_all(user):
    c.execute("DELETE FROM expenses WHERE user=?", (user,))
    conn.commit()

# -------------------------------
# LOGIN UI
# -------------------------------
if not st.session_state.logged_in:

    st.title("🔐 Smart Expense Tracker Login")

    menu = st.radio("Select", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Signup":
        if st.button("Create Account"):
            if create_user(username, password):
                st.success("Account created! Now login.")
            else:
                st.error("Username already exists")

    if menu == "Login":
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# -------------------------------
# MAIN APP
# -------------------------------
st.title("💰 Smart Expense Tracker")

# LOGOUT
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

menu = st.sidebar.radio("Navigation", ["Add Expense", "Dashboard"])

user = st.session_state.username

# -------------------------------
# ADD EXPENSE
# -------------------------------
if menu == "Add Expense":
    st.header("Add Expense")

    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description")
    selected_date = st.date_input("Date", value=date.today())

    if description:
        predicted = predict_category(description)
        st.success(f"Auto Category: {predicted}")
    else:
        predicted = "Other"

    if st.button("Add Expense"):
        add_expense(user, amount, predicted, description, str(selected_date))
        st.success("Expense Added!")

# -------------------------------
# DASHBOARD
# -------------------------------
if menu == "Dashboard":
    st.header("Dashboard")

    df = get_data(user)

    if df.empty:
        st.warning("No data available")
    else:
        df["date"] = pd.to_datetime(df["date"]).dt.date

        # METRICS
        total = df["amount"].sum()
        today = df[df["date"] == date.today()]["amount"].sum()
        entries = len(df)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total", f"₹{total}")
        col2.metric("Today", f"₹{today}")
        col3.metric("Entries", entries)

        # GRAPH
        st.subheader("Monthly Spending")
        df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
        monthly = df.groupby("month")["amount"].sum().reset_index()

        fig = px.bar(monthly, x="month", y="amount")
        st.plotly_chart(fig, use_container_width=True)

        # CATEGORY
        st.subheader("📂 Category Breakdown")
        summary = df.groupby("category")["amount"].sum()

        for cat, amt in summary.items():
            st.write(f"{cat} → ₹{amt}")

        # EDIT + DELETE
        st.subheader("Manage Expenses")

        for i, row in df.iterrows():
            with st.expander(f"{row['description']} - ₹{row['amount']} ({row['date']})"):

                new_amount = st.number_input("Edit Amount", value=row["amount"], key=f"a{row['id']}")
                new_desc = st.text_input("Edit Description", value=row["description"], key=f"d{row['id']}")

                col1, col2 = st.columns(2)

                if col1.button("Update", key=f"u{row['id']}"):
                    update_expense(row["id"], new_amount, new_desc)
                    st.success("Updated!")
                    st.rerun()

                if col2.button("Delete", key=f"x{row['id']}"):
                    delete_expense(row["id"])
                    st.warning("Deleted!")
                    st.rerun()

        # RESET
        st.subheader("Reset")
        if st.button("Clear All Data"):
            clear_all(user)
            st.success("All data cleared!")
            st.rerun()
