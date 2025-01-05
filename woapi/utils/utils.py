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

def convert_to_time_type(time_str):
    """Converts time strings like '5 pm', '12:30 am' to datetime.time object"""
    return datetime.strptime(time_str, '%I:%M %p').time() if ':' in time_str else datetime.strptime(time_str,
                                                                                                    '%I %p').time()

def extract_times(time_string):
    # Define a regular expression pattern to capture times (with optional minutes and AM/PM)
    time_pattern = r'(\d{1,2}:\d{2}\s?[apm]{2}|\d{1,2}\s?[apm]{2})'

    # Split the input string by the '/' separator
    sections = time_string.split('/')
    extracted_times = []
    for section in sections:
        # Find all matches (start and end times) in the current section
        times = re.findall(time_pattern, section.strip())

        if len(times) == 2:
            # Convert both start and end times to datetime.time objects
            start_time = convert_to_time_type(times[0])
            end_time = convert_to_time_type(times[1])
            extracted_times.append((start_time, end_time))

    return extracted_times

def conv_extracted_times_list(companiesdataframe):
    temp = companiesdataframe['Hours'].tolist()
    res = []
    for i in range(len(temp)):
        new = extract_times(temp[i])
        res.append(new)
        for j in new:
            res.append(j)
    return res

def cleanup_times(res):
    timeslist = [xx for xx in res]
    timelist = [x for xs in timeslist for x in xs]
    timeres = []
    for xx in timelist:
        if isinstance(xx, tuple):
            timeres.append(xx)
    return timeres

def replace_midnight_with_close_time(df): #function to replace midnight with 11:59, feeds into overlap edge case fx
    # Loop through the dataframe and replace 12:00 AM with 11:59 PM
    df['close'] = df['close'].apply(lambda x: time(23, 59, 59) if x == time(0, 0, 0) else x)

    return df

def add_bins_for_time_overlap(df): #if the close time < open time, we need to add a new row with 00:00:00 open and same close
    new_rows = []
    for index, row in df.iterrows():
        if row['close'] < row['open']:
            new_row = {'open': time(0, 0), 'close': row['close'], 'company_name':row['company_name'], 'wkday':row['wkday']}
            new_rows.append(new_row)

    # Append new rows to the original dataframe
    df_new_rows = pd.DataFrame(new_rows)
    df = pd.concat([df, df_new_rows], ignore_index=True).sort_values(by='open').reset_index(drop=True)
    return df

def transform_company_df(companiesdf):

    res_time = conv_extracted_times_list(companiesdf)
    res_time = cleanup_times(res_time)
    wk_ranges_and_days = wkdays_from_input(companiesdf)
    res_days = structure_days_list(wk_ranges_and_days)
    company_names = get_company_names_list(companiesdf)
    open_close_temp_df = pd.DataFrame(res_time, columns=['open', 'close'])
    compdf_transformed = pd.DataFrame({
        'wkday': res_days,
        'company_name': company_names,
    })
    compdf_transformed = pd.concat([compdf_transformed, open_close_temp_df], axis=1)
    compdf_transformed = compdf_transformed.explode('wkday', ignore_index=True)
    compdf_transformed = replace_midnight_with_close_time(compdf_transformed)
    compdf_transformed = add_bins_for_time_overlap(compdf_transformed)
    return compdf_transformed


