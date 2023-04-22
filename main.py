import os
import time
from InMemIndex import InMemIndex
from Utils import Load,Build,FormatSuggestions
from QueryCorrection import QueryCorrection

scriptPath = os.getcwd()



def Main():
    Index = Load()
    correction = QueryCorrection(Index)
    inputQuery = input('Enter your query: ')
    while(inputQuery != 'exit'):
        stime = time.time()
        sugguestions = correction.context(inputQuery)
        print(FormatSuggestions(sugguestions,20))
        print("\nSearch time: {0} second\n".format(time.time() - stime) )
        inputQuery = input('\nEnter your query: ')
    

if __name__ == "__main__":
    Main()