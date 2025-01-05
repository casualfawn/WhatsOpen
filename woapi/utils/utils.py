from datetime import datetime, timedelta, time
import pandas as pd
import re

#Funs to extract Day Ranges and individual Days from input string Hours Column
def extract_days_after_comma(temp_match, matches_comma):
    if matches_comma:
        temp_comma = matches_comma[0]
        temp_match = ','.join(temp_match) + ',' + temp_comma
        temp_match = temp_match.split(',')
    return temp_match

def extract_days_after_slash(matches_slash, days_out, pattern):
    for part in matches_slash[1:]:
        temp_slash = re.findall(pattern, part)
        days_out.append(temp_slash[0][0])
    return days_out

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

def convert_day_range(matches):
    if '-' in matches[0][0]:
        temp_match = convert_weekday_range(matches[0][0])
    else:
        temp_match = list(matches[0][0])
    return temp_match

def days_out_fun(companiesdf):
    data_list = companiesdf['Hours'].to_list()
    data_list = [s.replace('Tues', 'Tue') for s in data_list]
    days_out = []
    for i in range(len(data_list)):
        # Match days and ranges: "Mon-Fri" or "Mon"
        pattern = r'(\\?\s?\w{3}-\w{3}|\s?\\?\w{3})(?:\s*-\s*(\w{3}))?'
        matches = re.findall(pattern, data_list[i])
        # Match days and day ranges directy after a comma "Mon-Fri," "Mon,"
        pattern_comma = r',\s*([A-Za-z]{3})(?=\s)'
        matches_comma = re.findall(pattern_comma, data_list[i])
        # Match days and ranges that come directly after a slash: " / Mon-Fri", " / Mon"
        matches_slash = data_list[i].split(' / ')
        # Convert Day Ranges to list of days "Mon-Tue" to "Mon, Tue"
        day_or_day_range = convert_day_range(matches)
        # If comma then additional days include days after comma [["Mon, Tue"], ["Thu"]] to [["Mon", "Tue", "Thu"]]
        day_or_day_range = extract_days_after_comma(day_or_day_range, matches_comma)
        # Append list of open days before a slash to output list
        days_out.append(day_or_day_range)
        # Append the additional days or day ranges that occur after a "/": "Mon-Tue 9am to 9pm / Wed 9am to 5pm" to [["Mon","Tue"],["Wed"]]
        days_out = extract_days_after_slash(matches_slash, days_out, pattern)

    return days_out


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
    res_days = days_out_fun(companiesdf)
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


