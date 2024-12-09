def remove_none_fields(data: dict):
    data = {key: value for key, value in data.items() if value not in ["", None]}
    return data
