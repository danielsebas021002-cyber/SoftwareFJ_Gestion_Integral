from modelo_sistema import Cliente, AlquilerEquipos, ReservaSalas, AsesoriaEspecializada, ErrorValidacion
import logging

def ejecutar_simulacion():
    print("--- INICIANDO SOFTWARE FJ (10 OPERACIONES) ---")
    servicios = [
        AlquilerEquipos("Computador", 40000),
        ReservaSalas("Auditorio", 150000),
        AsesoriaEspecializada("Soporte Técnico", 70000)
    ]
    
    # Realizamos las 10 operaciones requeridas [cite: 32]
    for i in range(1, 11):
        try:
            print(f"\n>>> Prueba #{i}:")
            if i == 7: # Simulamos un error de datos vacíos [cite: 19]
                c = Cliente("", "")
            else:
                c = Cliente(f"100{i}", f"Estudiante {i}")
                s = servicios[i % 3]
                total = s.calcular_costo(i)
                print(f"ÉXITO: {c.nombre} reservó {s.nombre} por ${total}")
                logging.info(f"Operación {i} exitosa para ID: {c.obtener_id()}")
                
        except ErrorValidacion as e: # Manejo de excepciones [cite: 17, 32]
            print(f"CAPTURA DE ERROR: {e}")
            logging.error(f"Error en prueba {i}: {e}")
        except Exception as e:
            logging.critical(f"Error crítico: {e}")
        finally:
            print("Sistema: CONTINÚA EN EJECUCIÓN") # Garantiza estabilidad [cite: 11]

if __name__ == "__main__":
    ejecutar_simulacion()