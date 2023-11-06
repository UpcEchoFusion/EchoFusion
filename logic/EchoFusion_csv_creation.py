#imports
import csv


#Getting the .csv file with the edges weighted
def getNameList():
    nameList = []
    csv_file = csv.reader(open('Spotify-2000.csv', 'r'))
    next(csv_file)
    for lines in csv_file:
        nameList.append(lines[1])
    return nameList

def getGenreList():
    genreList = []
    csv_file = csv.reader(open('Spotify-2000.csv', 'r'))
    next(csv_file)
    for lines in csv_file:
        genreList.append(lines[3])
    return genreList

def getYearList():
    yearList = []
    csv_file = csv.reader(open('Spotify-2000.csv', 'r'))
    next(csv_file)
    for lines in csv_file:
        yearList.append(lines[4])
    return yearList

    
def getLoudnessList():
    loudnessList = []
    csv_file = csv.reader(open('Spotify-2000.csv', 'r'))
    next(csv_file)
    for lines in csv_file:
        loudnessList.append(lines[8])
    return loudnessList

#Edges not weighted
def getNamesByGenre(nameList, genreList):
    namesRelated = []
    for i in range(0, len(nameList) - 2):
        for j in range(1, len(nameList)-1):
            if genreList[i] == genreList[j]:
                namesRelated.append({'Source': nameList[i], 'Target': nameList[j]})
    fieldName = ['Source', 'Target']
    csv_file = csv.DictWriter(open('aristas3.csv', 'w', newline=''),fieldnames=fieldName,delimiter=';')
    csv_file.writeheader()
    csv_file.writerows(namesRelated)

#Edges weighted
def getNamesByGenreWeighted(nameList, genreList, yearList, loudnessList):    
    namesRelated = []
    for i in range(0, len(nameList) - 2):
        for j in range(1, len(nameList)-1):
            if genreList[i] == genreList[j]:
                yearDif = 0.5 * abs(int(yearList[i]) - int(yearList[j]))
                loudnessDif = 0.4* abs(abs(int(loudnessList[i])) - abs(int(loudnessList[j])))
                weight = 1 + yearDif + loudnessDif
                weight = round(weight,3)
                str(weight)
                namesRelated.append({'Source': nameList[i], 'Target': nameList[j], 'Weight': weight})
    fieldName = ['Source', 'Target', 'Weight']
    csv_file = csv.DictWriter(open('aristasWeighted.csv', 'w', newline=''),fieldnames=fieldName,delimiter=';')
    csv_file.writeheader()
    csv_file.writerows(namesRelated)


getNamesByGenreWeighted(getNameList(), getGenreList(),getYearList(),getLoudnessList())




