import csv
import heapq
import numpy as np
import graphviz as gv
import math
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

#-------------------------------------------------------- Logica del programa para encontrar canciones ---------------------------------------------------------------------------------

#Getting the list of the names from the dataset
artistsList = {}
nameList = []
def getNameList():
    csv_file = csv.reader(open('Spotify-2000.csv', 'r'))
    next(csv_file)
    for lines in csv_file:
        nameList.append(lines[1])
        artistsList[lines[1]] = lines[2]

#Getting the list of the edges from the .csv file created
songsRelations = []
def readCsvFile():
    csv_file = csv.reader(open('aristasWeighted.csv', 'r'), delimiter=';')
    next(csv_file)
    for lines in csv_file:
        songsRelations.append([lines[0],lines[1],lines[2]])


#Implement prim algorithm, modified to return the mst_tree instead of the min weight
def prim_mst(graph, quantity_nodes, nodo_inicial=0):
    priority_queue = []
    visited = [False] * (quantity_nodes)
    min_weight = 0
    mst_edges = []
    mst_tree = []
    #max_quantity = 100
    counter = 0

    heapq.heappush(priority_queue, (0, nodo_inicial))
    
    while len(priority_queue) > 0:
        weight, to = heapq.heappop(priority_queue)
        
        if visited[to]:
            continue

        visited[to] = True

        if to != nodo_inicial:
            mst_edges.append((to, weight))

        min_weight += weight

        for neighbour in graph[to]:
            if visited[neighbour[0]]:
                continue
            heapq.heappush(priority_queue, (neighbour[1], neighbour[0]))

    #sets the mst_tree with a max of 10 songs
    for edge in mst_edges:
        #if counter < max_quantity:
        mst_tree.append([edge[0], edge[1]])
        #counter += 1
        
    return mst_tree

#converting the mst_tree to a list of the songs recommended

def get_songs(songsRecomended, songList):
    songsRecomendedName = []
    for i in range(len(songsRecomended)):
        for key, val in songList.items():
            if val == songsRecomended[i][0]:
                songsRecomendedName.append(key)
    return songsRecomendedName

#read the .csv files
readCsvFile()
getNameList()

#get the # of edges and nodes
nAristas = len(songsRelations)
nDataSet = len(nameList)

#setting a dictionary of the nodes
songsList = {}
for i in range(0,nDataSet-1):
    songsList[nameList[i]] = i

#converting the list of the edges on a graph
newSongsRelations = []
a = -1
b = -1
for i in range(nAristas):
    for j in range(nDataSet):
        if a == -1 and nameList[j] == songsRelations[i][0]:
            a = j
        if nameList[j] == songsRelations[i][1]:
            b = j
        if a != -1 and b != -1:
            newSongsRelations.append([a,b,float(songsRelations[i][2])])
            a = -1
            b = -1
            break
graph = [[] for _ in range(len(newSongsRelations))]
for i in range(len(newSongsRelations)):
    graph[newSongsRelations[i][0]].append((newSongsRelations[i][1],(newSongsRelations[i][2])))
    graph[newSongsRelations[i][1]].append((newSongsRelations[i][0],(newSongsRelations[i][2])))

## Método para gráficar el grafo
def drawGraph(G, directed=False, weighted=False, path=[], layout="neato"):
  graph = gv.Digraph("digrafo") if directed else gv.Graph("grafo")
  graph.graph_attr["layout"] = layout
  graph.edge_attr["color"] = "gray"
  graph.node_attr["color"] = "orangered"
  graph.node_attr["width"] = "0.1"
  graph.node_attr["height"] = "0.1"
  graph.node_attr["fontsize"] = "8"
  graph.node_attr["fontcolor"] = "mediumslateblue"
  graph.node_attr["fontname"] = "monospace"
  graph.edge_attr["fontsize"] = "8"
  graph.edge_attr["fontname"] = "monospace"
  n = len(G)
  added = set()
  for v, u in enumerate(path):
    if u != -1:
      if weighted:
        graph.edge(str(u), str(v), str(G[u, v]), dir="forward", penwidth="2", color="orange")
      else:
        graph.edge(str(u), str(v), dir="forward", penwidth="2", color="orange")
      added.add(f"{u},{v}")
      added.add(f"{v},{u}")
  for u in range(n):
    for v in range(n):
      draw = False
      if G[u, v] > 0 and not directed and not f"{u},{v}" in added:
        added.add(f"{u},{v}")
        added.add(f"{v},{u}")
        draw = True
      elif directed:
        draw = True
      if draw:
        if weighted:
          graph.edge(str(u), str(v), str(G[u, v]))
        else:
          graph.edge(str(u), str(v))
  return graph


#-------------------------------------------------------- Logica del programa para crear la GUI ---------------------------------------------------------------------------------

# Copiar la ruta de los assets del build para que el programa pueda correr, version portable en progreso
OUTPUT_PATH = Path(__file__).parent 
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\STEVENS\Desktop\CARPETAS\CLASES-UPC\CICLOS\Ciclo-6\Cursos\Comple\trabajo\TF\EchoFusion\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.geometry("700x800")
window.configure(bg = "#FFFFFF")

# Crear el Canvas o el Frame
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 800,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

# Crear los elementos visuales 
canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    700.0,
    78.0,
    fill="#3DCBEA",
    outline="")

canvas.create_text(
    250.0,
    7.0,
    anchor="nw",
    text="EchoFusion",
    fill="#FFFFFF",
    font=("Inika Bold", 32 * -1)
)

canvas.create_text(
    162.0,
    48.0,
    anchor="nw",
    text="¡Genera tus playlists a partir de tu canción favorita! ",
    fill="#FFFFFF",
    font=("Inika", 14 * -1)
)

canvas.create_text(
    70.0,
    95.0,
    anchor="nw",
    text="Título de una canción:",
    fill="#000000",
    font=("Inika", 14 * -1)
)

canvas.create_text(
    70.0,
    134.0,
    anchor="nw",
    text="Artista a descartar:",
    fill="#000000",
    font=("Inika", 14 * -1)
)

canvas.create_text(
    42.0,
    234.0,
    anchor="nw",
    text="Playlist generada:",
    fill="#000000",
    font=("Inika", 14 * -1)
)

canvas.create_text(
    42.0,
    406.0,
    anchor="nw",
    text="Grafo:",
    fill="#000000",
    font=("Inika", 14 * -1)
)

# Cuadro para ingresar nombre de alguna cancion
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    389.5,
    107.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#EFEFEF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=258.0,
    y=95.0,
    width=263.0,
    height=23.0
)

# Cuadro para ingresar nombre de algun artista
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    389.5,
    146.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#EFEFEF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=258.0,
    y=134.0,
    width=263.0,
    height=23.0
)



# Funcion para generar la lista de canciones
def generateListSongs():
    entry_3.config(state= "normal")
    entry_3.delete('1.0', 'end')
    counter = 0
    max = 10
    lstSongsRecommended = []
    showList = []
    graphList = [[0]*11]*11
    weightListForGraph = [0]
    songName = entry_1.get()
    artistName = entry_2.get()
    nodo_inicial = songsList[songName]
    songsRecomended = prim_mst(graph, nDataSet, nodo_inicial)
    lstSongsRecommended = get_songs(songsRecomended,songsList)
    for i in range(0, len(lstSongsRecommended)):
        if(counter < max):
            if(artistsList[lstSongsRecommended[i]] != artistName):
                showList.append(lstSongsRecommended[i])
                counter += 1
                weightListForGraph.append(songsRecomended[i][1])

    graphList[[0][0]] = weightListForGraph
    graphicGraph = np.array(graphList)

    print(showList)
    for i in range(0, len(showList)):
        entry_3.insert('1.0', f"{ i + 1 }: { showList[i] }\n")
    entry_3.config(state= "disabled")    
    showGraph = drawGraph(graphicGraph, weighted=True)
    showGraph.render('grafo_output',format='png', cleanup=True)
    #entry_4.insert()
    #entry_4.config(state= "disabled")
    
    print(f"Lista de canciones recomendadas: {showList}")

# Boton para generar canciones
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command = generateListSongs,
    relief="flat"
)
button_1.place(
    x=300.0,
    y=179.0,
    width=100.0,
    height=31.0
)

########################## Imagenes ############################

# image_1
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    79.0,
    40.0,
    image=image_image_1
)

# image_2
image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    622.0,
    40.0,
    image=image_image_2
)

#################### Cajas de Texto ############################
# entry_3
entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    347.0,
    328.0,
    image=entry_image_3
)
entry_3 = Text(
    bd=0,
    bg="#EFEFEF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=52.0,
    y=261.0,
    width=590.0,
    height=132.0
)

# entry_4
entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    347.0,
    591.5,
    image=entry_image_4
)
entry_4 = Text(
    bd=0,
    bg="#EFEFEF",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=52.0,
    y=433.0,
    width=590.0,
    height=315.0
)

# Mantiene la aplicacion abierta
window.resizable(False, False)
window.mainloop()