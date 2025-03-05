from console_dialogues import *
from classes import Simulation
from aux_functions import find_save_file
from os import listdir
import re

# chosen_option = None
def main_simulation():

    simulation = None
    TOTAL_FLOORS = None
    ROOMS_PER_FLOOR = None

    print("Bienvenido al simulador de zombies!")
    print("Para comenzar escoge una opción ingresando el numero correspondiente:")

    # Loop inicial, se rompe solo si se escoge una opción válida
    while True:
        chosen_option = input(STARTING_MENU).strip()

        while re.fullmatch(STARTING_MENU_REGEX, chosen_option) == None:
            print("Opción no valida. Para escoger solo debes ingresar el número de la opción que deseas. Intenta de nuevo:")
            chosen_option = input(STARTING_MENU).strip()

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
            TOTAL_FLOORS = total_floors
            ROOMS_PER_FLOOR = rooms_per_floor
            break

        elif chosen_option == "2":
            print("Estados guardados:")
            any_save_file = False
            for file in listdir("./save_states"):
                if file.endswith(".json"):
                    any_save_file = True
                    print(f"- {file}")
            
            if not any_save_file:
                print("No hay estados guardados. Volviendo al menú inicial...")
                continue

            load_file_text = "Ingresa el nombre del archivo a cargar o deja en blanco para volver atras: "

            file_name = input(load_file_text).strip()

            while file_name != "" and find_save_file(file_name) == False:
                print(f"Archivo {file_name} no encontrado. Intenta de nuevo:")
                file_name = input(load_file_text).strip()

            if file_name == "":
                continue
            
            simulation = Simulation()
            TOTAL_FLOORS, ROOMS_PER_FLOOR = simulation.load_state(file_name)
            break
        
        elif chosen_option == "3":
            sure = input("Estás seguro que deseas salir? (s/n): ").strip()
            if sure.lower() == "s":
                print("Hasta luego!")
                return
            else:
                print("Cancelado.Volviendo al menú principal...")
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
        elif chosen_option == "3" or chosen_option == "4" or chosen_option == "5":
            room_to_block = input(ROOM_ACTION_TEXT).strip()

            while room_to_block != "" and re.fullmatch(ROOM_ACTION_REGEX(TOTAL_FLOORS, ROOMS_PER_FLOOR), room_to_block) == None:
                print("Opción no valida o habitación no encontrada. Intenta de nuevo:")
                room_to_block = input(ROOM_ACTION_TEXT).strip()
            
            if room_to_block == "":
                continue

            floor_number, room_number = room_to_block.split("-")

            # Se les resta 1 para que queden en base 0
            floor_number = int(floor_number) - 1
            room_number = int(room_number) - 1
            
            if chosen_option == "3":
                simulation.building.rooms[floor_number][room_number].block_room()
            elif chosen_option == "4":
                simulation.building.rooms[floor_number][room_number].unblock_room()
            elif chosen_option == "5":
                simulation.building.rooms[floor_number][room_number].clean_room()
        elif chosen_option == "6":
            pass
        elif chosen_option == "7":
            sure = input("Estás seguro que deseas salir? (s/n): ").strip()
            if sure.lower() == "s":
                print("Hasta luego!")
                return
            else:
                print("Cancelado.Volviendo al menú principal...")
                continue
                




# TODO: Limitar los save states para evitar demasiados archivos