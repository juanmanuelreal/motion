def suma(a: int, b: int):
    return a + b

def dividir(a: int, b: int):
    if b == 0:
        raise ZeroDivisionError("The divisor can not be zero")
    return a / b