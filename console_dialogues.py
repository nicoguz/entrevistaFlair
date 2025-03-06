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
[6] Resetear Sensor de Habitación
[7] Menu Configuración
[8] Salir
{line}\n
"""
MAIN_MENU_REGEX = r"[1-8]"

CONFIG_MENU = f"""
{line}
[1] Verbosidad
[2] Guardar Estado
[3] Cargar Estado
[4] Resetear Simulación
[5] Volver al Menu Principal
{line}\n
"""
CONFIG_MENU_REGEX = r"[1-5]"

ROOM_ACTION_TEXT = """\
Ingresa el número del piso y número de la habitación en forma Piso-Habitación.
Considera que tanto los pisos como las habitaciones comienzan en 1.
Deja en blanco para volver atras.
Ejemplo: 2-3 para la habitación 3 del piso 2.
"""

def ROOM_ACTION_REGEX(total_floors, rooms_per_floor):
    return rf"[1-{total_floors}]-[1-{rooms_per_floor}]"

