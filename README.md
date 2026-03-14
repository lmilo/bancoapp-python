# BancoApp — Sistema Bancario en Python

Sistema de administración bancaria desarrollado en Python con interfaz gráfica usando **Tkinter**. Aplica principios de **Programación Orientada a Objetos** como encapsulamiento, abstracción y separación de responsabilidades.

---

## Características

- Crear cuentas bancarias con número único
- Realizar depósitos y retiros con validación de fondos
- Consultar saldo e historial de transacciones
- Listar todas las cuentas registradas
- Interfaz gráfica con navegación por sidebar
- Saldo encapsulado, solo modificable mediante métodos autorizados

---

## Estructura del Proyecto

```
proyecto_banco/
├── cuenta.py   → Clase CuentaBancaria (encapsulamiento del saldo)
├── banco.py    → Clase Banco (administración de cuentas)
├── cliente.py  → Clase Cliente (modelo de datos del cliente)
└── main.py     → Interfaz gráfica con Tkinter
```

---

## Requisitos

- Python 3.8 o superior
- Tkinter (incluido en la mayoría de instalaciones de Python)

### Instalar Tkinter en Linux

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install python3-tk

# Fedora / CentOS
sudo dnf install python3-tkinter
```

### Verificar instalación

```bash
python3 -m tkinter
```

> Debe abrirse una pequeña ventana de prueba.

---

## Ejecución

```bash
cd proyecto_banco/
python3 main.py
```

---

## Arquitectura del Código

### `cuenta.py` — `CuentaBancaria`

| Elemento | Tipo | Descripción |
|---|---|---|
| `numero_cuenta` | Atributo público | Identificador único de la cuenta |
| `titular` | Atributo público | Nombre del propietario |
| `__saldo` | Atributo privado | Saldo encapsulado |
| `__historial` | Atributo privado | Registro de transacciones |
| `depositar(monto)` | Método público | Agrega dinero al saldo |
| `retirar(monto)` | Método público | Retira dinero si hay fondos |
| `consultar_saldo()` | Método público | Retorna el saldo actual |
| `mostrar_info()` | Método público | Muestra datos de la cuenta |
| `__validar_monto(monto)` | Método privado | Valida que el monto sea numérico y positivo |

### `banco.py` — `Banco`

| Método | Descripción |
|---|---|
| `crear_cuenta(numero, titular, saldo_inicial)` | Crea una cuenta, evita números duplicados |
| `buscar_cuenta(numero)` | Retorna una cuenta por número |
| `listar_cuentas()` | Retorna todas las cuentas registradas |

### `cliente.py` — `Cliente`

Modelo de datos del cliente con atributos: `nombre`, `identificacion`, `email`, `telefono` y lista de cuentas asociadas.

### `main.py` — Interfaz Gráfica

Arquitectura de vistas independientes (`tk.Frame`) montadas dinámicamente sobre un panel principal, navegadas desde un sidebar lateral.

| Vista | Descripción |
|---|---|
| Dashboard | Resumen de cuentas y saldo total |
| Crear Cuenta | Formulario con validación |
| Depositar | Ingreso de monto con confirmación |
| Retirar | Retiro con validación de fondos |
| Consultar Saldo | Info de cuenta + historial |
| Listar Cuentas | Tabla scrollable de todas las cuentas |

---

## Principios OOP Aplicados

- **Encapsulamiento**: `__saldo` e `__historial` son privados, inaccesibles desde fuera de la clase.
- **Abstracción**: `__validar_monto()` oculta la lógica de validación al consumidor de la clase.
- **Separación de responsabilidades**: cada archivo contiene una clase con una única responsabilidad.
- **Manejo de excepciones**: `ValueError`, `TypeError` y `KeyError` se propagan desde el modelo y se capturan en la UI con `messagebox`.

---

## Paleta de Colores (UI)

| Elemento | Color |
|---|---|
| Fondo principal | `#0D1B2A` |
| Panel lateral | `#1B2A3B` |
| Tarjetas | `#1E2F42` |
| Acento principal | `#00C896` |
| Alerta / Peligro | `#E05C5C` |
| Texto principal | `#E8EDF2` |

---

## Autor

Desarrollado como taller académico de Programación Orientada a Objetos en Python.
