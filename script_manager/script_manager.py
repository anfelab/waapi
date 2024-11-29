import tkinter as tk

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WAAPI Script Manager")
        self.minsize(720,480)
        btn = tk.Button(self, text = "Boton")

        btn.pack()

if __name__ == "__main__":
    root = Interface()
    root.mainloop()