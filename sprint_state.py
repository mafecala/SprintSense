# sprint_state.py

class SprintState:
    def __init__(self):
        self.tareas = {
            "Tarea 1": "To Do",
            "Tarea 2": "In Progress",
            "Tarea 3": "To Do"
        }
        self.seleccionada = None

    def marcar_completada(self):
        if self.seleccionada and self.tareas.get(self.seleccionada) != "Done":
            self.tareas[self.seleccionada] = "Done"

    def tareas_completadas(self):
        return {k: v for k, v in self.tareas.items() if v == "Done"}

    def seleccionar_tarea_por_posicion(self, y):
        index = (y - 100) // 30
        if 0 <= index < len(self.tareas):
            self.seleccionada = list(self.tareas.keys())[index]
        else:
            self.seleccionada = None
