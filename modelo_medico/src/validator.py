"""
Módulo de validación de datos.
Valida que los datos de entrada cumplan con los requisitos esperados.
"""


class DataValidator:
    """Valida los datos de entrada del paciente"""

    # Rangos válidos para cada variable
    RANGOS_VALIDOS = {"edad": (0, 150), "fiebre": (35, 45), "dolor": (0, 10)}

    def __init__(self):
        self.errores = []

    def validar(self, datos):
        """
        Valida que los datos cumplan con los requisitos.

        Args:
            datos (dict): Diccionario con edad, fiebre y dolor

        Returns:
            dict: {"valido": bool, "mensaje": str}
        """
        self.errores = []

        for campo, (min_val, max_val) in self.RANGOS_VALIDOS.items():
            if campo not in datos:
                self.errores.append(f"Campo requerido: {campo}")
                continue

            valor = datos[campo]

            # Validar tipo
            if not isinstance(valor, (int, float)):
                self.errores.append(f"{campo} debe ser un número")
                continue

            # Validar rango
            if not (min_val <= valor <= max_val):
                self.errores.append(
                    f"{campo} debe estar entre {min_val} y {max_val}, recibido: {valor}"
                )

        if self.errores:
            return {"valido": False, "mensaje": "; ".join(self.errores)}

        return {"valido": True, "mensaje": "Datos válidos"}
