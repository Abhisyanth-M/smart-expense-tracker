# Smart Expense Tracker

A Machine Learning powered expense tracking web app that automatically predicts expense categories and provides spending insights through an interactive dashboard.

## Live Demo
https://huggingface.co/spaces/Abhisyanth-M/smart-expense-tracker

## Overview
Smart Expense Tracker eliminates the need to manually categorise daily expenses. Enter your expense description and amount — the ML model automatically predicts the category. Track your spending patterns through a clean dashboard with category breakdown and insights.

## Features
- Multi-user support with login system
- Add, edit and delete expenses
- Automatic expense category prediction using ML
- Spending dashboard with category breakdown
- Persistent data storage using SQLite
- Clean and simple UI

## Tech Stack
- Python
- Streamlit
- Scikit-learn
- SQLite
- Docker
- Hugging Face Spaces

## How It Works
1. User logs in or creates an account
2. User enters expense description and amount
3. ML model predicts the expense category automatically
4. Expense is saved to SQLite database
5. Dashboard updates with latest spending breakdown and insights

## Installation and Running Locally
```bash
git clone https://github.com/Abhisyanth-M/smart-expense-tracker
cd smart-expense-tracker
pip install -r requirements.txt
python -m streamlit run app.py
```

## Limitations
- Category prediction is based on keyword patterns in expense description
- Multi-user data is stored locally — not suitable for shared cloud deployment without a proper database server
- Limited to predefined expense categories

## Future Improvements
- Add monthly and weekly spending reports
- Export expenses as CSV or PDF
- Budget alerts when spending exceeds set limits
- Integration with bank transaction data

## GitHub
https://github.com/Abhisyanth-M/smart-expense-tracker
