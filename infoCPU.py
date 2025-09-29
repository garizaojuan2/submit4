import psutil
import platform
import os

# CPUs
logical_cpus = psutil.cpu_count(logical=True)
physical_cpus = psutil.cpu_count(logical=False)
cpu_usage = psutil.cpu_percent(interval=1)

# Memoria
mem = psutil.virtual_memory()
total_mem = mem.total / (1024 ** 2)  # en MB
available_mem_percent = mem.available * 100 / mem.total

# Info de la CPU
cpu_name = platform.processor() or platform.uname().processor
architecture = platform.machine()
freq = psutil.cpu_freq()

# Nota: en Windows no siempre se puede obtener familia, modelo y cache directamente.
# Podemos simular/extraer datos adicionales con wmic si es necesario.

# Ejecutar wmic para obtener info extra (solo Windows)
family = "N/A"
model = "N/A"
l3_cache = "N/A"
cache_align = "64 bytes"

if os.name == "nt":
    try:
        import subprocess
        result = subprocess.check_output("wmic cpu get Name,Family,Stepping,Revision,L3CacheSize /format:list", shell=True).decode()
        for line in result.strip().split("\n"):
            if line.startswith("Family"):
                family = line.split("=")[1].strip()
            elif line.startswith("Revision"):
                model = line.split("=")[1].strip()
            elif line.startswith("L3CacheSize"):
                l3_cache = str(int(line.split("=")[1].strip()) // 1024) + " MB"
    except Exception as e:
        pass

# Mostrar resultados
print(f"Número de CPUs lógicas: {logical_cpus}")
print(f"Porcentaje de uso de la CPU: {cpu_usage}%")
print(f"Total memory: {total_mem:.2f} MB, porcentaje de memoria disponible: {available_mem_percent:.2f}%")
print(f"Modelo: {cpu_name}")
print(f"Arquitectura: {architecture}")
print(f"Familia: {family}")
print(f"Modelo: {model}")
if freq:
    print(f"Frecuencia base reportada: ~{freq.current:.1f} MHz")
print(f"Núcleos: {physical_cpus} núcleo(s) físico(s)")
print(f"Cache L3: {l3_cache}")
print(f"Cache line/align: {cache_align}")
