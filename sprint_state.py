class SprintState:
    def __init__(self):
        self.tareas = {
            "Tarea 1": "To Do",
            "Tarea 2": "In Progress",
            "Tarea 3": "To Do"
        }
        self.seleccionada = None
        self.modo_dibujo = False
        self.modo_crear = False
        self.editando = False
        self.nuevo_texto = ""

    @property
    def modo_seleccion(self):
        return not self.modo_dibujo

    def toggle_modo_dibujo(self):
        self.modo_dibujo = not self.modo_dibujo
        self.modo_crear = False
        self.editando = False
        self.nuevo_texto = ""
        self.seleccionada = None

    def iniciar_creacion(self):
        self.modo_crear = True
        self.editando = False
        self.nuevo_texto = ""

    def crear_nueva_tarea(self):
        if self.nuevo_texto.strip():
            self.tareas[self.nuevo_texto.strip()] = "To Do"
        self.modo_crear = False
        self.nuevo_texto = ""

    def iniciar_edicion(self):
        if self.seleccionada:
            self.editando = True
            self.modo_crear = False
            self.nuevo_texto = self.seleccionada

    def confirmar_edicion(self):
        if self.seleccionada and self.nuevo_texto.strip():
            estado = self.tareas[self.seleccionada]
            del self.tareas[self.seleccionada]
            self.tareas[self.nuevo_texto.strip()] = estado
        self.editando = False
        self.nuevo_texto = ""

    def eliminar_tarea(self):
        if self.seleccionada:
            del self.tareas[self.seleccionada]
            self.seleccionada = None

    def marcar_completada(self):
        if self.seleccionada:
            self.tareas[self.seleccionada] = "Done"
