import matplotlib.pyplot as plt
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
boroughs = ["Brooklyn", "Queens", "Manhattan", "Bronx", "Staten Island", "The City"]


def getData(date, boro, count):
    if boro == "THE CITY":
        return getData(date, "MANHATTAN", count) + getData(date, "BROOKLYN", count) + \
               getData(date, "QUEENS", count) + getData(date, "BRONX", count) + \
               getData(date, "STATEN ISLAND", count)
    col = boros[boro] + types[count]
    return df[col][date]  # df col row


def dodPercentChange(date1, date2, boro, count):
    return str(round(((getData(date2, boro, count) - getData(date1, boro, count)) / getData(date1, boro, count)) * 100, 2)) + "%"


def infectionRate(num):
    nycPop = 8550971
    return num / nycPop * 100


def checkDate(m, d, y):
    if m not in months:
        return True
    elif d == 'DAY' or d == '':
        return True
    elif y == 'YEAR' or y == '':
        return True
    return False


def showGraph(boro, count):
    register_matplotlib_converters()
    dates = pd.date_range(start="2020-02-29", end="2020-07-07")
    countM = []
    countBK = []
    countQ = []
    countBX = []
    countSI = []
    countCity = []
    for i in dates:
        countM.append(getData(i, "MANHATTAN", count.upper()))
        countBK.append(getData(i, "BROOKLYN", count.upper()))
        countQ.append(getData(i, "QUEENS", count.upper()))
        countBX.append(getData(i, "BRONX", count.upper()))
        countSI.append(getData(i, "STATEN ISLAND", count.upper()))
        countCity.append(getData(i, "THE CITY", count.upper()))
    if boro[0]:
        plt.plot(dates, countBK, label="Brooklyn")
    if boro[1]:
        plt.plot(dates, countQ, label="Queens")
    if boro[2]:
        plt.plot(dates, countM, label="Manhattan")
    if boro[3]:
        plt.plot(dates, countBX, label="Bronx")
    if boro[4]:
        plt.plot(dates, countSI, label="Staten Island")
    if boro[5]:
        plt.plot(dates, countCity, label="The City")
    plt.ylabel('COUNT')
    plt.xlabel('DATE')
    plt.xticks(rotation=30)
    plt.title(count)
    plt.legend()
    plt.show(block=False)


# Command Line
def main():
    choice = ""
    print("Welcome to the COVID-19 Calculator")
    print("What would you like to do?")
    print("1. Look at data for a specific day.")
    print("2. Calculate percent change between two dates.")
    print("3. Calculate the infection rate for a specific day.")
    print("4. Plot a graph.")
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
        date1 = input("\n" + "Choose a date (in YYYY-MM-DD). \n")
        date2 = input("\n" + "Choose another date (in YYYY-MM-DD). \n")
        boro = input("What borough do you want to see? \n").upper()
        count = input("What type of data? Enter case count, hospitalized count, death count, or all. \n").upper()
        print(dodPercentChange(date1, date2, boro, count))
    elif choice == 3:
        date = input("\n" + "Choose a date (in YYYY-MM-DD). \n")
        cases = getData(date, "THE CITY", "CASE COUNT")
        rate = infectionRate(cases)
        print(date + ": " + "TOTAL CASES: " + str(cases) + " Infection Rate: " + str(round(rate, 5)) + "%.")
    elif choice == 4:
        # the user should choose bc everything together is quite cluttered
        # perhaps in the GUI, offer the user a choice to view how many boroughs they want + the total
        count = input("What type of data? Enter case count, hospitalized count, or death count \n").upper()
        showGraph(count)
        print("DISPLAYING GRAPH")


# GUI
def run():
    # sg.theme('Dark Blue 3')  # please make your creations colorful
    sg.ChangeLookAndFeel('Reddit')
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
    mainWindow = sg.Window('Coronavirus Calculator', layout, size=(500, 250), element_justification='c')
    while True:
        event, values = mainWindow.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == one:
            mainWindow.Hide()
            # may have to take invalid inputs or bypass this by putting in more combos
            layout = [[sg.Text('Choose a date:')],
                      [sg.Combo(months, key='MM'), sg.InputText('DAY', key='DD', size=(4, 1)),
                       sg.InputText('YEAR', key='YYYY', size=(6, 1))],
                      [sg.Text('Choose a borough:')],
                      [sg.Combo(boroughs)],
                      [sg.Button("Submit")],
                      [sg.Text(key="title", size=(30, 1))],
                      [sg.Text(key="data", size=(30, 3))]]
            window = sg.Window('Data for a Specific Day', layout, size=(500, 250), element_justification='c')
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    window.Close()
                    mainWindow.UnHide()
                    break
                if event == "Submit":
                    if checkDate(values['MM'], values['DD'], values['YYYY']):
                        window['data'].update('Please enter a valid date.')
                    elif values[0] not in boroughs:
                        window['data'].update('Please enter a valid borough.')
                    else:
                        date = values['YYYY'] + "-" + monthToNum[values['MM']] + "-" + values['DD']
                        boro = values[0].upper()
                        case = "CASE COUNT: " + str(getData(date, boro, "CASE COUNT"))
                        hospitalized = "HOSPITALIZED COUNT: " + str(getData(date, boro, "HOSPITALIZED COUNT"))
                        death = "DEATH COUNT: " + str(getData(date, boro, "DEATH COUNT"))
                        window['title'].update("All Counts for " + values[0])
                        window['data'].update(case + "\n" + hospitalized + "\n" + death)
        elif event == two:
            mainWindow.Hide()
            layout = [[sg.Text('Choose a date:')],
                      [sg.Combo(months, key='MM1'), sg.InputText('DAY', key='DD1', size=(4, 1)),
                       sg.InputText('YEAR', key='YYYY1', size=(6, 1))],
                      [sg.Text('Choose another date:')],
                      [sg.Combo(months, key='MM2'), sg.InputText('DAY', key='DD2', size=(4, 1)),
                       sg.InputText('YEAR', key='YYYY2', size=(6, 1))],
                      [sg.Text('Choose a borough:')],
                      [sg.Combo(boroughs)],
                      [sg.Button("Submit")],
                      [sg.Text(key="title", size=(30, 1))],
                      [sg.Text(key="data", size=(30, 3))]]
            window = sg.Window('Percent Change Between Two Dates', layout, size=(500, 250), element_justification='c')
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    window.Close()
                    mainWindow.UnHide()
                    break
                if event == "Submit":
                    if checkDate(values['MM1'], values['DD1'], values['YYYY1']):
                        window['data'].update('Please enter a valid first date.')
                    elif checkDate(values['MM2'], values['DD2'], values['YYYY2']):
                        window['data'].update('Please enter a valid second date.')
                    elif values[0] not in boroughs:
                        window['data'].update('Please enter a valid borough.')
                    else:
                        date1 = values['YYYY1'] + "-" + monthToNum[values['MM1']] + "-" + values['DD1']
                        date2 = values['YYYY2'] + "-" + monthToNum[values['MM2']] + "-" + values['DD2']
                        boro = values[0].upper()
                        caseChange = "CASE COUNT: " + dodPercentChange(date1, date2, boro, "CASE COUNT")
                        hospitalizedChange = "HOSPITALIZED COUNT: " + \
                                             dodPercentChange(date1, date2, boro, "HOSPITALIZED COUNT")
                        deathChange = "DEATH COUNT: " + dodPercentChange(date1, date2, boro, "DEATH COUNT")
                        window['title'].update("Percent Change in " + values[0])
                        window['data'].update(caseChange + "\n" + hospitalizedChange + "\n" + deathChange)
        elif event == three:
            mainWindow.Hide()
            layout = [[sg.Text('Choose a date:')],
                      [sg.Combo(months, key='MM'), sg.InputText('DAY', key='DD', size=(4, 1)),
                       sg.InputText('YEAR', key='YYYY', size=(6, 1))],
                      [sg.Button("Submit")],
                      [sg.Text(key="title", size=(30, 1))],
                      [sg.Text(key="data", size=(30, 1))]]
            window = sg.Window('Infection Rate for a Specific Day', layout, size=(500, 250), element_justification='c')
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    window.Close()
                    mainWindow.UnHide()
                    break
                if event == "Submit":
                    if checkDate(values['MM'], values['DD'], values['YYYY']):
                        window['data'].update('Please enter a valid date.')
                    else:
                        date = values['YYYY'] + "-" + monthToNum[values['MM']] + "-" + values['DD']
                        window['title'].update("Infection Rate on " + date)
                        window['data'].update(infectionRate(getData(date, "THE CITY", "CASE COUNT")))
        elif event == four:
            mainWindow.Hide()
            layout = [[sg.Text("Choose borough(s):")],
                      [sg.Checkbox(boroughs[0]), sg.Checkbox(boroughs[1]), sg.Checkbox(boroughs[2]),
                       sg.Checkbox(boroughs[3]), sg.Checkbox(boroughs[4])],
                      [sg.Checkbox(boroughs[5])],
                      [sg.Text("Choose a count:")],
                      [sg.Button("Case Count"), sg.Button("Hospitalized Count"), sg.Button("Death Count")]]
            window = sg.Window('Plot A Graph', layout, size=(500, 250), element_justification='c')
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    window.Close()
                    mainWindow.UnHide()
                    break
                if event == 'Case Count':
                    showGraph(values, event)
                if event == 'Hospitalized Count':
                    showGraph(values, event)
                if event == 'Death Count':
                    showGraph(values, event)
    mainWindow.close()


# Running Methods
# main()
# showGraph("CASE COUNT")
run()
