import tkinter as tk
from tkinter import messagebox, simpledialog
import csv

class Interfaz:
    def __init__(self, ciudades):
        self.ciudades = ciudades  # lista de objetos Nodo
        self.solicitudes = []

    def crear_solicitud(self):
        ventana = tk.Tk()
        ventana.withdraw()  # Oculta ventana principal hasta pedir la cantidad

        cantidad = simpledialog.askinteger("Solicitudes", "¿Cuántas solicitudes desea crear?", minvalue=1, parent=ventana)
        if not cantidad:
            ventana.destroy()
            return

        ventana.deiconify()
        ventana.title("Crear Solicitudes")

        index = 0  # Indice de solicitud

        def solicitar_datos():
            nonlocal index

            if index >= cantidad:
                messagebox.showinfo("Finalizado", "Todas las solicitudes han sido creadas.")
                ventana.destroy()

                # Guardar en CSV
                with open("nuevas_solicitudes.csv", "w", newline="", encoding="utf-8") as archivo:
                    writer = csv.writer(archivo)
                    writer.writerow(["id_carga", "peso_kg", "origen", "destino"])
                    for i, s in enumerate(self.solicitudes, start=1):
                        writer.writerow([f"CARGA_{i:03d}", s[1], s[2].ciudad, s[3].ciudad])

                print("Solicitudes creadas:")
                for s in self.solicitudes:
                    print(s)
                return

            for widget in ventana.winfo_children():
                widget.destroy()

            tk.Label(ventana, text=f"Solicitud #{index + 1}").pack(pady=5)

            tk.Label(ventana, text="Ciudad de origen:").pack()
            entry_origen = tk.Entry(ventana)
            entry_origen.pack()

            tk.Label(ventana, text="Ciudad de destino:").pack()
            entry_destino = tk.Entry(ventana)
            entry_destino.pack()

            tk.Label(ventana, text="Peso (kg):").pack()
            entry_peso = tk.Entry(ventana)
            entry_peso.pack()

            def validar_y_guardar():
                nonlocal index #para que sepa que no estoy intenando crear una copia de la variabel index, sino que estoy modificando la variable que esta en un nivel mas de la funcion
                origen_nombre = entry_origen.get().strip()
                destino_nombre = entry_destino.get().strip()
                peso_input = entry_peso.get().strip()

                origen = next((c for c in self.ciudades if c.ciudad.lower().replace("_", " ") == origen_nombre.lower()), None)
                destino = next((c for c in self.ciudades if c.ciudad.lower().replace("_", " ") == destino_nombre.lower()), None)

                errores = []
                if not origen:
                    errores.append("Ciudad de origen no válida.")
                if not destino:
                    errores.append("Ciudad de destino no válida.")
                try:
                    peso = float(peso_input)
                    if peso <= 0:
                        errores.append("El peso debe ser mayor a 0.")
                except ValueError:
                    errores.append("El peso debe ser un número válido.")

                if errores:
                    messagebox.showerror("Error", "\n".join(errores))
                    return

                nueva_solicitud = [f"CARGA_{index+1:03d}", peso, origen, destino]
                self.solicitudes.append(nueva_solicitud)
                index += 1
                solicitar_datos()

            tk.Button(ventana, text="Guardar", command=validar_y_guardar).pack(pady=10)

        solicitar_datos()
        ventana.mainloop()
