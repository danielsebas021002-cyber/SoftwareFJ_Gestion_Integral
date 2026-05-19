import logging
from abc import ABC, abstractmethod

# Configuración de Logs exigida por la guía
logging.basicConfig(
    filename='eventos_sistema.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 1. EXCEPCIONES PERSONALIZADAS Y ENCADENAMIENTO
class SoftwareFJError(Exception):
    """Excepción personalizada base"""
    pass

class ErrorValidacion(SoftwareFJError):
    """Error para datos inválidos"""
    pass

class ErrorReserva(SoftwareFJError):
    """Error para operaciones de reserva no permitidas"""
    pass


# 2. CLASE ABSTRACTA GENERAL (Entidad del sistema)
class EntidadSistema(ABC):
    @abstractmethod
    def obtener_descripcion(self):
        pass


# 3. CLASE CLIENTE (Con encapsulación estricta)
class Cliente(EntidadSistema):
    def __init__(self, id_cliente, nombre):
        if not id_cliente or not nombre:
            raise ErrorValidacion("ID y Nombre son obligatorios")
        self.__id = id_cliente  # Atributo privado
        self.__nombre = nombre  # Atributo privado

    @property
    def id_cliente(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    def obtener_descripcion(self):
        return f"Cliente: {self.__nombre} (ID: {self.__id})"


# 4. CLASE ABSTRACTA SERVICIO
class Servicio(EntidadSistema, ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, cantidad, **kwargs):
        pass

    def obtener_descripcion(self):
        return f"Servicio: {self.nombre} - Costo Base: ${self.costo_base}"


# 5. CLASES DERIVADAS (Polimorfismo y Sobrecarga)
class AlquilerEquipos(Servicio):
    def calcular_costo(self, horas, **kwargs):
        # Sobrecarga mediante parámetros opcionales (kwargs)
        seguro = kwargs.get('seguro', 0)
        return (self.costo_base * horas) + seguro

class ReservaSalas(Servicio):
    def calcular_costo(self, dias, **kwargs):
        descuento = kwargs.get('descuento', 0)
        return (self.costo_base * dias) - descuento

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, sesiones, **kwargs):
        total = self.costo_base * sesiones
        # Impuesto opcional por mantenimiento de plataforma
        iva = kwargs.get('iva', False)
        if iva:
            total *= 1.19
        return total * 0.9 if sesiones > 3 else total


# 6. CLASE RESERVA (Obligatoria según la guía)
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if duracion <= 0:
            try:
                raise ValueError("La duración debe ser mayor a cero.")
            except ValueError as e:
                # Encadenamiento de excepciones exigido por la guía
                raise ErrorReserva("No se pudo procesar la reserva debido a parámetros inválidos.") from e
        
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def procesar_reserva(self, **kwargs):
        self.estado = "Confirmada"
        return self.servicio.calcular_costo(self.duracion, **kwargs)

    def cancelar_reserva(self):
        self.estado = "Cancelada"
