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

def ejecutar_simulacion(num_procesos, intervalo, RAM_size=100, CPU_capacity=2, instrucciones_por_ciclo=3):
    """Ejecuta la simulacion con los parametros especificados."""
    global tiempos_totales
    tiempos_totales = []

    env = simpy.Environment()
    RAM = simpy.Container(env, init=RAM_size, capacity=RAM_size)
    CPU = simpy.Resource(env, capacity=CPU_capacity)

    env.process(generar_procesos(env, RAM, CPU, intervalo, num_procesos))
    env.run()

    # Calcular estadísticas
    promedio = statistics.mean(tiempos_totales) if tiempos_totales else 0
    desviacion = statistics.stdev(tiempos_totales) if len(tiempos_totales) > 1 else 0
    return promedio, desviacion
    
def graficar_resultados(cantidades, resultados):
    """Genera una grafica de numero de procesos vs tiempo promedio."""
    tiempos_promedio = [r[0] for r in resultados]
    desviaciones = [r[1] for r in resultados]

    plt.errorbar(cantidades, tiempos_promedio, yerr=desviaciones, fmt='o-', capsize=5)
    plt.xlabel("Numero de procesos")
    plt.ylabel("Tiempo promedio en el sistema")
    plt.title("Numero de procesos vs. Tiempo promedio")
    plt.grid(True)
    plt.show()

# Ejecutar la simulación con configuración inicial (RAM = 100, CPU = 1 núcleo, 3 instrucciones por ciclo)
cantidades = [25, 50, 100, 150, 200]
intervalo = 10

resultados = []
for num_procesos in cantidades:
    promedio, desviacion = ejecutar_simulacion(num_procesos, intervalo)
    resultados.append((promedio, desviacion))
    print(f"Procesos: {num_procesos}, Tiempo promedio: {promedio:.2f}, Desviacion estandar: {desviacion:.2f}")

graficar_resultados(cantidades, resultados)
