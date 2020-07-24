import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import PySimpleGUI as sg

# --Initialization --
df = pd.read_csv('data/boroughs-case-hosp-death.csv', parse_dates=True, index_col=0)
# print(df.tail(10))

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


def getData(date, boro, count):
    col = boros[boro] + types[count]
    return df[col][date]  # df col row


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


def main():
    print("Welcome to the COVD19 Calculator")
    print("What would you like to do?")
    print("1. Look at data for a specific day.")
    print("2. Calculate percent change between two dates.")
    print("3. Calculate the infection rate for a specific day.")
    choice = input("Enter a number as your choice. \n")
    if choice == "1":
        date = input("\n" + "Choose a date (in YYYY-MM-DD). \n")
        boro = input("What borough do you want to see? \n").upper()
        count = input("What type of data? Enter case count, hospitalized count, death count, or all. \n").upper()
        if count == "ALL":
            print("CASE COUNT:" + str(getData(date, boro, "CASE COUNT")))
            print("HOSPITALIZED COUNT: " + str(getData(date, boro, "HOSPITALIZED COUNT")))
            print("DEATH COUNT: " + str(getData(date, boro, "DEATH COUNT")))
        else:
            print(count + ": " + str(getData(date, boro, count)))
    elif choice == "2":
        print(dodPercentChange())
    elif choice == "3":
        date = input("\n" + "Choose a date (in YYYY-MM-DD). \n")
        cases = getData(date, "MANHATTAN", "CASE COUNT") + getData(date, "BROOKLYN", "CASE COUNT") + \
                getData(date, "QUEENS", "CASE COUNT") + getData(date, "BRONX", "CASE COUNT") + \
                getData(date, "STATEN ISLAND", "CASE COUNT")
        rate = infectionRate(cases)
        print(date + ": " + "TOTAL CASES: " + str(cases) + " Infection Rate: " + str(round(rate, 5)) + "%.")


def run():
    # sg.theme('Dark Blue 3')  # please make your creations colorful
    one = "Look at data for a specific day"
    two = "Calculate percent change between two dates."
    three = "Calculate the infection rate for a specific day."
    layout = [[sg.Text('Welcome to the Coronavirus Calculator')],
              [sg.Button(one)],
              [sg.Button(two)],
               [sg.Button(three)]]
    window = sg.Window('Coronavirus Calculator', layout)
    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break
    window.close()

main()