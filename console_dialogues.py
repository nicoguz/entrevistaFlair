line = "-"*20

STARTING_MENU = f"""
{line}
[1] Iniciar Nueva Simulación
[2] Cargar Estado
[3] Salir
{line}\n
"""
STARTING_MENU_REGEX = r"[1-3]"

MAIN_MENU = f"""
{line}
[1] Mostrar Estado
[2] Ejecutar Paso
[3] Bloquear Habitación
[4] Desbloquear Habitación
[5] Limpiar Habitación
[6] Menu Configuración
[7] Salir
{line}\n
"""
MAIN_MENU_REGEX = r"[1-7]"

CONFIG_MENU = f"""
{line}
[1] Capacidad de Habitaciones
[2] Capacidad de comodidad de Zombies
[3] Resetear Sensor de una Habitación
[4] Verbosidad
[5] Guardar Estado
[6] Cargar Estado
[7] Resetear Simulación
[8] Volver al Menu Principal
{line}\n
"""
CONFIG_MENU_REGEX = r"[1-8]"

ROOM_ACTION_TEXT = """\
Ingresa el número del piso y número de la habitación en forma Piso-Habitación.
Considera que tanto los pisos como las habitaciones comienzan en 1.
Deja en blanco para volver atras.
Ejemplo: 2-3 para la habitación 3 del piso 2.
"""

def ROOM_ACTION_REGEX(total_floors, rooms_per_floor):
    return rf"[1-{total_floors}]-[1-{rooms_per_floor}]"

