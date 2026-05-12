import logging
from abc import ABC, abstractmethod

# Configuración de Logs exigida por la guía [cite: 13, 18, 31]
logging.basicConfig(
    filename='eventos_sistema.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SoftwareFJError(Exception):
    """Excepción personalizada base [cite: 17]"""
    pass

class ErrorValidacion(SoftwareFJError):
    """Error para datos inválidos [cite: 19]"""
    pass

class Cliente:
    def __init__(self, id_cliente, nombre):
        if not id_cliente or not nombre:
            raise ErrorValidacion("ID y Nombre son obligatorios")
        self.__id = id_cliente # Encapsulación [cite: 11, 22]
        self.nombre = nombre

    def obtener_id(self):
        return self.__id

class Servicio(ABC): # Abstracción [cite: 11, 23]
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, cantidad):
        pass

class AlquilerEquipos(Servicio): # Herencia [cite: 24]
    def calcular_costo(self, horas):
        return self.costo_base * horas

class ReservaSalas(Servicio): # Polimorfismo [cite: 24]
    def calcular_costo(self, dias):
        return self.costo_base * dias

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, sesiones):
        # Sobrecarga lógica: Descuento por volumen [cite: 26]
        total = self.costo_base * sesiones
        return total * 0.9 if sesiones > 3 else total