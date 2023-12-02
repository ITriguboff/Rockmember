import tkinter as tk
from tkinter import filedialog, messagebox
import pickle
from collections import Counter

class AplicacionOrganizador(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lista Conciertos")
        self.geometry("300x400")

        self.lista_datos = self.cargar_datos()  # Cargar datos al iniciar la aplicación

        self.label = tk.Label(self, text="Ingresa una Banda:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self)
        self.entry.pack(pady=10)

        # Botones en la misma línea
        button_frame = tk.Frame(self)
        button_frame.pack()

        self.button_agregar = tk.Button(button_frame, text="Agregar", command=self.agregar_dato)
        self.button_agregar.pack(side=tk.LEFT, padx=5)

        self.button_eliminar = tk.Button(button_frame, text="Eliminar", command=self.eliminar_dato)
        self.button_eliminar.pack(side=tk.LEFT, padx=5)

        self.button_organizar = tk.Button(button_frame, text="Organizar", command=self.organizar_lista)
        self.button_organizar.pack(side=tk.LEFT, padx=5)

        self.button_guardar_texto_plano = tk.Button(self, text="Guardar en Texto Plano", command=self.guardar_en_texto_plano)
        self.button_guardar_texto_plano.pack()

        self.button_importar = tk.Button(self, text="Importar desde Texto Plano", command=self.importar_desde_texto_plano)
        self.button_importar.pack()

        self.resultado_text = tk.Text(self, height=10, width=40)
        self.resultado_text.pack(pady=10)

        # Etiqueta para el contador
        self.contador_label = tk.Label(self, text="Datos ingresados: 0")
        self.contador_label.pack(anchor=tk.NW, padx=10, pady=5)

        # Asociar la función agregar_dato al evento <Return>
        self.entry.bind("<Return>", lambda event: self.agregar_dato())

        # Mostrar los datos al iniciar la aplicación
        self.mostrar_datos()

        # Botón Limpiar Lista al final
        self.button_limpiar_lista = tk.Button(self, text="Limpiar Lista", command=self.limpiar_lista)
        self.button_limpiar_lista.pack()

    def agregar_dato(self):
        dato = self.entry.get().strip().capitalize()  # Primera letra en mayúscula
        if dato:
            self.lista_datos.append(dato)
            self.mostrar_datos()
            self.entry.delete(0, tk.END)
            self.actualizar_contador()

    def eliminar_dato(self):
        dato = self.entry.get().strip().capitalize()  # Primera letra en mayúscula
        if dato in self.lista_datos:
            self.lista_datos.remove(dato)
            self.mostrar_datos()
            self.actualizar_contador()
        self.entry.delete(0, tk.END)

    def mostrar_datos(self):
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, "\n".join(self.lista_datos))

    def organizar_lista(self):
        contador = Counter(self.lista_datos)
        resultado = []

        for dato, cantidad in contador.items():
            resultado.append(f"{dato} ({cantidad})")

        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, "\n".join(resultado))

    def limpiar_lista(self):
        self.lista_datos = []
        self.mostrar_datos()
        self.actualizar_contador()

    def guardar_en_texto_plano(self):
        with filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")]) as file:
            if file:
                for dato, cantidad in Counter(self.lista_datos).items():
                    file.write(f"{dato} ({cantidad})\n")

        messagebox.showinfo("Guardado", "Datos guardados en el archivo de texto")

    def importar_desde_texto_plano(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    # Modificación aquí para procesar datos en formato (n)
                    parts = line.strip().split()
                    dato = " ".join(parts[:-1]).capitalize() if len(parts) > 1 and parts[-1].startswith("(") else line.strip().capitalize()
                    self.lista_datos.append(dato)

            self.mostrar_datos()
            self.actualizar_contador()
            messagebox.showinfo("Importado", "Datos importados desde el archivo de texto")

    def cargar_datos(self):
        try:
            with open("datos.pkl", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []

    def guardar_datos(self):
        with open("datos.pkl", "wb") as file:
            pickle.dump(self.lista_datos, file)

    def actualizar_contador(self):
        cantidad_datos = len(self.lista_datos)
        self.contador_label.config(text=f"Datos ingresados: {cantidad_datos}")

    def destroy(self):
        self.guardar_datos()  # Guardar datos antes de cerrar la aplicación
        super().destroy()

if __name__ == "__main__":
    app = AplicacionOrganizador()
    app.mainloop()
