# entrevistaFlair

preguntas:
* Cuando un zombie sale de la habitación el sensor pasa a normal de nuevo?
  Yo creo que no, porque al mostrar el estado se pide el estado de cada habitación y si tiene zombies o no
  por lo que sería redundante, todas las habitaciones que tienen zombies estan en alerta y las que no simplemente están normales

Algunas consideraciones:
* Cada room tiene una función get_state que solo devuelve su string. Esto se hace para generalizar el llamado a su estado, en caso que en algún futuro se complejice la clase y se necesiten operaciones extra.

* Para la verificación de entrada se ocupa regex, incluso para los casos más simples. Esto se hace para mantener la misma lógica de chequeo que con otras opciones del menú que requieren de inputs más complejos.

Buenas prácticas consideradas:
* Validación de inputs
* Guardado y manejo de save states

Asunciones:
* Se asume que la carpeta `save_states` no incluirá archivos json con formato distinto al definido para los save_state (ejemplo en carpeta!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!). Se puede modificar el código para que considere estos casos, pero es un chequeo extra que potencialmente podría ralentizar la app.