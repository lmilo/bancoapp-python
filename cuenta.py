from datetime import datetime

class CuentaBancaria:
    def __init__(self, numero_cuenta, titular, saldo_inicial=0):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.__saldo = saldo_inicial
        self.__historial = []
        if saldo_inicial > 0:
            self.__historial.append(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Saldo inicial: +${saldo_inicial:,.2f}"
            )

    def __validar_monto(self, monto):
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto debe ser un número.")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        return True

    def depositar(self, monto):
        self.__validar_monto(monto)
        self.__saldo += monto
        registro = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Depósito: +${monto:,.2f} | Saldo: ${self.__saldo:,.2f}"
        self.__historial.append(registro)
        return True

    def retirar(self, monto):
        self.__validar_monto(monto)
        if monto > self.__saldo:
            raise ValueError(f"Fondos insuficientes. Saldo disponible: ${self.__saldo:,.2f}")
        self.__saldo -= monto
        registro = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Retiro: -${monto:,.2f} | Saldo: ${self.__saldo:,.2f}"
        self.__historial.append(registro)
        return True

    def consultar_saldo(self):
        return self.__saldo

    def obtener_historial(self):
        return list(self.__historial)

    def mostrar_info(self):
        return (
            f"Cuenta: {self.numero_cuenta}\n"
            f"Titular: {self.titular}\n"
            f"Saldo: ${self.__saldo:,.2f}"
        )
