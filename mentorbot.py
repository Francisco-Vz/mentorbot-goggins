import schedule
import time
import json
from datetime import datetime
from plyer import notification

# Ruta del archivo donde guardaremos las tareas
TAREAS_FILE = "tareas.json"

# Frases estilo Goggins
GOGGINS_QUOTES = [
    "¡No seas blando! Tienes trabajo que hacer.",
    "No estás cansado, estás cómodo. ¡Muévete!",
    "Las excusas son para los que se rinden. Tú no eres uno de ellos.",
    "¡Mantente fuerte! Stay hard.",
    "Tu mente quiere parar, pero tú sigues. ¡Eres imparable!"
]

# Cargar tareas desde archivo
def cargar_tareas():
    try:
        with open(TAREAS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Guardar tareas al archivo
def guardar_tareas(tareas):
    with open(TAREAS_FILE, "w") as f:
        json.dump(tareas, f, indent=2)

# Mostrar notificación
def notificar(mensaje):
    notification.notify(
        title="MentorBot Goggins 💪",
        message=mensaje,
        timeout=10
    )

# Recordatorio diario
def recordatorio_diario():
    tareas = cargar_tareas()
    hoy = datetime.now().strftime("%Y-%m-%d")
    tareas_hoy = [t for t in tareas if t["fecha"] == hoy and not t["completada"]]

    if tareas_hoy:
        mensaje = f"{len(tareas_hoy)} tarea(s) pendientes. ¡{GOGGINS_QUOTES[datetime.now().second % len(GOGGINS_QUOTES)]}"
        notificar(mensaje)
    else:
        notificar("¡Buen trabajo, soldado! No tienes tareas pendientes. Pero no te duermas. Crea nuevos retos.")

# Agregar nueva tarea
def agregar_tarea():
    descripcion = input("¿Cuál es la tarea que quieres agregar?: ").strip()
    fecha = input("¿Para qué fecha es? (formato YYYY-MM-DD, o presiona Enter para hoy): ").strip()

    if not fecha:
        fecha = datetime.now().strftime("%Y-%m-%d")

    nueva_tarea = {
        "descripcion": descripcion,
        "fecha": fecha,
        "completada": False
    }

    tareas = cargar_tareas()
    tareas.append(nueva_tarea)
    guardar_tareas(tareas)

    print(f"✅ Tarea agregada: {descripcion} para el {fecha}")

# Ver tareas
def mostrar_tareas():
    tareas = cargar_tareas()
    if not tareas:
        print("No tienes tareas aún. ¡Hora de crear retos!")
        return

    for i, t in enumerate(tareas):
        estado = "✅" if t["completada"] else "⏳"
        print(f"{i + 1}. [{estado}] {t['descripcion']} (para {t['fecha']})")

# Marcar tarea como completada
def completar_tarea():
    mostrar_tareas()
    try:
        num = int(input("¿Qué número de tarea completaste?: "))
        tareas = cargar_tareas()
        if 1 <= num <= len(tareas):
            tareas[num - 1]["completada"] = True
            guardar_tareas(tareas)
            print("💪 Tarea marcada como completada. ¡Así se hace!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Ingresa un número válido.")

# Menú principal
def menu():
    while True:
        print("\n--- MentorBot Goggins ---")
        print("1. Ver tareas")
        print("2. Agregar tarea")
        print("3. Completar tarea")
        print("4. Salir")

        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            mostrar_tareas()
        elif opcion == "2":
            agregar_tarea()
        elif opcion == "3":
            completar_tarea()
        elif opcion == "4":
            print("¡Vuelve pronto, soldado! Stay hard.")
            break
        else:
            print("Opción no válida.")

# Programar recordatorios
schedule.every(60).minutes.do(recordatorio_diario)

# Ejecutar menú y recordatorios al mismo tiempo
import threading

def correr_recordatorios():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Iniciar recordatorios en segundo plano
hilo = threading.Thread(target=correr_recordatorios)
hilo.daemon = True
hilo.start()

# Iniciar menú principal
menu()
