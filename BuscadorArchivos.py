from tkinter import filedialog
from tkinter import *
import os

ventana = ()

def abrir_archivo():
  archivo_abierto = filedialog.askopenfilename(initialdir = "/", title = "Seleccione archivo, filetypes = (("txt files",".txt"),("csv files",".csv"),("excel files",".xlsx")))
  print(archivo_abierto)

Button (text = "Abrir archivo", bg = "pale green",command = abrir_archivo).place(x=10,y=10)
