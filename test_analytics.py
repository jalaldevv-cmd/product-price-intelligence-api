from analytics import calculate_price_change


def test_calculate_price_change():
    history = [
        {"price": 100},
        {"price": 80},
    ]

    result = calculate_price_change(history)

    assert result["previous_price"] == 100
    assert result["current_price"] == 80
    assert result["change"] == -20
    assert result["percentage_change"] == -20


def test_not_enough_price_history():
    history = [
        {"price": 100},
    ]

    result = calculate_price_change(history)

    assert result is None


def test_zero_previous_price():
    history = [
        {"price": 0},
        {"price": 50}
    ]

    result = calculate_price_change(history)

    assert result["change"] == 50
    assert result["percentage_change"] is None
