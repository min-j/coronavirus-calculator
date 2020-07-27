import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd
import PySimpleGUI as sg
from pandas.plotting import register_matplotlib_converters

# --Initialization --
df = pd.read_csv('data/boroughs-case-hosp-death.csv', parse_dates=True, index_col=0)

boros = {
    'BROOKLYN': "BK",
    'QUEENS': "QN",
    'MANHATTAN': "MN",
    'BRONX': "BX",
    'STATEN ISLAND': "SI"
}

types = {
    "CASE COUNT": "_CASE_COUNT",
    "HOSPITALIZED COUNT": "_HOSPITALIZED_COUNT",
    "DEATH COUNT": "_DEATH_COUNT"
}

monthToNum = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

months = ["January", "February", "March", "April",
          "May", "June", "July", "August",
          "September", "October", "November", "December"]
boroughs = ["Brooklyn", "Queens", "Manhattan", "Bronx", "Staten Island"]


def getData(date, boro, count):
    col = boros[boro] + types[count]
    return df[col][date]  # df col row


def getTotal(date, count):
    return getData(date, "MANHATTAN", count) + getData(date, "BROOKLYN", count) + \
           getData(date, "QUEENS", count) + getData(date, "BRONX", count) + \
           getData(date, "STATEN ISLAND", count)


def dodPercentChange():
    # today = main()
    date1 = input("Choose the first (earlier) date (in YYYY-MM-DD format): ")
    date2 = input("Choose the second(later) date (in YYYY-MM-DD format): ")
    boro = input("What borough do you want to see? ").upper()
    count = input("What type of data (enter case count, death count, or hospitalized count)? ").upper()
    return str(((getData(date2, boro, count) - getData(date1, boro, count)) / getData(date1, boro, count)) * 100) + "%"


def infectionRate(num):
    nycPop = 8550971
    return num / nycPop * 100


# maybe plot all lines for proper comparison
def showGraph(count):
    register_matplotlib_converters()
    dates = pd.date_range(start="2020-02-29", end="2020-07-07")
    countM = []
    countBK = []
    countQ = []
    countBX = []
    countSI = []
    countTotal = []
    for i in dates:
        countM.append(getData(i, "MANHATTAN", count))
        countBK.append(getData(i, "BROOKLYN", count))
        countQ.append(getData(i, "QUEENS", count))
        countBX.append(getData(i, "BRONX", count))
        countSI.append(getData(i, "STATEN ISLAND", count))
        countTotal.append(getTotal(i, count))
    plt.plot(dates, countM, label="Manhattan")
    plt.plot(dates, countBK, label="Brooklyn")
    plt.plot(dates, countQ, label="Queens")
    plt.plot(dates, countBX, label="Bronx")
    plt.plot(dates, countSI, label="Staten Island")
    # plt.plot(dates, countTotal, label="Total")
    plt.ylabel('COUNT')
    plt.xlabel('DATE')
    plt.xticks(rotation=30)
    plt.title(count)
    plt.legend()
    plt.show()


def main():
    choice = ""
    print("Welcome to the COVID-19 Calculator")
    print("What would you like to do?")
    print("1. Look at data for a specific day.")
    print("2. Calculate percent change between two dates.")
    print("3. Calculate the infection rate for a specific day.")
    print("4. Plot a graph.")
    # This 'catching
    while True:
        try:
            choice = int(input("Enter a number as your choice. \n"))
        except ValueError:
            continue
        else:
            break
    if choice == 1:
        date = input("\n" + "Choose a date (in YYYY-MM-DD). \n")
        boro = input("What borough do you want to see? \n").upper()
        count = input("What type of data? Enter case count, hospitalized count, death count, or all. \n").upper()
        if count == "ALL":
            print("CASE COUNT:" + str(getData(date, boro, "CASE COUNT")))
            print("HOSPITALIZED COUNT: " + str(getData(date, boro, "HOSPITALIZED COUNT")))
            print("DEATH COUNT: " + str(getData(date, boro, "DEATH COUNT")))
        else:
            print(count + ": " + str(getData(date, boro, count)))
    elif choice == 2:
        print(dodPercentChange())
    elif choice == 3:
        date = input("\n" + "Choose a date (in YYYY-MM-DD). \n")
        cases = getTotal(date, "CASE COUNT")
        rate = infectionRate(cases)
        print(date + ": " + "TOTAL CASES: " + str(cases) + " Infection Rate: " + str(round(rate, 5)) + "%.")
    elif choice == 4:
        # the user should choose bc everything together is quite cluttered
        # perhaps in the GUI, offer the user a choice to view how many boroughs they want + the total
        count = input("What type of data? Enter case count, hospitalized count, or death count \n").upper()
        showGraph(count)
        print("DISPLAYING GRAPH")


# have to take invalid user inputs
def run():
    # sg.theme('Dark Blue 3')  # please make your creations colorful
    one = "Look at data for a specific day"
    two = "Calculate percent change between two dates."
    three = "Calculate the infection rate for a specific day."
    four = "Plot a graph."
    layout = [[sg.Text('Welcome to the Coronavirus Calculator')],
              [sg.Button(one)],
              [sg.Button(two)],
              [sg.Button(three)],
              [sg.Button(four)],
              ]
    mainWindow = sg.Window('Coronavirus Calculator', layout)  # size=(500, 500)
    mainActive = False
    while True:
        event, values = mainWindow.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == one:
            mainWindow.Hide()
            # may have to take invalid inputs or bypass this by putting in more combos
            layout = [[sg.Text('Choose a date:')],
                      [sg.Combo(months, key='MM', default_value='February'), sg.InputText('DAY', key='DD', size=(4, 1)),
                       sg.InputText('YEAR', key='YYYY', size=(6, 1))],
                      [sg.Text('Choose a borough:')],
                      [sg.Combo(boroughs)],
                      [sg.Text("What type of data?")],
                      [sg.Button("Case Count"), sg.Button("Hospitalized Count"), sg.Button("Death Count"),
                       sg.Button("All")],
                      [sg.Text(key="title", size=(30, 1))],
                      [sg.Text(key="data", size=(30, 3))]]
            window = sg.Window('Data for a specific day', layout)
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    window.Close()
                    mainWindow.UnHide()
                    break
                date = values['YYYY'] + "-" + monthToNum[values['MM']] + "-" + values['DD']
                boro = values[0].upper()
                if event == "Case Count":
                    window['title'].update(values[0] + " " + event)
                    window['data'].update(event.upper() + ": " + str(getData(date, boro, event.upper())))
                elif event == "Hospitalized Count":
                    window['title'].update(values[0] + " " + event)
                    window['data'].update(event.upper() + ": " + str(getData(date, boro, event.upper())))
                elif event == "Death Count":
                    window['title'].update(values[0] + " " + event)
                    window['data'].update(event.upper() + ": " + str(getData(date, boro, event.upper())))
                elif event == "All":
                    case = "CASE COUNT: " + str(getData(date, boro, "CASE COUNT"))
                    hospitalized = "HOSPITALIZED COUNT: " + str(getData(date, boro, "HOSPITALIZED COUNT"))
                    death = "DEATH COUNT: " + str(getData(date, boro, "DEATH COUNT"))
                    window['title'].update(values[0] + " All Counts")
                    window['data'].update(case + "\n" + hospitalized + "\n" + death)
    mainWindow.close()


# Running Methods
# main()
# showGraph("CASE COUNT")
run()
