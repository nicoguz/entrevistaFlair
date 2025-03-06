from typing import List, Tuple
from random import randint
from aux_functions import determine_zombies_moving, find_save_file
from datetime import datetime
from os.path import isfile
import json

# Se asume un solo edificio
class Building:
    """
    Maneja un set de pisos con habitaciones
    """
    # def __init__(self, total_floors: int, total_rooms: int):
    #     self.floors = [Floor(total_rooms, n_floor) for n_floor in range(total_floors)]

    def __init__(self, total_floors: int, rooms_per_floor: int):
        self.total_floors = total_floors
        self.rooms_per_floor = rooms_per_floor
        self.rooms: List[List[Room]] = []
        for _ in range(total_floors):
            self.rooms.append([Room(n_room) for n_room in range(rooms_per_floor)])
    
    def show_state(self) -> None:
        for floor_idx, floor in enumerate(self.rooms):
            print("-"*30)
            print(f"Piso {floor_idx + 1}:\n")
            for room in floor:
                print(room.show_state())
    
    def get_state(self) -> dict:
        data = {
            "floors": self.total_floors,
            "rooms_per_floor": self.rooms_per_floor,
            "rooms": []
        }

        for floor in self.rooms:
            floor_state = []
            for room in floor:
                floor_state.append(room.get_state())
            
            data["rooms"].append(floor_state)
        
        return data
    
    def load_state(self, data: dict) -> None:
        self.total_floors = data.get("floors")
        self.rooms_per_floor = data.get("rooms_per_floor")
        rooms = data.get("rooms")

        self.rooms: List[List[Room]] = []
        for floor_idx in range(self.total_floors):
            floor = []
            for room_idx in range(self.rooms_per_floor):
                n_zombies = rooms[floor_idx][room_idx][0]
                sensor_state = True if rooms[floor_idx][room_idx][1] == "alert" else False
                blocked = rooms[floor_idx][room_idx][2]
                floor.append(Room(room_idx, n_zombies, sensor_state, blocked))
            self.rooms.append(floor)
    
    def execute_step(self) -> None:

        for floor_idx, floor in enumerate(self.rooms):
            for room in floor:
                # Zombies se mueven a habitaciones adyacentes horizontalmente
                if room.n_zombies > 0:
                    if room.id > 0:
                        left_room = floor[room.id - 1]
                        zombies_out = determine_zombies_moving(room, left_room)
                        room.remove_zombies(zombies_out)
                        left_room.add_zombies(zombies_out)
                    if room.id < len(floor) - 1:
                        right_room = floor[room.id + 1]
                        zombies_out = determine_zombies_moving(room, right_room)
                        room.remove_zombies(zombies_out)
                        right_room.add_zombies(zombies_out)

            # Zombies se mueven a habitaciones adyacentes verticalmente (solo para habitación N)
            if room.n_zombies > 0:
                if floor_idx > 0:
                    down_room = self.rooms[floor_idx - 1][-1]
                    zombies_out = determine_zombies_moving(room, down_room)
                    room.remove_zombies(zombies_out)
                    down_room.add_zombies(zombies_out)
                if floor_idx < len(self.rooms) - 1:
                    up_room = self.rooms[floor_idx + 1][-1]
                    zombies_out = determine_zombies_moving(room, up_room)
                    room.remove_zombies(zombies_out)
                    up_room.add_zombies(zombies_out)

        # Una vez hechos los cálculos, completamos los movimientos
        for floor in self.rooms:
            for room in floor:
                room.commit_zombies()
    
    def add_or_remove_zombies(self, quantity: int) -> None:
        lobby = self.rooms[0][0]
        if lobby.blocked:
            return

        if quantity >= 0:
            lobby.add_zombies(quantity)
        # Si se intentan remover mas de los que se pueden simplemente vaciamos la habitación
        elif quantity < 0 and lobby.n_zombies < quantity*-1:
            lobby.remove_zombies(lobby.n_zombies)
        else:
            lobby.remove_zombies(quantity)
        
        lobby.commit_zombies()
    
    def block_room(self, floor_idx: int, room_idx: int) -> None:
        self.rooms[floor_idx][room_idx].block_room()
        self.show_state()
    
    def unblock_room(self, floor_idx: int, room_idx: int) -> None:
        self.rooms[floor_idx][room_idx].unblock_room()
        self.show_state()
    
    def clean_room(self, floor_idx: int, room_idx: int) -> None:
        self.rooms[floor_idx][room_idx].clean_room()
        self.show_state()
    
    def reset_sensor(self, floor_idx: int, room_idx: int) -> None:
        self.rooms[floor_idx][room_idx].reset_sensor()
        self.show_state()

# class Floor:
#     """
#     Manages a set of rooms
#     """
#     def __init__(self, total_rooms: int, n_floor: int):
#         self.rooms = [Room(n_room) for n_room in range(total_rooms)]
#         self.id = n_floor
    
#     def get_state(self) -> List[int]:
#         with_zombies = []
#         for room in self.rooms:
#             if room.get_state():
#                 with_zombies.append(room.id)
        
#         return with_zombies

class Room:
    """
    Maneja el estado de una habitación
    """
    def __init__(self, n_room: int, n_zombies: int = 0, sensor_state: bool = False, blocked: bool = False):
        self.id = n_room
        self.sensor = Sensor(sensor_state)
        self.n_zombies = n_zombies
        self.entering_zombies = 0
        self.leaving_zombies = 0
        self.blocked = blocked

    def show_state(self) -> str:
        return str(self)

    def get_state(self) -> Tuple[int, str, bool]:
        return [self.n_zombies, self.sensor.state, self.blocked]

    def add_zombies(self, quantity: int) -> None:
        self.entering_zombies += quantity
    
    def remove_zombies(self, quantity: int) -> None:
        self.leaving_zombies += quantity
    
    def commit_zombies(self) -> None:
        if self.entering_zombies == 0 and self.leaving_zombies == 0:
            return

        if self.entering_zombies > 0:
            self.sensor.state = True
        self.n_zombies += self.entering_zombies - self.leaving_zombies
        self.entering_zombies = 0
        self.leaving_zombies = 0
    
    def reset_sensor(self) -> None:
        self.sensor.state = False
        print("Sensor reseteado")
    
    def clean_room(self) -> None:
        self.n_zombies = 0
        print("Habitación limpiada")
    
    def block_room(self) -> None:
        self.blocked = True
        print("Habitación bloqueada")
    
    def unblock_room(self) -> None:
        self.blocked = False
        print("Habitación desbloqueada")

    def __str__(self):
        return f"- Room {self.id + 1}{' (blocked)' if self.blocked else ''}: {self.sensor}, {self.n_zombies} zombies"

class Sensor:
    """
    Sensor de habitación

    state == False: normal
    state == True: alert (han pasado zombies por aquí)
    """
    def __init__(self, init_state: bool = False):
        self._state = init_state
    
    @property
    def state(self) -> bool:
        if self._state: 
            return "alert"
        return "normal"
    
    @state.setter
    def state(self, value: bool) -> None:
        if type(value) == bool: self._state = value
        else:
            raise TypeError("Sensor state must be a boolean")

    def __str__(self):
        return self.state

class Simulation:
    """
    Corre la simulación
    """
    def __init__(self, total_floors: int = 5, rooms_per_floor: int = 5):
        self.building = Building(total_floors, rooms_per_floor)

    def run_step(self) -> None:
        # Cada turno, una cantidad aleatoria de zombies entran o salen del edificio por la puerta de entrada
        self.building.add_or_remove_zombies(randint(-5, 15))
        self.building.execute_step()
        self.show_state()
    
    def show_state(self) -> None:
        self.building.show_state()
    
    def save_state(self, name: str = "") -> str:
        if name == "":
            now = datetime.now().strftime("%d_%m_%y-%H_%M_%S")
            file_name = f"./saved_states/{now}.json"
        else:
            file_name = f"./saved_states/{name}.json"

        data = self.building.get_state()

        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        return file_name
    
    def load_state(self, name: str) -> Tuple[int, int]:
        found_name = find_save_file(name)
        if not found_name:
            print("El archivo no existe")
            return
        
        with open(f"./saved_states/{found_name}", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.building.load_state(data)

        return data.get("floors"), data.get("rooms_per_floor")
    
    def reset(self) -> None:
        total_floors = self.building.total_floors
        rooms_per_floor = self.building.rooms_per_floor
        self.building = Building(total_floors, rooms_per_floor)