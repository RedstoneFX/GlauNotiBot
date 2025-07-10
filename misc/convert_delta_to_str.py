def convert_delta_to_str(deltaTime: float | int):
    minutes = round(deltaTime // 60 % 60)
    hours = round(deltaTime // 3600 % 24)
    days = round(deltaTime // 3600 // 24)
    if days != 0:
        delta_str = f"{days} дней {hours} часов и {minutes} минут"
    elif hours != 0:
        delta_str = f"{hours} часов и {minutes} минут"
    else:
        delta_str = f"{minutes} минут"
    return delta_str