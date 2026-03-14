class Cliente:
    def __init__(self, nombre, identificacion, email="", telefono=""):
        self.nombre = nombre
        self.identificacion = identificacion
        self.email = email
        self.telefono = telefono
        self.cuentas = []

    def agregar_cuenta(self, numero_cuenta):
        if numero_cuenta not in self.cuentas:
            self.cuentas.append(numero_cuenta)

    def mostrar_info(self):
        return (
            f"Cliente: {self.nombre}\n"
            f"ID: {self.identificacion}\n"
            f"Email: {self.email}\n"
            f"Teléfono: {self.telefono}\n"
            f"Cuentas asociadas: {len(self.cuentas)}"
        )
