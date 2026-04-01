import matplotlib.pyplot as plt
import json

def detect_category(description):
    description = description.lower()

    if "food" in description or "pizza" in description or "hotel" in description:
        return "Food"
    elif "bus" in description or "train" in description or "uber" in description:
        return "Travel"
    elif "shirt" in description or "shoes" in description or "mall" in description:
        return "Shopping"
    elif "bat" in description or "ball" in description:
        return "Sports items"
    else:
        return "Other"

try:
    with open("data.json", "r") as file:
        expenses = json.load(file)
except:
    expenses = []

try:
    with open("data.json","r") as file:
        expenses = json.load(file)
except:
    expenses = []

while True:
    amount = int(input("Enter the amount:"))
    description = input("Enter the description:")
    category = detect_category(description)
    date = input("Enter the date (YYYY-MM-DD):")

    expenses.append({"amount": amount, 
                 "category": category, 
                 "date": date})
    
    choice = input("Do you want to add another expense? (yes/no):")
    if choice == "no" or choice == "No":
        break

total = 0

for expense in expenses:
    total += expense["amount"]

print("Total expenses:", total)

category_summary = {}
for expense in expenses:
    category = expense["category"]
    amount = expense["amount"]
    
    if category in category_summary:
        category_summary[category] += amount
    else:
        category_summary[category] = amount

max_category = None
max_amount = 0

for category, amount in category_summary.items():
    if amount > max_amount:
        max_amount = amount
        max_category = category

print("\nCategory-wise spending:")
for category, amount in category_summary.items():
    print(category,":",amount)

print(f"\nHighest spending category: {max_category} with amount: {max_amount}")

print("\nSuggestions:")

if max_category.lower() == "Food":
    print("You are spending a lot on food. Consider cooking at home more often or looking for discounts.")
elif max_category.lower() == "Travel":
    print("Your travel expenses are high. Try planning routes better.")
elif max_category.lower() == "Shopping":
    print("Your shopping expenses are high. Consider setting a budget for shopping and sticking to it.")
elif max_category.lower() == "Sports items":
    print("Your sports items expenses are high. Consider looking for sales or using items more efficiently.")
else:
    print("Your expenses are well balanced. Keep it up!")

print("\nAll Expenses:")
for e in expenses:
    print(e)
with open("data.json","w") as file:
    json.dump(expenses,file,indent=4)

print(expenses)

import matplotlib.pyplot as plt

categories = list(category_summary.keys())
amounts = list(category_summary.values())

plt.figure(figsize=(10,6))  # bigger graph

bars = plt.bar(categories, amounts)

plt.xlabel("Category", fontsize=12, color='blue')
plt.ylabel("Amount", fontsize=12, color='red')
plt.title("Expense Distribution", fontsize=16, color='purple')

# Add values on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval),
             ha='center', va='bottom')

plt.xticks(rotation=30)  # tilt labels

plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()