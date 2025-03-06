from random import randint
from typing import TYPE_CHECKING
from os.path import isfile

# Evitamos dependencia circular importando solo para chequeo de tipado
if TYPE_CHECKING:
    from classes import Room

# Capacidad física que aguanta una habitación
MAX_ZOMBIES_IN_ROOM = 50

# Capacidad máxima a la cual los zombies se sienten cómodos en una habitación
MAX_COMODITY_ZOMBIES = 20

def determine_zombies_moving(current_room: "Room", adjacent_room: "Room") -> int:
    remaining_zombies = current_room.n_zombies - current_room.leaving_zombies

    # Primero chequeamos si podemos mover zombies y si la habitación adyacente se llenará
    if (remaining_zombies == 0 or adjacent_room.blocked or
        adjacent_room.n_zombies + adjacent_room.entering_zombies >= MAX_ZOMBIES_IN_ROOM):
        return 0
    
    # Si hay demasiados zombies en una habitación, se deben mover al menos 5, ya que
    # muchos están incomodos y quieren más espacio.
    if remaining_zombies >= MAX_COMODITY_ZOMBIES:
        moving = randint(5, remaining_zombies)
    else:
        moving = randint(0, remaining_zombies)

    if moving + adjacent_room.n_zombies + adjacent_room.entering_zombies > MAX_ZOMBIES_IN_ROOM:
        moving = MAX_ZOMBIES_IN_ROOM - adjacent_room.n_zombies - adjacent_room.entering_zombies
    
    return moving

def find_save_file(name: str) -> str:
    if name == "":
        return False
    
    # Formateamos la extensión a .json
    if name[-5:] == ".json":
        name = name[:-5]
    
    if isfile(f"./saved_states/{name}.json"):
        return f"{name}.json"
    
    return False
