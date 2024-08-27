def to_came_case(name: str) -> str:
    return "".join([word.title() for word in name.split("_")])+"s"
