from datetime import datetime, timedelta, time
import pandas as pd
import re

#Funs to extract Day Ranges and individual Days from input string Hours Column
def wkdays_from_input(companiesdataframe):
    input_string = companiesdataframe['Hours'].tolist()
    input_string = ''.join(input_string) # convert df column to string
    input_string = input_string.replace(' ', '') # rm space
    input_string = input_string.replace('Tues', 'Tue') #format for indexing (3 letter abbr)
    charlist = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fin = [] #output list
    #iterate to extract 'Day-Day' and 'Day' from string.
    for i in range(len(input_string)-2):
        daystr = input_string[i:i+3]
        if daystr in charlist:
            daystrcheck = input_string[i:i+4]
            if '-' == daystrcheck[3]:
                daystr = input_string[i:i+8]
                if ',' == daystr[7]:
                    daystr = input_string[i:i+11]
                else:
                    daystr = input_string[i:i+7]
                fin.append(daystr)
            if input_string[i:i+3] in charlist and input_string[i-1] == '/' and len(daystr) != 7:
                fin.append(daystr)
    return fin #returns 'Day-Day' and 'Day' as sep list items

def convert_weekday_range(weekday_range): #converts 'Day-Day' to full range [Day, Day, Day...]
    days_map = {
        'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6
    }
    reverse_days_map = {v: k for k, v in days_map.items()}
    start_day, end_day = weekday_range.split('-')
    start_day_num = days_map[start_day]
    end_day_num = days_map[end_day]

    # Get range of weekdays
    if start_day_num <= end_day_num:
        weekdays_in_range = list(range(start_day_num, end_day_num + 1))
    else:
        weekdays_in_range = list(range(start_day_num, 7)) + list(range(0, end_day_num + 1))

    return [reverse_days_map[day_num] for day_num in weekdays_in_range]

def structure_days_list(wkfin):
    res = list() #output ls
    charlist = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    for i in range(len(wkfin)):
        daystr = wkfin[i]
        for j in range(len(daystr)):
            if daystr[j] == '-':
                # get the days of the range mon-fri
                temp = convert_weekday_range(daystr[j-3:j+4])
                newday = wkfin[i].replace(''.join(daystr[j-3:j+4]), '')
                if ',' in newday: #if ',Day' append to sublist item's date range
                    temp.append(newday[1:len(newday)])
                res.append(temp)
            if daystr[j:j+3] in charlist and '-' not in daystr:
                res.append(daystr) #if 'Day' append to list in sep sublist
    return res

def get_company_names_list(companiesdf):
    count = 0
    tracker = 0
    cnames = list()
    curr = 1
    clist = []
    companiesls = companiesdf['Restaurant Name'].tolist()
    wordlist = companiesdf['Hours'].tolist()
    for word in wordlist:
        for i in range(curr):
            curr = 1
            clist.append(companiesls[tracker - 1])
            for letter in word:
                if letter == '/':  # don't skip
                    curr += 1  # how many times to add to companies list
        tracker += 1
    clist = clist[1:]

    wordendlist = wordlist[-1:]
    count = 1
    for word in wordendlist:
        for letter in word:
            if '/' == letter:
                count += 1
    for i in range(count):
        clist.append(''.join(companiesls[-1:]))
    return clist

