import random
import simpy

class TaskProcess:
    """
    Representa la simulacion
    Cada proceso solicita memoria, ejecuta instrucciones en el CPU y finaliza.
    """

    def __init__(self, env, pid, instructions, memory_manager, cpu):
        """
        Comienza un nuevo sistma
        :env: Entorno de SimPy.
        :pid: Identificador del proceso.
        :parinstructions: Total de instrucciones a ejecutar.
        :memory_manager: Administrador de memoria.
        :cpu: Recurso del CPU.
        """
        self.env = env
        self.pid = pid
        self.instructions = instructions
        self.memory_manager = memory_manager
        self.cpu = cpu
        self.memory_needed = random.randint(1, 10)  # Memoria aleatoria entre 1 y 10 unidades
        self.action = env.process(self.run())

    def run(self):
        """
        Ciclo: solicitar memoria, ejecutar instrucciones y liberar memoria.
        """
        yield self.env.process(self.request_memory())
        yield self.env.process(self.execute())
        yield self.env.process(self.release_memory())

    def request_memory(self):
        """ Solicita memoria al administrador antes de ejecutarse. """
        print(f"[{self.env.now}] Proceso {self.pid} solicitando {self.memory_needed} unidades de memoria.")
        yield self.memory_manager.request_memory(self.memory_needed)

    def execute(self):
        """ Ejecuta instrucciones en bloques de 3 hasta finalizar. """
        while self.instructions > 0:
            with self.cpu.request() as req:
                yield req
                execute_count = min(self.instructions, 3)
                self.instructions -= execute_count
                print(f"[{self.env.now}] Proceso {self.pid} ejecutando {execute_count} instrucciones. Restantes: {self.instructions}")
                yield self.env.timeout(1)

    def release_memory(self):
        """ Libera la memoria al terminar. """
        print(f"[{self.env.now}] Proceso {self.pid} finalizado. Liberando {self.memory_needed} unidades de memoria.")
        yield self.memory_manager.release_memory(self.memory_needed)