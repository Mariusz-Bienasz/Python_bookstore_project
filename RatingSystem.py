# Plik do obsługi systemu ocen:
import csv

import GlobalVariables


def addRating(bookID,rate):
    '''
        Funkcja dodająca opinię do bazy danych

        Args:
            bookID: id książki
            rate: ocena ksiązki
        Return:
            True lub False
    '''
    path = "DATABASE/ratings.csv"
    newId = 1
    newLine = False
    with open(path,mode='r',encoding='utf-8') as file:
        allText = file.read()
        if allText and not allText.endswith('\n'):
            newLine = True
        reader = list(csv.reader(file))
        if len(reader) > 1:
            last = reader[-1]
            newId = int(last[0])+1
    with open(path,mode='a', newline='', encoding='utf-8') as file:
        if newLine == True:
            file.write('\n')
        writer = csv.writer(file)
        writer.writerow([newId, GlobalVariables.userID, bookID, rate])
        return True

    return False

def edditRating(bookID,rate):
    path = "DATABASE/ratings.csv"
    rows = []
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            if row[1] == str(GlobalVariables.userID) and row[2] == str(bookID):
                row[3] = str(rate)

            rows.append(row)
    with open(path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        return True
    return False

def setRating(bookID, rate):
    path = "DATABASE/ratings.csv"
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            if row[1] == str(GlobalVariables.userID) and row[2] == str(bookID):
                result = edditRating(bookID,rate)
                if result == True:
                    return True ,'Nadpisano ocene'
                else:
                    return False , "Nie udało się nadpisać oceny"

    result = addRating(bookID,rate)
    if result == True:
        return True , 'Zapisano ocenę'
    else:
        return False , "Nie udało się dodać oceny"

def getMyRate(bookId):
    path = "DATABASE/ratings.csv"
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            if row[1] == str(GlobalVariables.userID) and row[2] == str(bookId):
                return str(row[3])
    return "Wybierz ocenę"


def getMeanRate(bookID):
    path = "DATABASE/ratings.csv"
    ratings = []
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            if row[2] == str(bookID):
                ratings.append(int(row[3]))
    if len(ratings) > 0:
        mean = (sum(ratings)/len(ratings))
        return round(mean, 2)
    else: return 0.0