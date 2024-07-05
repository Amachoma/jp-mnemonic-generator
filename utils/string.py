def to_snake_case(string):
    return string.replace("-", " ").replace('(', '').replace(')', '').lower().replace(" ", "_")