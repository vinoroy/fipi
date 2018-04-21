
import csv


def loadSsap():

    with open('ssap.txt') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')

        row1 = next(readCSV)

    return [row1]