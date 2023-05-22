#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################################################
# Script: ProyectoIA.py.
# Entidad académica: Facultad de Ingeniería, UNAM.
# Asignatura: Inteligencia Artificial
# Autor: Hernández Fontes, Aldo.
# Fecha de creación: Noviembre 23, 2020.
# Última de actualización: Enero 13, 2021.
##########################################################################################################
# .: Biblioteca(s) :.
import numpy as np                  # Biblioteca para la creación vectores y matrices de n dimensiones
# Biblioteca para la generación de gráficas a partir de datos contenidos en listas
import matplotlib.pyplot as plt
import pandas as pd                 # Biblioteca para la manipulación y análisis de datos
from apyori import apriori          # Módulo para la manipulación y análisis de datos
from tkinter import filedialog      # Módulo para la creación de una ventana de busqueda de archivos
from tkinter import *               # Módulos para la creación de una interfáz gráfica
from math import sqrt               # Módulo para obtener la distancia euclidiana
from scipy.spatial import distance  # Módulo para obtener la distancia euclidiana
import os                           # Biblioteca para la manipulación a nivel path
import seaborn as sb  # Biblioteca para visualización de datos basado en matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
from mpl_toolkits.mplot3d import Axes3D

pd.options.display.max_rows = None
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None
pd.options.display.expand_frame_repr = True
pd.options.display.width = 999
##########################################################################################################
# .: Funcion(es) :.
# Función. Número de filas y columnas


def FilasYColumnas(Datos):
    filas = len(Datos)
    columnas = 0
    for i in Datos:
        columnas = columnas + 1
    return filas, columnas
# Reglas de asociación. Algoritmo Apriori
# Función. Algoritmo Apriori para archivos CSV, TXT y XLSX


def Apriori(nombreArchivo, soporte, confianza, lift, tamano):
    # Se determina el tipo de archivo
    tipo = nombreArchivo.split('.')[1]
    # Se determina si es un archivo .txt
    if (tipo == 'txt'):
        # Se leen los datos
        Datos = pd.read_table(nombreArchivo, header=None)
    elif (tipo == 'xlsx'):
        # Se leen los datos
        Datos = pd.read_excel(nombreArchivo, header=None)
    elif (tipo == 'csv'):
        # Se leen los datos
        Datos = pd.read_csv(nombreArchivo, header=None)
    # Se determina el número de filas y de columnas
    filas, columnas = FilasYColumnas(Datos)
    # Se determinan las transacciones realizadas
    Transacciones = []
    for i in range(0, filas):
        Transacciones.append([str(Datos.values[i, j]) for j in range(0, columnas)])
    # Se aplica el algoritmo apriori
    Reglas = apriori(Transacciones, min_support=soporte,
                     min_confidence=confianza, min_lift=lift, min_length=tamano)
    # Se retornan los resultados
    Resultados = list(Reglas)
    return Resultados

# Borrar los elementos de la ventana


def limpiar(contenedor):
    list = contenedor.grid_slaves()
    for i in list:
        i.destroy()

##########################################################################################################
# Clase(s)
# Clase. Ventana principal


class Aplicacion:
    def __init__(self, contenedor):
        limpiar(contenedor)
        self.contenedor = contenedor
        # Variables
        self.archivoRuta = ''
        self.cadena = StringVar()
        texto = ""
        self.datos = pd.DataFrame()
        self.MCorrelaciones = pd.DataFrame()
        # Apriori
        self.confianza = DoubleVar()
        self.confianza.set(0.1)
        self.lift = DoubleVar()
        self.lift.set(0.1)
        self.tamano = IntVar()
        self.tamano.set(1)
        self.soporte = DoubleVar()
        self.soporte.set(0.1)
        # correlacional
        self.cadena1 = StringVar()
        self.cadena2 = StringVar()
        # Elementos o componentes
        self.button1 = Button(contenedor, text="Seleccionar archivo",
                              command=lambda: self.cadena.set(self.abrirArchivo()))
        self.label0 = Label(contenedor, text="Nombre: ")
        self.textField1 = Entry(contenedor, textvariable=self.cadena, state=DISABLED)
        self.button3 = Button(contenedor, text="Seleccionar algoritmo",
                              command=self.seleccionarAlgoritmo, state=DISABLED)
        self.xscrollbar = Scrollbar(contenedor, orient=HORIZONTAL)
        self.yscrollbar = Scrollbar(contenedor)
        self.textArea1 = Text(contenedor, bd=5, wrap=NONE,
                              xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)
        self.xscrollbar.config(command=self.textArea1.xview)
        self.yscrollbar.config(command=self.textArea1.yview)
        self.button2 = Button(contenedor, text="Mostrar datos",
                              command=self.MostrarDatos, state=DISABLED)
        self.guardar = Button(contenedor, text="Guardar", command=self.guardar, justify=RIGHT)
        self.borrar = Button(contenedor, text="Borrar", command=self.borrar)
        self.button4 = Button(contenedor, text="Diagnóstico", command=self.diagnostico)
        # Posición
        self.label0.grid(row=0, column=1)
        self.button1.grid(row=0, column=0)
        self.textField1.grid(row=0, column=2)
        self.button3.grid(row=1, column=0)
        self.button4.grid(row=1, column=1)
        self.button2.grid(row=1, column=2)
        self.textArea1.grid(row=2, column=0, columnspan=3)
        self.yscrollbar.grid(row=2, column=4, sticky=N+S+E+W)
        self.xscrollbar.grid(row=3, column=0, columnspan=3, sticky=N+S+E+W)
        self.guardar.grid(row=4, column=2)
        self.borrar.grid(row=4, column=0)

    # .: Método(s) :.
    # Método. abrir Archivo
    def abrirArchivo(self):
        self.archivoRuta = filedialog.askopenfilename(initialdir="/", title="Seleccione archivo", filetypes=(
            ("txt files", "*.txt"), ("csv files", "*.csv"), ("excel files", "*.xlsx")))
        nombreArchivo = os.path.split(self.archivoRuta)[1]
        self.textArea1.delete("1.0", END)
        self.button2.config(state=ACTIVE)
        self.button3.config(state=ACTIVE)
        return nombreArchivo

    # Función. Obtener datos
    def ObtenerDatos(self, nombreArchivo):
        # Se determina el tipo de archivo
        tipo = nombreArchivo.split('.')[1]
        # Se determina si es un archivo .txt
        if (tipo == 'txt'):
            # Se leen los datos
            Datos = pd.read_table(nombreArchivo, header=None)
        elif (tipo == 'xlsx'):
            # Se leen los datos
            Datos = pd.read_excel(nombreArchivo, header=None)
        elif (tipo == 'csv'):
            # Se leen los datos
            Datos = pd.read_csv(nombreArchivo, header=None)
        self.textArea1.insert(END, ".: DATOS :.\n")
        self.textArea1.insert(END, Datos)
        self.textArea1.see(END)

    # Función. Mostrar datos
    def MostrarDatos(self):
        self.ObtenerDatos(self.archivoRuta)
        self.textArea1.insert(END, '\n')

    # Método. Seleccionar algoritmo.
    # Abre una ventana la cual contiene los botones para hacer el algoritmo que desee el usuario
    def seleccionarAlgoritmo(self):
        # Especificaciones de ventana
        self.ventana3 = Toplevel()
        self.ventana3.resizable(0, 0)
        self.ventana3.title("Seleccionar algoritmo")
        # Elementos o componentes
        self.B_Temp1 = Button(self.ventana3, text="Apriori", command=self.Apriori)
        self.B_Temp2 = Button(self.ventana3, text="Correlacional", command=self.correlacional)
        self.B_Temp3 = Button(self.ventana3, text="Métricas de similitud", command=self.metricas)
        self.B_Temp4 = Button(self.ventana3, text="Clustering", command=self.clustering)
        self.B_Temp5 = Button(self.ventana3, text="Cerrar", command=self.ventana3.destroy)
        # Posicion
        self.B_Temp1.grid(row=0, column=0)
        self.B_Temp2.grid(row=1, column=0)
        self.B_Temp3.grid(row=2, column=0)
        self.B_Temp4.grid(row=3, column=0)
        self.B_Temp5.grid(row=4, column=0)
        # Se detiene la ventana principal
        self.ventana3.grab_set()
        self.contenedor.wait_window(self.ventana3)

    # Método. Guardar
    # Método que almacena el archivo de texto en un archivo .txt
    def guardar(self):
        # Se obtiene todo el texto que se encuentra en el textArea/text
        texto = self.textArea1.get("1.0", END)
        # Se abre la ventana de diálogo para seleccionar la ubicación y el nombre del archivo a almacenar
        archivo = filedialog.asksaveasfilename(
            defaultextension='.txt', initialdir="/", title="Archivo")
        # Se intenta crear el archivo y escribir sobre él en la ruta obtenida
        try:
            with open(archivo, 'w') as f:
                f.write(texto)
            f.close()
        # En caso de obtener una excepción por no poder almacenar el archivo en la ruta especificada, se manda un mensaje de error
        except OSError:
            self.ubicacionInvalida()

    # Método. Borrar
    # Método que elimina lo almacenado en la ventana de texto
    def borrar(self):
        self.textArea1.delete("1.0", END)

    # Método. criterios (para el algoritmo Apriori)
    # Abre una ventana para ingresar los criterios que desee el usuario
    def criterios(self):
        # Especificaciones de ventana
        self.ventana2 = Toplevel()
        self.ventana2.resizable(0, 0)
        self.ventana2.title("Criterios: Algoritmo \"Apriori\"")
        # Elementos o componentes
        self.labelTemp1 = Label(self.ventana2, text="Confianza:")
        self.labelTemp2 = Label(self.ventana2, text="Soporte:")
        self.labelTemp3 = Label(self.ventana2, text="Lift:")
        self.labelTemp4 = Label(self.ventana2, text="Tamaño:")
        self.TF_Temp1 = Entry(self.ventana2, textvariable=self.confianza)
        self.TF_Temp2 = Entry(self.ventana2, textvariable=self.soporte)
        self.TF_Temp3 = Entry(self.ventana2, textvariable=self.lift)
        self.TF_Temp4 = Entry(self.ventana2, textvariable=self.tamano)
        self.buttonTemp1 = Button(self.ventana2, text="Aceptar", command=self.Apriori_completo)
        self.buttonTemp2 = Button(self.ventana2, text="Cerrar", command=self.ventana2.destroy)
        # Posicion
        self.labelTemp1.grid(row=0, column=0)
        self.labelTemp2.grid(row=1, column=0)
        self.labelTemp3.grid(row=2, column=0)
        self.labelTemp4.grid(row=3, column=0)
        self.TF_Temp1.grid(row=0, column=1, columnspan=2)
        self.TF_Temp2.grid(row=1, column=1, columnspan=2)
        self.TF_Temp3.grid(row=2, column=1, columnspan=2)
        self.TF_Temp4.grid(row=3, column=1, columnspan=2)
        self.buttonTemp1.grid(row=4, column=2)
        self.buttonTemp2.grid(row=4, column=0)
        # Se detiene la ventana principal
        self.ventana2.grab_set()
        self.contenedor.wait_window(self.ventana2)

    # Método. Parámetros inválidos
    # Ventana para el mensaje de error.
    def parametrosInvalidos(self):
        # Especificaciones de ventana
        self.ventana2 = Toplevel()
        self.ventana2.resizable(0, 0)
        self.ventana2.title("ERROR")
        # Elementos o componentes
        self.labelTemp1 = Label(
            self.ventana2, text="Error. Ingrese parámetros válidos.\nRevise la redacción.")
        self.button1 = Button(self.ventana2, text="Cerrar", command=self.ventana2.destroy)
        # Posicion
        self.labelTemp1.grid(row=0, column=0)
        self.button1.grid(row=1, column=0)
        # Se detiene la ventana principal
        self.ventana2.grab_set()
        self.contenedor.wait_window(self.ventana2)

    # Método. Ubicación inválida
    # Ventana para el mensaje de error.
    def ubicacionInvalida(self):
        # Especificaciones de ventana
        self.ventana2 = Toplevel()
        self.ventana2.resizable(0, 0)
        self.ventana2.title("ERROR")
        # Elementos o componentes
        self.labelTemp1 = Label(
            self.ventana2, text="Error en el sistema.\nNo se puede almacenar un archivo en esta dirección.")
        self.button1 = Button(self.ventana2, text="Cerrar", command=self.ventana2.destroy)
        # Posicion
        self.labelTemp1.grid(row=0, column=0)
        self.button1.grid(row=1, column=0)
        # Se detiene la ventana principal
        self.ventana2.grab_set()
        self.contenedor.wait_window(self.ventana2)

    # Método. Apriori
    # Método que invoca a la ventana de criterios para el algoritmo apriori
    def Apriori(self):
        self.criterios()

    # Método. Apriori completo
    # Método que realiza todo el algoritmo apriori e ingresa en la aplicación los resultados con base a los criterios establecidos por el usuario o por defecto
    def Apriori_completo(self):
        Resultados = []
        nombreArchivo = self.archivoRuta
        confianza = self.confianza.get()
        soporte = self.soporte.get()
        lift = self.lift.get()
        tamano = self.tamano.get()
        # Se determina el tipo de archivo
        tipo = nombreArchivo.split('.')[1]
        # Se determina si es un archivo .txt
        if (tipo == 'txt'):
            # Se leen los datos
            Datos = pd.read_table(nombreArchivo, header=None)
        elif (tipo == 'xlsx'):
            # Se leen los datos
            Datos = pd.read_excel(nombreArchivo, header=None)
        elif (tipo == 'csv'):
            # Se leen los datos
            Datos = pd.read_csv(nombreArchivo, header=None)
        # Se determina el número de filas y de columnas
        filas, columnas = FilasYColumnas(Datos)
        # Se determinan las transacciones realizadas
        Transacciones = []
        for i in range(0, filas):
            Transacciones.append([str(Datos.values[i, j]) for j in range(0, columnas)])
        # Se aplica el algoritmo apriori
        Reglas = apriori(Transacciones, min_support=soporte,
                         min_confidence=confianza, min_lift=lift, min_length=tamano)
        # Se retornan los resultados
        Resultados = list(Reglas)
        self.textArea1.insert(END, ".: Reglas de asociación :.\n")
        for item in Resultados:
            # Primer índice de la lista interna
            # Contiene un elemento agrega otro
            pair = item[0]
            items = [x for x in pair]
            self.textArea1.insert(END, "Regla: " + items[0] + "->" + items[1] + "\n")
            # Segundo índice de la lista interna
            self.textArea1.insert(END, "Soporte: " + str(item[1]) + "\n")
            # Tercer índice de la lista interna
            self.textArea1.insert(END, "Confianza: " + str(item[2][0][2]) + "\n")
            self.textArea1.insert(END, "Lift: " + str(item[2][0][3]) + "\n")
            self.textArea1.insert(END, "=====================================\n")
            self.textArea1.see(END)

    # Método. Correlación
    # Método para obtener la correlación de los datos
    def correlacional(self):
        nombreArchivo = self.archivoRuta
        tipo = nombreArchivo.split('.')[1]
        # Se determina si es un archivo .txt
        if (tipo == 'txt'):
            # Se leen los datos
            self.datos = pd.read_table(nombreArchivo)
        elif (tipo == 'xlsx'):
            # Se leen los datos
            self.datos = pd.read_excel(nombreArchivo)
        elif (tipo == 'csv'):
            # Se leen los datos
            self.datos = pd.read_csv(nombreArchivo)
        # Se obtiene la matriz de correlación
        self.MCorrelaciones = self.datos.corr(method='pearson')
        # Se inserta la matriz en el área de texto
        self.textArea1.insert(END, self.MCorrelaciones)
        # Se llama a mandar la función graficar para hacer que el usuario decida los parámetros
        self.graficar()

    # Método. graficar
    # Método para realizar la graficación de la correlación de datos
    def graficar(self):
        # Especificaciones de ventana
        self.ventana5 = Toplevel()
        self.ventana5.resizable(0, 0)
        self.ventana5.title("Correlación")
        # Elementos o componentes
        self.l1 = Label(self.ventana5, text="Parámetro 1:")
        self.l2 = Label(self.ventana5, text="Parámetro 2:")
        self.e1 = Entry(self.ventana5, textvariable=self.cadena1)
        self.e2 = Entry(self.ventana5, textvariable=self.cadena2)
        self.b1 = Button(self.ventana5, text="Cerrar", command=self.ventana5.destroy)
        self.b2 = Button(self.ventana5, text="Graficar", command=self.relacion)
        # Posición
        self.l1.grid(row=0, column=0)
        self.l2.grid(row=1, column=0)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.b1.grid(row=2, column=0)
        self.b2.grid(row=2, column=1)
        # Se detiene la ventana principal
        self.ventana5.grab_set()
        self.contenedor.wait_window(self.ventana5)

    # Método. Relación
    # Método que permite graficar la correlación de los datos
    def relacion(self):
        # Se intenta, si no hay errores con los parámetros, se abre una ventana para graficar
        try:
            # Especificaciones de ventana
            self.ventana4 = Toplevel()
            self.ventana4.resizable(0, 0)
            self.ventana4.title("Correlación")
            # Elementos o componentes para graficar valores
            figura = Figure(figsize=(5, 4), dpi=100)
            # Si no se encuentra valor en los entry/textField, se grafica la matriz de correlaciones
            if(self.cadena1.get() == '' and self.cadena2.get() == ''):
                figura.add_subplot(111).matshow(self.MCorrelaciones)
            # En caso contrario se grafica la relación entre los dos parámetros dados por el usario
            else:
                figura.add_subplot(111).plot(
                    self.datos[self.cadena1.get()], self.datos[self.cadena2.get()], 'g*')
            canvas = FigureCanvasTkAgg(figura, master=self.ventana4)
            canvas.draw()
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            # Elementos o componentes para la manipulación de la aplicación
            self.B1 = Button(self.ventana4, text="cerrar", command=self.ventana4.destroy)
            self.B1.pack(side=BOTTOM)
        # Si ocurre una excepción de argumento inválido para los datos, se destruye la ventana creada y se muestra el mensaje de erro.
        except KeyError:
            self.ventana4.destroy()
            self.parametrosInvalidos()

    # Métricas de similitud
    def metricas(self):
        # Especificaciones de ventana
        self.ventana4 = Toplevel()
        self.ventana4.resizable(0, 0)
        self.ventana4.title("Similitud de similitud")
        # Componentes
        self.b1 = Button(self.ventana4, text="Distancia euclidiana", command=self.euclidiana)
        self.b2 = Button(self.ventana4, text="Distancia de Chebyshev", command=self.chebyshev)
        self.b3 = Button(self.ventana4, text="Distancia de Manhattan", command=self.manhattan)
        self.b4 = Button(self.ventana4, text="Distancia de Minkowski", command=self.minkowski)
        self.b5 = Button(self.ventana4, text="Cerrar", command=self.ventana4.destroy)
        # Posición
        self.b1.grid(row=0, column=0)
        self.b2.grid(row=1, column=0)
        self.b3.grid(row=2, column=0)
        self.b4.grid(row=3, column=0)
        self.b5.grid(row=4, column=0)
        # Precedencia
        self.ventana4.grab_set()
        self.contenedor.wait_window(self.ventana4)

    # Distancia euclidiana
    def euclidiana(self):
        # Se determina el tipo de archivo
        tipo = self.archivoRuta.split('.')[1]
        # Se determina si es un archivo .txt
        if (tipo == 'txt'):
            # Se leen los datos
            Datos = pd.read_table(self.archivoRuta, header=None)
        elif (tipo == 'xlsx'):
            # Se leen los datos
            Datos = pd.read_excel(self.archivoRuta, header=None)
        elif (tipo == 'csv'):
            # Se leen los datos
            Datos = pd.read_csv(self.archivoRuta, header=None)
        # Se elimina la primer fila que contiene registros de tipo cadena
        Datos = Datos.drop(0)
        # Se determina el número de filas y de columnas
        filas, columnas = FilasYColumnas(Datos)
        # Se crea el data frame de dimensión filasxfilas
        Data = {}
        for i in range(0, filas):
            Lista = []
            for j in range(0, filas):
                Lista.append('--')
            Data[i] = Lista
        # El data frame en cada registro tiene el valor '--'
        matrizSimilitudes = pd.DataFrame(data=Data)
        # Se realiza la matriz de similitudes
        for i in range(0, filas):
            # Con base a la fila de la que se quiera obtener la distancias
            # Se obtiene las distancias con las filas anteriores
            for j in range(0, i+1):
                # Se utilizan los datos del DataFrame que se desea
                # cuyos valores son de tipo str (String,cadena)
                E1 = Datos.iloc[i]
                E2 = Datos.iloc[j]
                # Se implementan variables auxiliares para almacenar
                # el valor de los registros en valores de tipo int (integer,entero)
                E1Temp = []
                E2Temp = []
                # Por cada registro en se intenta hacer un casteo y almacenarlo
                # en las variables auxiliares, en caso caso de que ocurra una expeción
                # el valor no se almacena debido a que solo se requieren valores númericos
                for k in range(0, len(E1)):
                    try:
                        E1Temp.append(int(E1[k]))
                    except ValueError:
                        pass
                for k in range(0, len(E2)):
                    try:
                        E2Temp.append(int(E2[k]))
                    except ValueError:
                        pass
                # Se calcula la distancia euclidiana
                dist = "{0:.5f}".format(
                    sqrt(sum((E1Temp-E2Temp)**2 for E1Temp, E2Temp in zip(E1Temp, E2Temp))))
                # La distancia se almacena en el DataFrame de similitudes
                # matrizSimilitudes.iloc[j, i] = dist # Descomentar para obtener Matriz completa
                matrizSimilitudes.iloc[i, j] = dist  # Matriz diagonal inferior
        # Impresión en la caja de texto de la GUI
        self.textArea1.insert(
            END, "\n.: METRICAS DE SIMILITUD :.\n.: Distancia euclidiana :.\n")
        self.textArea1.insert(END, matrizSimilitudes)
        self.textArea1.insert(END, '\n')
    # Distancia chebyshev

    def chebyshev(self):
        # Se determina el tipo de archivo
        tipo = self.archivoRuta.split('.')[1]
        # Se determina si es un archivo .txt
        if (tipo == 'txt'):
            # Se leen los datos
            Datos = pd.read_table(self.archivoRuta, header=None)
        elif (tipo == 'xlsx'):
            # Se leen los datos
            Datos = pd.read_excel(self.archivoRuta, header=None)
        elif (tipo == 'csv'):
            # Se leen los datos
            Datos = pd.read_csv(self.archivoRuta, header=None)
        # Se determina el número de filas y de columnas
        Datos = Datos.drop(0)
        filas, columnas = FilasYColumnas(Datos)
        # Se crea el data frame
        Data = {}
        for i in range(0, filas):
            Lista = []
            for j in range(0, filas):
                Lista.append('--')
            Data[i] = Lista
        matrizSimilitudes = pd.DataFrame(data=Data)
        # Se realiza la matriz de similitudes
        for i in range(0, filas):
            for j in range(0, i+1):
                E1 = Datos.iloc[i]
                E2 = Datos.iloc[j]
                E1Temp = []
                E2Temp = []
                for k in range(0, len(E1)):
                    try:
                        E1Temp.append(int(E1[k]))
                    except ValueError:
                        pass
                for k in range(0, len(E2)):
                    try:
                        E2Temp.append(int(E2[k]))
                    except ValueError:
                        pass
                dist = distance.chebyshev(E1Temp, E2Temp)
                # matrizSimilitudes.iloc[j, i] = dist
                matrizSimilitudes.iloc[i, j] = dist
        self.textArea1.insert(
            END, "\n.: METRICAS DE SIMILITUD :.\n.: Distancia de Chebyshev :.\n")
        self.textArea1.insert(END, matrizSimilitudes)
        self.textArea1.insert(END, '\n')

    # Distancia manhattan
    def manhattan(self):
        # Se determina el tipo de archivo
        tipo = self.archivoRuta.split('.')[1]
        # Se determina si es un archivo .txt
        if (tipo == 'txt'):
            # Se leen los datos
            Datos = pd.read_table(self.archivoRuta, header=None)
        elif (tipo == 'xlsx'):
            # Se leen los datos
            Datos = pd.read_excel(self.archivoRuta, header=None)
        elif (tipo == 'csv'):
            # Se leen los datos
            Datos = pd.read_csv(self.archivoRuta, header=None)
        # Se determina el número de filas y de columnas
        Datos = Datos.drop(0)
        filas, columnas = FilasYColumnas(Datos)
        # Se crea el data frame
        Data = {}
        for i in range(0, filas):
            Lista = []
            for j in range(0, filas):
                Lista.append('--')
            Data[i] = Lista
        matrizSimilitudes = pd.DataFrame(data=Data)
        # Se realiza la matriz de similitudes
        for i in range(0, filas):
            for j in range(0, i+1):
                E1 = Datos.iloc[i]
                E2 = Datos.iloc[j]
                E1Temp = []
                E2Temp = []
                for k in range(0, len(E1)):
                    try:
                        E1Temp.append(int(E1[k]))
                    except ValueError:
                        pass
                for k in range(0, len(E2)):
                    try:
                        E2Temp.append(int(E2[k]))
                    except ValueError:
                        pass
                dist = distance.cityblock(E1Temp, E2Temp)
                # matrizSimilitudes.iloc[j, i] = dist
                matrizSimilitudes.iloc[i, j] = dist
        self.textArea1.insert(
            END, "\n.: METRICAS DE SIMILITUD :.\n.: Distancia de Manhattan :.\n")
        self.textArea1.insert(END, matrizSimilitudes)
        self.textArea1.insert(END, '\n')

    # Distancia minkowski
    def minkowski(self):
        # Se determina el tipo de archivo
        tipo = self.archivoRuta.split('.')[1]
        # Se determina si es un archivo .txt
        if (tipo == 'txt'):
            # Se leen los datos
            Datos = pd.read_table(self.archivoRuta, header=None)
        elif (tipo == 'xlsx'):
            # Se leen los datos
            Datos = pd.read_excel(self.archivoRuta, header=None)
        elif (tipo == 'csv'):
            # Se leen los datos
            Datos = pd.read_csv(self.archivoRuta, header=None)
        # Se determina el número de filas y de columnas
        Datos = Datos.drop(0)
        filas, columnas = FilasYColumnas(Datos)
        # Se crea el data frame
        Data = {}
        for i in range(0, filas):
            Lista = []
            for j in range(0, filas):
                Lista.append('--')
            Data[i] = Lista
        matrizSimilitudes = pd.DataFrame(data=Data)
        # Se realiza la matriz de similitudes
        for i in range(0, filas):
            for j in range(0, i+1):
                E1 = Datos.iloc[i]
                E2 = Datos.iloc[j]
                E1Temp = []
                E2Temp = []
                for k in range(0, len(E1)):
                    try:
                        E1Temp.append(int(E1[k]))
                    except ValueError:
                        pass
                for k in range(0, len(E2)):
                    try:
                        E2Temp.append(int(E2[k]))
                    except ValueError:
                        pass
                dist = "{0:.5f}".format(distance.minkowski(E1Temp, E2Temp))
                # matrizSimilitudes.iloc[j, i] = dist
                matrizSimilitudes.iloc[i, j] = dist
        self.textArea1.insert(
            END, "\n.: METRICAS DE SIMILITUD :.\n.: Distancia de Minkowski :.\n")
        self.textArea1.insert(END, matrizSimilitudes)
        self.textArea1.insert(END, '\n')

    # Clustering particional
    def clustering(self):
        self.ventana6 = Toplevel()
        self.ventana6.title("Clustering particional")
        # Elementos o Componentes
        self.listbox = Listbox(self.ventana6, selectmode=EXTENDED)
        self.bc0 = Button(self.ventana6, text="Seleccionar variables:",
                          command=self.agregarElementos)
        self.bc1 = Button(self.ventana6, text="Clustering",
                          state=DISABLED, command=self.clusteringP)
        self.bc2 = Button(self.ventana6, text="Cerrar", command=self.ventana6.destroy)
        # Posición de los elementos
        self.bc0.grid(row=0, column=0)
        self.listbox.grid(row=1, column=0)
        self.bc1.grid(row=1, column=1)
        self.bc2.grid(row=2, column=1)
        # Se detiene la ventana principal
        self.ventana6.grab_set()
        self.contenedor.wait_window(self.ventana6)

    # Agregar elementos al listbox de la ventana clustering
    def agregarElementos(self):
        nombreArchivo = self.archivoRuta
        tipo = nombreArchivo.split('.')[1]
        # Se determina si es un archivo .txt
        if (tipo == 'txt'):
            # Se leen los datos
            datos = pd.read_table(nombreArchivo)
        elif (tipo == 'xlsx'):
            # Se leen los datos
            datos = pd.read_excel(nombreArchivo)
        elif (tipo == 'csv'):
            # Se leen los datos
            datos = pd.read_csv(nombreArchivo)
        self.listaClustering = []
        for column in datos:
            self.listaClustering.append(column)
        self.listbox.insert(0, *self.listaClustering)
        self.bc1.config(state=ACTIVE)

    # Método que realiza el clustering particional
    def clusteringP(self):
        elemento = self.listbox.curselection()
        elementos = []
        for i in elemento:
            elementos.append(i)
        nombreArchivo = self.archivoRuta
        tipo = nombreArchivo.split('.')[1]
        # Se determina si es un archivo .txt
        if (tipo == 'txt'):
            # Se leen los datos
            datos = pd.read_table(nombreArchivo)
        elif (tipo == 'xlsx'):
            # Se leen los datos
            datos = pd.read_excel(nombreArchivo)
        elif (tipo == 'csv'):
            # Se leen los datos
            datos = pd.read_csv(nombreArchivo)
        self.variablesModelo = datos.iloc[:, elementos].values
        self.SSE = []
        # Rango referencial
        for i in range(2, 16):
            kn = KMeans(n_clusters=i, random_state=1)  # Se recomineda un aleatorio 0 o 1
            kn.fit(self.variablesModelo)
            self.SSE.append(kn.inertia_)
        # Se grafica el codo
        self.graficarCodo()
        # Se crean los clustersfrom kneed import KneeLocator
        k1 = KneeLocator(range(2, 16), self.SSE, curve="convex", direction="decreasing")
        self.textArea1.insert(
            END, "\n.: Clustering particional. Número de cluster recomendado :.\n")
        self.textArea1.insert(END, k1.elbow)
        self.textArea1.insert(END, "\n")
        # random_state se utiliza para inicializar el generador interno de números aleatorios (mismo resultado)
        self.MParticional = KMeans(n_clusters=k1.elbow, random_state=0).fit(self.variablesModelo)
        self.MParticional.predict(self.variablesModelo)
        datos['clusterP'] = self.MParticional.labels_
        # Se inserta en la GUI la nueva tabla con los clusters
        self.textArea1.insert(END, "\n.: Cluster particional :.\n")
        self.textArea1.insert(END, datos)
        self.textArea1.insert(END, '\n')
        # Se mencionan la cantidad de miembros que tiene cada cluster
        self.textArea1.insert(END, "\n.: Cluster particional. Elementos por cada cluster :.\n")
        self.textArea1.insert(END, datos.groupby(['clusterP'])['clusterP'].count())
        self.textArea1.insert(END, '\n')
        # Especificaciones de los clusters
        self.CentroidesP = self.MParticional.cluster_centers_
        # Se grafican los centroides
        self.graficarCentroides()
        # Se muestran las especificaciones de cada cluster
        clusterNames = []
        for i in range(0, len(elemento)):
            clusterNames.append(self.listaClustering[elemento[i]])
        df = pd.DataFrame(self.CentroidesP.round(4), columns=clusterNames)
        self.textArea1.insert(
            END, "\n.: Cluster particional. Especificaciones para cada cluster :.\n")
        self.textArea1.insert(END, df)
        self.textArea1.insert(END, '\n')
        # Se identifica a las varibles más cercanas con respecto a cada centroide
        Cercanos, _ = pairwise_distances_argmin_min(
            self.MParticional.cluster_centers_, self.variablesModelo)
        # Se imprimen las valores
        cercanos2 = datos.iloc[:, 0].values
        self.textArea1.insert(
            END, "\n.: Cluster particional. Elementos cercanos a cada cluster :.\n")
        i = 0
        for row in Cercanos:
            self.textArea1.insert(END, "Cluster {}: {}".format(i, cercanos2[row]))
            self.textArea1.insert(END, '\n')
            i = i + 1

    # Método para visualizar el codo aproximado
    def graficarCodo(self):
        # Se intenta, si no hay errores con los parámetros, se abre una ventana para graficar
        try:
            # Especificaciones de ventana
            self.ventana4 = Toplevel()
            self.ventana4.resizable(0, 0)
            self.ventana4.title("Correlación")
            # Elementos o componentes para graficar valores
            figura = Figure(figsize=(5, 4), dpi=100)
            figura.add_subplot(111).plot(range(2, 16), self.SSE, marker='o')
            canvas = FigureCanvasTkAgg(figura, master=self.ventana4)
            canvas.draw()
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            # Elementos o componentes para la manipulación de la aplicación
            self.B1 = Button(self.ventana4, text="cerrar", command=self.ventana4.destroy)
            self.B1.pack(side=BOTTOM)
        # Si ocurre una excepción de argumento inválido para los datos, se destruye la ventana creada y se muestra el mensaje de erro.
        except:
            self.ventana4.destroy()

    # Método para graficar centroides
    def graficarCentroides(self):
        try:
            # Especificaciones de ventana
            self.ventana5 = Toplevel()
            self.ventana5.resizable(0, 0)
            self.ventana5.title("Clusters")
            # Elementos o componentes para graficar valores
            figura = Figure(figsize=(5, 4), dpi=100)
            colores = ['blue', 'red', 'cyan', 'green', 'yellow']
            asignar = []
            for row in self.MParticional.labels_:
                asignar.append(colores[row])
            ax = Axes3D(figura)
            ax.scatter(self.variablesModelo[:, 0], self.variablesModelo[:, 1],
                       self.variablesModelo[:, 2], marker='+', c=asignar, s=60)
            ax.scatter(self.CentroidesP[:, 0], self.CentroidesP[:, 1],
                       self.CentroidesP[:, 2], marker='*', c=colores, s=1000)
            #figura.add_subplot(111).plot(range(2, 16), self.SSE, marker='o')
            canvas = FigureCanvasTkAgg(figura, master=self.ventana5)
            canvas.draw()
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            # Elementos o componentes para la manipulación de la aplicación
            self.B1 = Button(self.ventana5, text="cerrar", command=self.ventana5.destroy)
            self.B1.pack(side=BOTTOM)
        # Si ocurre una excepción de argumento inválido para los datos, se destruye la ventana creada y se muestra el mensaje de erro.
        except:
            self.ventana5.destroy()

    # Método para abrir la ventana de diagnóstico
    def diagnostico(self):
        self.ventana7 = Toplevel()
        self.ventana7.title("Cancer diagnosis")
        self.ventana7.resizable(0, 0)
        # Variables
        self.id = IntVar()
        self.texture = DoubleVar()
        self.area = DoubleVar()
        self.compactness = DoubleVar()
        self.concavity = DoubleVar()
        self.symmetry = DoubleVar()
        self.fractalDimension = DoubleVar()
        self.diagnosis = StringVar()
        # Componentes
        self.l1 = Label(self.ventana7, text="ID patient")
        self.l2 = Label(self.ventana7, text="Texture")
        self.l3 = Label(self.ventana7, text="Area")
        self.l4 = Label(self.ventana7, text="Compactness")
        self.l5 = Label(self.ventana7, text="Concavity")
        self.l6 = Label(self.ventana7, text="Symmetry")
        self.l7 = Label(self.ventana7, text="Fractal Dimension")
        self.l8 = Label(self.ventana7, text="Diagnosis")
        self.b1 = Button(self.ventana7, text="Diagnose", command=self.prediccion)
        self.tf1 = Entry(self.ventana7, textvariable=self.id)
        self.tf2 = Entry(self.ventana7, textvariable=self.texture)
        self.tf3 = Entry(self.ventana7, textvariable=self.area)
        self.tf4 = Entry(self.ventana7, textvariable=self.compactness)
        self.tf5 = Entry(self.ventana7, textvariable=self.concavity)
        self.tf6 = Entry(self.ventana7, textvariable=self.symmetry)
        self.tf7 = Entry(self.ventana7, textvariable=self.fractalDimension)
        self.tf8 = Entry(self.ventana7, textvariable=self.diagnosis)
        # Posición
        self.l1.grid(row=0, column=2)
        self.l2.grid(row=1, column=0)
        self.l3.grid(row=2, column=0)
        self.l4.grid(row=3, column=0)
        self.l5.grid(row=1, column=4)
        self.l6.grid(row=2, column=4)
        self.l7.grid(row=3, column=4)
        self.l8.grid(row=5, column=2)
        self.tf1.grid(row=0, column=3)
        self.tf2.grid(row=1, column=1)
        self.tf3.grid(row=2, column=1)
        self.tf4.grid(row=3, column=1)
        self.tf5.grid(row=1, column=5)
        self.tf6.grid(row=2, column=5)
        self.tf7.grid(row=3, column=5)
        self.tf8.grid(row=5, column=3)
        self.b1.grid(row=4, column=5)
        # Se detiene la ventana principal
        self.ventana7.grab_set()
        self.contenedor.wait_window(self.ventana7)

    # Método para hacer la predicción del diagnóstico
    def prediccion(self):
        P = 11.72 - 0.19*self.texture.get() - 0.01*self.area.get() - 2.27*self.compactness.get() - \
            3.08*self.concavity.get() - 0.88*self.symmetry.get() - 0.21*self.fractalDimension.get()
        probabilidad = 1/(1+np.exp(P))
        if(probabilidad < 0.5):
            self.diagnosis.set("Benign tumor")
        elif(probabilidad > 0.5):
            self.diagnosis.set("Malignant tumor")
        else:
            self.diagnosis.set("Incomplete")
        self.textArea1.insert(END, "\n.: DIAGNÓSTICO :.\nID Paciente: {}\nTextura: {}\nConcavidad: {}\nArea: {}\nSimetría: {}\nCompacidad: {}\nDimensión fractal: {}\nDiagnóstico: {}".format(self.id.get(),
                                                                                                                                                                                              self.texture.get(), self.concavity.get(), self.area.get(), self.symmetry.get(), self.compactness.get(), self.fractalDimension.get(), self.diagnosis.get()))
        self.textArea1.insert(END, '\n')
        self.textArea1.see(END)


##########################################################################################################
# Programa princial
# Se crea una ventana para decidir si hace un análisis clínico para el cáncer de un paciente o el análisis de datos
ventana = Tk()
# Título de la ventana: "Inteligencia Artificial"
ventana.title("Inteligencia Artificial")
# Impide que la ventana sea redimensionable
ventana.resizable(width=0, height=0)
# Se crea el objeto Aplicación
Aplicacion = Aplicacion(ventana)
# Se mantiene activa la aplicación
ventana.mainloop()
##########################################################################################################
