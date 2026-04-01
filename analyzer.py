def calculate_total(expenses):
    return sum(e["amount"] for e in expenses)


def category_summary(expenses):
    summary = {}
    for e in expenses:
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]
    return summary


def detect_anomalies(expenses):
    if len(expenses) < 3:
        return []

    amounts = [e["amount"] for e in expenses]
    avg = sum(amounts) / len(amounts)

    anomalies = []
    for e in expenses:
        if e["amount"] > avg * 2:
            anomalies.append(e)

    return anomalies