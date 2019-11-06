import quandl, requests, json, time
import yfinance as yf
import matplotlib.pyplot as plt
import pandas
#symbol, name, exch, type, exchDisp, typeDisp
 
result = []
brake = True
 
starttext = """
STOCK COUNTER v3.0
Gnu 3.0 Samuel Cheng
bit.ly/SamuelCheng2019
 
WELCOME!
 
               ______________
   __,.,---'''''              '''''---..._
,-'             .....:::''::.:            '`-.
'           ...:::.....       '
           ''':::'''''       .               ,
|'-.._           ''''':::..::':          __,,-
'-.._''`---.....______________.....---''__,,-
     ''`---.....______________.....---''
 
 
Type in a list company to begin!
(e.g. Google)
"""
 
 
help_text = """
Type in a list company to begin!
(e.g. Google)
 
Type in [exit] to exit!
 
Type in [help] to display help!
"""
def printResult():
    i = 0
    recurse = ["Symbol", "Name", "Exch", "Type", "ExchDisp", "TypeDisp"]
    for element in recurse:
        print("{0} -> {1}".format(element, result[i]))
        i += 1
 
 
 
 
class load:
    infoAPI = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={name}&region=1&lang=en"
    recurse = ["symbol", "name", "exch", "type", "exchDisp", "typeDisp"]
    symbol = ""
 
    def __init__(self, r):
        self.r = r
 
        load.load(r)
 
 
    def load(r):
        parse(r)
        global result
        #load data
        response = json.loads(requests.get(load.infoAPI.format(name = r)).text)
 
 
        #Clears Variables
        result = []
        load.symbol = ""
 
 
        try:
            for element in load.recurse:
                result.append(response["ResultSet"]["Result"][0][element])
 
            load.symbol = result[0]
        except IndexError:
            print("Error: Your search - {} - did not match any results in our database.\nSuggestions:\n1. Make sure that all words are spelled correctly.\n2. Try different keywords.".format(r))
            brake = False
            main()
        brake = True
 
 
        msft = yf.Ticker(load.symbol)
        continueAction = True
        history = msft.history(period = "max").index.copy()
        print("=========Meta Info=========")
        print("Historical Market Data:\n----------\n{}\n----------\n".format(msft.history(period = "max")))
        if msft.actions.empty:
            print("No Actions!\n")
        else:
            print("Actions:\n----------\n{}\n----------\n".format(msft.actions))
 
 
 
 
        if brake:
            printResult()
        graph(history, msft)
 
 
 
 
 
 
 
def graph(date, msft):
    x = date.tolist()
    lister = []
    index = 1
    for element in x:
        if index % 365 == 0:
            lister.append("{0}-{1}-{2}".format(element.year, element.month, element.day))
        index += 1
    x1 = msft.history(period="max")["Open"].tolist()
    final = []
    index1 = 1
    for element in x1:
        if index1 % 365 == 0:
            final.append(element)
        index1 += 1
 
 
    #init graph
    global result
    plt.style.use('seaborn-whitegrid')
    plt.plot(lister, final)
    plt.xlabel("Date")
    plt.ylabel("Open")
    plt.title("Graph of {}'s Open History".format(result[1]))
    plt.gcf().autofmt_xdate()
    plt.show()
 
 
 
def parse(r):
    if r == "[exit]":
        print("Exiting...")
        exit()
    elif r == "[help]":
        print(help_text)
        main()
 
 
 
def main():
    global brake
    while True:
        load(input(" >>> "))
 
        if brake:
            brake = False
 
 
 
 
if __name__ == "__main__":
    print(starttext)
    main()
