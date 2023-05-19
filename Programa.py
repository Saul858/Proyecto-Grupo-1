import pandas as pd #libreria para el analisis y estructura de datos, lee csv,excel y bd sql
import numpy as np #libreria par calculos numericos, arrays, vectores, matrices
import matplotlib.pyplot as plt # libreria para personalizar graficos, diagramas de barras, histogramas
from tkinter import * #proporciona herramientas para administrar ventanas de dialogs
from tkinter import filedialog
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px

root = Tk()
root.geometry("400x400")

label1 = Label(root, text="CSV File Path")
label1.pack()

entry1 = Entry(root)
entry1.pack()

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("CSV files", "*.csv*"), ("all files", "*.*")))
    entry1.insert(END, filename)

button1 = Button(root, text="Browse", command=browseFiles)
button1.pack()

def importCSV():
    path = entry1.get()
    df = pd.read_csv(path, sep = ';', decimal = ',')
    print(df)
    df.to_pickle(r'C:\Users\bryan\OneDrive\Documentos1\Proyecto GCS\df_importado.plk')

# SAVE df to 

button2 = Button(root, text="Import CSV", command=importCSV)
button2.pack()

button3 = Button(root, text="Finalizar", command=root.destroy)
button3.pack()

root.mainloop()

app = dash.Dash()
application = app.server
# read the pickle file
df= pd.read_pickle(r'C:\Users\bryan\OneDrive\Documentos1\Proyecto GCS\df_importado.plk')
df.head()
app.layout = html.Div([
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='price'
    ),
    html.Div(id='stats-output')
])

@app.callback(
    Output('stats-output', 'children'),
    [Input('column-dropdown', 'value')]
)
def update_output(column):
    stats = df[column].describe()
    fig = px.histogram(df, x=column)
    return [
        html.H4(f'Descriptive Statistics for {column}'),
        dash_table.DataTable(
            data=stats.to_frame().reset_index().to_dict('records'),
            columns=[{'name': i, 'id': i} for i in ['index', column]]
        ),
        dcc.Graph(figure=fig)
    ]

if __name__ == '__main__':
    application.run(debug=False, port=8080)