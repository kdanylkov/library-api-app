

def operations(a: int, b: int, c: str) -> int | float | str:
    if c == '+':
        return a + b
    elif c == '-':
        return a - b
    elif c == '*':
        return a * b
    elif c == '/':
        return a / b
    else:
        return 'Operation unknown'

