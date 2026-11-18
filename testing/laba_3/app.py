def get_angles(shape: str) -> list:
    if shape == "triangle":
        return [60, 60, 60]
    elif shape == "square":
        return [90, 90, 90, 90]
    elif shape == "rectangle":
        return [90, 90, 90, 90]
    else:
        return []

if __name__ == "__main__":  # pragma: no cover
    print(get_angles("triangle"))