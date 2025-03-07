import simpy
import random
import statistics
import matplotlib.pyplot as plt

# Configuración inicial
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Variables globales para almacenar los tiempos de los procesos
tiempos_totales = []

def proceso(env, nombre, RAM, CPU):
    """Simula un proceso en el sistema."""
    llegada = env.now  # Momento en el que el proceso llega
    memoria_requerida = random.randint(1, 10)

    # 1. Solicitar memoria RAM
    yield RAM.get(memoria_requerida)

    # 2. Ejecutar instrucciones en el CPU
    instrucciones_pendientes = random.randint(1, 10)
    while instrucciones_pendientes > 0:
        with CPU.request() as req:
            yield req  # Esperar turno en CPU
            tiempo_cpu = min(3, instrucciones_pendientes)  # Ejecutar hasta 3 instrucciones
            yield env.timeout(1)  # Simula tiempo de ejecución
            instrucciones_pendientes -= tiempo_cpu

        # Simular posible espera en I/O
        if instrucciones_pendientes > 0 and random.randint(1, 21) == 1:
            yield env.timeout(3)  # Simula espera en I/O

    # 3. Devolver memoria y registrar el tiempo total
    RAM.put(memoria_requerida)
    tiempo_total = env.now - llegada
    tiempos_totales.append(tiempo_total)

def generar_procesos(env, RAM, CPU, intervalo, num_procesos):
    """Crea procesos en la simulacion con un tiempo de llegada exponencial."""
    for i in range(num_procesos):
        env.process(proceso(env, f"Proceso-{i+1}", RAM, CPU))
        yield env.timeout(random.expovariate(1.0 / intervalo))
