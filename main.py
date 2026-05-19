from modelo_sistema import Cliente, AlquilerEquipos, ReservaSalas, AsesoriaEspecializada, Reserva, ErrorValidacion, ErrorReserva
import logging

def ejecutar_simulacion():
    print("--- INICIANDO SOFTWARE FJ (10 OPERACIONES SIMULADAS) ---")
    
    # Instanciamos los tres tipos de servicios requeridos por la guía
    servicios = [
        AlquilerEquipos("Computador Portátil", 40000),
        ReservaSalas("Auditorio Principal", 150000),
        AsesoriaEspecializada("Soporte Técnico Especializado", 70000)
    ]

    # Simulación obligatoria de 10 operaciones con éxitos y fallos controlados
    for i in range(1, 11):
        print(f"\n>>> Prueba #{i}:")
        try:
            # Forzamos fallos específicos para demostrar el control de excepciones y logs
            if i == 4:
                # Error de validación: cliente con campos vacíos
                c = Cliente("", "")
                r = Reserva(c, servicios[0], i)
            elif i == 8:
                # Error de reserva: duración inválida (cero)
                c = Cliente(f"100{i}", f"Estudiante {i}")
                r = Reserva(c, servicios[1], 0)
            else:
                # Casos exitosos que modelan correctamente la gestión integral
                c = Cliente(f"100{i}", f"Estudiante {i}")
                s = servicios[i % 3]
                r = Reserva(c, s, i)
            
            # Procesamiento de la reserva usando parámetros opcionales para la sobrecarga
            total = r.procesar_reserva(seguro=5000, descuento=10000, iva=True)
            
        except (ErrorValidacion, ErrorReserva) as e:
            # Captura y registro robusto en Logs de los errores controlados
            print(f"CAPTURA DE ERROR: {e}")
            logging.error(f"Error controlado en prueba {i}: {e}")
            if e.__cause__:
                logging.error(f"Causa original detectada: {e.__cause__}")
                
        except Exception as e:
            # Captura preventiva de fallos críticos inesperados
            print(f"ERROR CRÍTICO INESPERADO: {e}")
            logging.critical(f"Error crítico en prueba {i}: {e}")
            
        else:
            # Bloque ELSE exigido por la guía (se ejecuta si NO hubo excepciones)
            print(f"ÉXITO: {r.cliente.nombre} reservó {r.servicio.nombre}. Estado: {r.estado}. Total: ${total}")
            logging.info(f"Operación {i} exitosa. Reserva confirmada para Cliente ID: {r.cliente.id_cliente}")
            
        finally:
            # Bloque FINALLY exigido para garantizar la estabilidad e impedir interrupciones
            print("Estado del Sistema: CONTINÚA EN EJECUCIÓN Y ESTABLE")

if __name__ == "__main__":
    ejecutar_simulacion()
