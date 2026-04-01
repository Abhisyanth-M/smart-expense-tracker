import pickle

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

def predict_category_ml(description):
    vec = vectorizer.transform([description])
    return model.predict(vec)[0]