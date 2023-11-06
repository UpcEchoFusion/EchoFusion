#imports
import csv
import heapq

#Getting the list of the names from the dataset
nameList = []
def getNameList():
    csv_file = csv.reader(open('Spotify-2000.csv', 'r'))
    next(csv_file)
    for lines in csv_file:
        nameList.append(lines[1])

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
    max_quantity = 10
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
        if counter < max_quantity:
          mst_tree.append([edge[0], edge[1]])
        counter += 1
        
    return mst_tree

#converting the mst_tree to a list of the songs recommended
songsRecomendedName = []
def get_songs(songsRecomended, songList):
    for key, val in songList.items():
        for i in range(len(songsRecomended)):
            if val == songsRecomended[i][0]:
                songsRecomendedName.append(key)

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


#asking for the song and getting the recommended song list
songName = input("escribe el nombre de la canción que quieres buscar: ")
nodo_inicial = songsList[songName]
songsRecomended = prim_mst(graph, nDataSet, nodo_inicial)
get_songs(songsRecomended,songsList)
print(f"Lista de canciones recomendadas: {songsRecomendedName}")