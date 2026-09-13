def calculate_price_change(price_history):
    if len(price_history) < 2:
        return None

    previous_price = float(price_history[-2]["price"])
    current_price = float(price_history[-1]["price"])

    change = current_price - previous_price
    if previous_price == 0:
        percentage_change = None
    else:
        percentage_change = (change / previous_price) * 100

    return {
        "previous_price": previous_price,
        "current_price": current_price,
        "change": change,
        "percentage_change": percentage_change,
    }
