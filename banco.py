from cuenta import CuentaBancaria

class Banco:
    def __init__(self, nombre="Mi Banco"):
        self.nombre = nombre
        self.__cuentas = {}

    def crear_cuenta(self, numero, titular, saldo_inicial=0):
        if numero in self.__cuentas:
            raise ValueError(f"Ya existe una cuenta con el número {numero}.")
        if not titular.strip():
            raise ValueError("El nombre del titular no puede estar vacío.")
        cuenta = CuentaBancaria(numero, titular, saldo_inicial)
        self.__cuentas[numero] = cuenta
        return cuenta

    def buscar_cuenta(self, numero):
        cuenta = self.__cuentas.get(numero)
        if not cuenta:
            raise KeyError(f"No se encontró la cuenta número {numero}.")
        return cuenta

    def listar_cuentas(self):
        return list(self.__cuentas.values())

    def total_cuentas(self):
        return len(self.__cuentas)
