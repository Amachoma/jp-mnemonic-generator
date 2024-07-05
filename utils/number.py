def to_number(value):
    try:
        return int(value)
    except ValueError:
        return float(value)
