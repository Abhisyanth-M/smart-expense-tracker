import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# ------------------ DATASET ------------------
data = {
    "text": [
        # FOOD
        "pizza", "burger", "hotel food", "restaurant",
        "idly", "dosa", "masala dosa", "butter masala dosa",
        "meal", "biryani", "chapati", "south indian food","roti","methi roti","butter roti","butter naan",

        # TRAVEL
        "bus ticket", "uber ride", "train ticket", "auto fare",
        "petrol", "diesel", "flight ticket",

        # CLOTHES
        "shirt", "jeans", "t shirt", "pants", "clothes shopping",

        # GROCERIES
        "milk", "vegetables", "grocery items", "rice", "dal","eggs","fruits",

        # SPORTS
        "football", "cricket kit", "ball", "sports shoes","badminton racket","tennis bat","volleyball","throwball","sports drinks",

        # SHOPPING
        "amazon order", "online shopping", "flipkart order","mall shopping","meesho order","myntra super sales order"
    ],
    "category": [
        # FOOD
        "Food","Food","Food","Food",
        "Food","Food","Food","Food",
        "Food","Food","Food","Food","Food","Food","Food","Food",

        # TRAVEL
        "Travel","Travel","Travel","Travel",
        "Travel","Travel","Travel",

        # CLOTHES
        "Clothes","Clothes","Clothes","Clothes","Clothes",

        # GROCERIES
        "Groceries","Groceries","Groceries","Groceries","Groceries","Groceries","Groceries",

        # SPORTS
        "Sports items","Sports items","Sports items","Sports items","Sports items","Sports items","Sports items","Sports items","Sports items",

        # SHOPPING
        "Shopping","Shopping","Shopping","Shopping","Shopping","Shopping"
    ]
}
# Convert to DataFrame
df = pd.DataFrame(data)

# Features & Labels
X = df["text"]
y = df["category"]

# Vectorization
vectorizer = TfidfVectorizer(ngram_range=(1,2))
X_vec = vectorizer.fit_transform(X)

# Model
model = LogisticRegression()
model.fit(X_vec, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model trained and saved!")