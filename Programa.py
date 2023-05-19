import pandas as pd #libreria para el analisis y estructura de datos, lee csv,excel y bd sql
import numpy as np #libreria par calculos numericos, arrays, vectores, matrices
import matplotlib.pyplot as plt # libreria para personalizar graficos, diagramas de barras, histogramas
from tkinter import * #proporciona herramientas para administrar ventanas de dialogos, * es para jalar todas las funciones
from tkinter import filedialog #Es para cargr una funcion especifica
import dash #Libreria para crear dashboards
import dash_core_components as dcc #Carga la funcion de dash para los componentes del dashboard
import dash_html_components as html #Funicona para que se cree la aplicación web
import dash_table #Funciona para crear tablas en dash
from dash.dependencies import Input, Output, State #Funciona para los elementos el dash
import plotly.express as px #Funciona para crear los gráficos

root = Tk() #Funcion Tk hace el cuadro emergente 
root.geometry("400x400") #define el tamaño del cuadro

label1 = Label(root, text="CSV File Path Equipo 1") #Funcion para crear el titulo 
label1.pack() #Se utiliza para agregar el titulo al cuadro y mostrar en la pantalla

entry1 = Entry(root) #funcion para crear el cuadro en blanco donde ingresar texto del path 
entry1.pack() #agrega el cuadro blanco 

def browseFiles(): #desarrolla la funcion de crear el path del archivo seleccionado
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("CSV files", "*.csv*"), ("all files", "*.*"))) #funcion para dar instruccion de que archivos y retorna la dirección del archivo seleccionado, se puede cargar CSV u otros archivos ya que tiene esta opción también
    entry1.insert(END, filename) #inserta la direccion en el objeto en blanco
 
button1 = Button(root, text="Browse", command=browseFiles) #funcion para crear boton browse
button1.pack() #inserta boton en el cuadro 

def importCSV(): #Funcion para importar el CSV
    path = entry1.get() #extrae la direccion del CSV del entry1
    df = pd.read_csv(path, sep = ';', decimal = ',') #lee el CSV y aqui modifico los separadores 
    print(df) #print del CSV
    df.to_pickle(r'Descargas\df_importado.plk') #guarda el archivo en formato plk


button2 = Button(root, text="Import CSV", command=importCSV) #Boton para la funcion importCSV
button2.pack() #inserta el boton

button3 = Button(root, text="Finalizar", command=root.destroy) #boton para la funcion finalizar (ya tiene incorporada la funcion)
button3.pack() #inserta el boton 

root.mainloop() #ejecuta todas las funciones anteriores

app = dash.Dash() #crea el dashboard en blanco
application = app.server #crea el servidor web del dashboard
# read the pickle file
df= pd.read_pickle(r'Descargas\df_importado.plk') #se vuelve a llamar el archivo plk
df.head() #imprime las primera 5 filas (se puede agregar la cantidad que desee ver en los parentesis)
app.layout = html.Div([ #le da diseño y estructura fisica HTML al dashboard, se compone por la
    dcc.Dropdown( #crea la lista desplegable 
        id='column-dropdown', #parte de los parametros del dropdown
        options=[{'label': col, 'value': col} for col in df.columns], #agrega las columnas de las opciones
        value='price' #columna que aparece por defecto
    ),
    html.Div(id='stats-output') #contenedor donde se encuentra el analisis descriptivo
])

@app.callback( #forma parte del dashboard, muestra lo seleccionado del dropdown
    Output('stats-output', 'children'),
    [Input('column-dropdown', 'value')]
)
def update_output(column): #forma parte del dashboard, se da las instrucciones de lo que se desea ver
    stats = df[column].describe() #funcion para mostrar diferentes los minimos, maximos, promedio
    fig = px.histogram(df, x=column)
    return [
        html.H4(f'Descriptive Statistics for {column}'), #crea el titulo para el cuadro de estadisticas
        dash_table.DataTable(
            data=stats.to_frame().reset_index().to_dict('records'), #
            columns=[{'name': i, 'id': i} for i in ['index', column]]
        ),
        dcc.Graph(figure=fig) #grafico
    ]

if __name__ == '__main__': #ejecuta todas las funciones del dashboard
    application.run(debug=False, port=8080)