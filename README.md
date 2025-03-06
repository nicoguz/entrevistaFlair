# entrevistaFlair

## Ejecución
Para comenzar la simulación solo se debe correr el archivo main.py. Es importante si que el resto de los módulos esten presentes, además de la carpeta de saved_states.

## Funcionamiento
Ocupé loops `while` para manejar la interfaz de usuario y para asegurarme que los inputs del mismo sean válidos. Existen 3 menús:
* Menú inicial --> Se muestran las dos opciones para comenzar una simulación (estado guardado o uno nuevo)
* Menú principal --> Contiene las funciones principales del programa
* Menú de configuración --> Aquí se pueden guardar, cargar y resetear los estados del programa.

Para escoger cada opción solo se debe ingresar el número de la misma. Cuando se pida el número de una habitación, se debe ingresar en la forma Piso-Habitación (1-1 por ejemplo), siempre considerando que los pisos y habitaciones comienzan en 1.

## Algunas consideraciones:
* Para la verificación de entrada se ocupa regex, incluso para los casos más simples. Esto se hace para mantener la misma lógica de chequeo que con otras opciones del menú que requieren de inputs más complejos.
* Los zombies pueden subir y bajar de pisos en la habitación N-ésima, pero es un suceso aleatorio.
* La lógica de expansión es aleatoria. Es decir, se expande un número aleatorio de zombies (0-máx en la habitación) cada turno, respetando la cantidad de zombies en cada habitación. Si una habitación tiene 20 zombies o más, se moverán al menos 5. Por último, cada habitación tiene una capacidad física de 50, exceptuando el lobby.
* Los zombies parten desde el lobby (Piso 1 - habitación 1) y se expanden al resto de las habitaciones.

## Arquitectura
Se sigue la estructura recomendada, exceptuando la clase Floors. Consideré que el manejo de una matriz de rooms sería más simple que añadir una estructura nueva para cada piso, sobretodo teniendo en cuenta que floors en este minuto no tiene ninguna responsabilidad particular más que el manejo de rooms.
* Simulation --> Maneja la simulación y un building
* Building --> Maneja una matriz de rooms que representan un edificio. Recolecta los estados de los rooms para poder mostrarlos en consola también
* Room --> Simula una habitación. Puede ser bloqueada y limpiada.
* Sensor --> Alerta cuando un zombie entra en una habitación. Una vez en alerta se mantiene en este estado hasta que se resetee.

## Estrucutra Repositorio
* `aux_functions.py` --> Funciones de utilidad que se dejan en un módulo a parte para que puedan ser usados por múltiples archivos o simplemente por limpieza y legibilidad de código.
* `classes.py` --> Contiene las clases descritas en `Arquitectura`
* `console_dialogues.py` --> Contiene textos largos que se muestran en consola, como los menús. Se separan de main para mejor legibilidad. También contiene los patrones Regex de cada menú para la verificación de inputs.
* `main.py` --> Lógica principal del programa. Contiene el loop de la interfaz de usuario, donde se chequean inputs, ejecutan las funciones implementadas y se diseña la interfaz y su lógica para una mejor experiencia de usuario.

## Asunciones:
* Se asume que la carpeta `saved_states` no incluirá otros archivos que no sean los creados por la app.
* Se asume que solo existe un edificio en este mundo post-apocaliptico.