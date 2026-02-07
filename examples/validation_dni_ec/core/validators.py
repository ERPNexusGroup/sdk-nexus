# validation_dni_ec/core/validators.py
def validate_ecuadorian_id(id_number: str) -> bool:
    """
    Valida cédula ecuatoriana según algoritmo oficial del SRI.

    Algoritmo:
    1. Los primeros 2 dígitos deben ser válidos (01-24 para provincias + 30 para ecuatorianos en el exterior)
    2. El décimo dígito es un dígito verificador calculado con coeficientes [2,1,2,1,2,1,2,1,2]
    3. Si el producto es >=10, se resta 9
    4. El verificador = (10 - (suma % 10)) % 10

    Returns:
        True si la cédula es válida, False en caso contrario
    """
    # Validar longitud
    if len(id_number) != 10:
        return False

    # Validar que sean todos dígitos
    if not id_number.isdigit():
        return False

    # Validar provincia (primeros 2 dígitos)
    province_code = int(id_number[:2])
    if province_code < 1 or (province_code > 24 and province_code != 30):
        return False

    # Coeficientes para el algoritmo de validación
    coefficients = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0

    # Calcular suma ponderada
    for i in range(9):
        digit = int(id_number[i])
        product = digit * coefficients[i]
        total += product if product < 10 else product - 9

    # Calcular dígito verificador esperado
    verifier_expected = (10 - (total % 10)) % 10
    verifier_actual = int(id_number[9])

    return verifier_expected == verifier_actual