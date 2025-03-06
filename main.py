from console_dialogues import *
from classes import Simulation
from aux_functions import find_save_file
from os import listdir
import re
from typing import Union

general_state = {
    "total_floors": None,
    "rooms_per_floor": None
}

# chosen_option = None
def main_simulation():

    simulation = None


    print("Bienvenido al simulador de zombies!")
    print("Para comenzar escoge una opción ingresando el numero correspondiente:")

    # Loop inicial, se rompe solo si se escoge una opción válida
    while True:
        chosen_option = input(STARTING_MENU).strip()

        while re.fullmatch(STARTING_MENU_REGEX, chosen_option) == None:
            print("Opción no valida. Para escoger solo debes ingresar el número de la opción que deseas. Intenta de nuevo:")
            chosen_option = input(STARTING_MENU).strip()

        # Nueva simulación
        if chosen_option == "1":
            total_floors_message = "Ingresa el total de pisos del edificio (deja en blanco para valor default): "
            total_floors = input(total_floors_message).strip()

            if total_floors == "":
                total_floors = "5"

            while total_floors.isnumeric() == False:
                print("Opción no valida. Debes ingresar un número entero positivo. Intenta de nuevo:")
                total_floors = input(total_floors_message).strip()
            
            total_floors = int(total_floors)

            rooms_per_floor_message = "Ingresa el total de habitaciones por piso (deja en blanco para valor default): "
            rooms_per_floor = input(rooms_per_floor_message).strip()

            if rooms_per_floor == "":
                rooms_per_floor = "5"

            while rooms_per_floor.isnumeric() == False:
                print("Opción no valida. Debes ingresar un número entero positivo. Intenta de nuevo:")
                rooms_per_floor = input(rooms_per_floor_message).strip()
            
            rooms_per_floor = int(rooms_per_floor)

            simulation = Simulation(total_floors, rooms_per_floor)
            general_state["total_floors"] = total_floors
            general_state["rooms_per_floor"] = rooms_per_floor
            break

        # Cargar simulación
        elif chosen_option == "2":
            state_info = load_state()

            # Volvemos al menú principal
            if state_info == "continue":
                continue

            simulation = state_info
            break
        
        elif chosen_option == "3":
            sure = input("Estás seguro que deseas salir? (s/n): ").strip()
            if sure.lower() == "s":
                print("Hasta luego!")
                return
            else:
                print("Cancelado. Volviendo al menú principal...")
                continue
    
    # Loop principal, se rompe solo si se escoge una opcion valida
    while True:
        chosen_option = input(MAIN_MENU).strip()

        while re.fullmatch(MAIN_MENU_REGEX, chosen_option) == None:
            print("Opción no valida. Para escoger solo debes ingresar el número de la opción que deseas. Intenta de nuevo:")
            chosen_option = input(MAIN_MENU).strip()

        # Mostrar estado
        if chosen_option == "1":
            simulation.show_state()
        # Ejecutar paso
        elif chosen_option == "2":
            simulation.run_step()
        # Bloquear, desbloquear y limpiar habitación
        elif chosen_option == "3" or chosen_option == "4" or chosen_option == "5" or chosen_option == "6":
            room_to_block = input(ROOM_ACTION_TEXT).strip()

            room_regex = ROOM_ACTION_REGEX(general_state["total_floors"], general_state["rooms_per_floor"])

            while (room_to_block != "" and re.fullmatch(room_regex, room_to_block) == None):
                print("Opción no valida o habitación no encontrada. Intenta de nuevo:")
                room_to_block = input(ROOM_ACTION_TEXT).strip()
            
            if room_to_block == "":
                continue

            floor_number, room_number = room_to_block.split("-")

            # Se les resta 1 para que queden en base 0
            floor_number = int(floor_number) - 1
            room_number = int(room_number) - 1
            
            if chosen_option == "3":
                simulation.building.block_room(floor_number, room_number)
            elif chosen_option == "4":
                simulation.building.unblock_room(floor_number, room_number)
            elif chosen_option == "5":
                simulation.building.clean_room(floor_number, room_number)
            elif chosen_option == "6":
                simulation.building.reset_sensor(floor_number, room_number)
        
        # Menú configuración
        elif chosen_option == "7":
            new_simulation = config_loop(simulation)

            if new_simulation is not None:
                simulation = new_simulation

        elif chosen_option == "8":
            sure = input("Estás seguro que deseas salir? (s/n): ").strip()
            if sure.lower() == "s":
                print("Hasta luego!")
                return
            else:
                print("Cancelado. Volviendo al menú principal...")
                continue
                
def load_state() -> Union[str, Simulation]:
    print("Estados guardados:")
    any_save_file = False
    for file in listdir("./saved_states"):
        if file.endswith(".json"):
            any_save_file = True
            print(f"- {file}")
    
    if not any_save_file:
        print("No hay estados guardados. Volviendo al menú inicial...")
        return "continue"

    load_file_text = "Ingresa el nombre del archivo a cargar o deja en blanco para volver atras: "

    file_name = input(load_file_text).strip()

    while file_name != "" and find_save_file(file_name) == False:
        print(f"Archivo {file_name} no encontrado. Intenta de nuevo:")
        file_name = input(load_file_text).strip()

    if file_name == "":
        return "continue"
    
    print("Cargando estado...")
    
    simulation = Simulation()
    total_floors, rooms_per_floor = simulation.load_state(file_name)

    general_state["total_floors"] = total_floors
    general_state["rooms_per_floor"] = rooms_per_floor

    print("Estado cargado con éxito")
    
    return simulation

def config_loop(simulation: Simulation) -> None:
    while True:
        chosen_option = input(CONFIG_MENU).strip()

        while re.fullmatch(CONFIG_MENU_REGEX, chosen_option) == None:
            print("Opción no valida. Para escoger solo debes ingresar el número de la opcion que deseas. Intenta de nuevo:")
            chosen_option = input(CONFIG_MENU).strip()

        # Guardar estado
        if chosen_option == "1":
            # Chequeo que no hayan demasiados archivos en la carpeta
            if len(listdir("./saved_states")) >= 10:
                print("Has alcanzado el límite (10) de archivos guardados. Elimina algunos para poder guardar el nuevo.")
                print("Para eliminar estados debes hacerlo manualmente en la carpeta ./saved_states.")
                continue
            file_name = input("Ingresa el nombre con el que deseas guardar el estado: ")
            print("Guardando estado...")
            saved_name = simulation.save_state(file_name)
            print(f"Estado guardado en el archivo {saved_name}")

        # Cargar estado
        elif chosen_option == "2":
            state_info = load_state()

            # Volvemos al menú principal
            if state_info == "continue":
                continue

            simulation = state_info
            return simulation

        # Resetear simulación
        elif chosen_option == "3":
            response = input("Estás seguro que deseas resetear la simulación? (s/n): ").strip()

            if response.lower() == "s":
                print("Reseteando simulación...")
                simulation.reset()
                print("Simulación reseteada con éxito")
                return
        
        elif chosen_option == "4":
            return

if __name__ == "__main__":
    main_simulation()
