import pandas as pd
from datetime import datetime, timedelta

def groups_size_check(week_col, groups_size):

    ### The function checks if the number of points per week in the uploaded file is
    ### equal to the number of points per week in the groups_size dictionary

    ### @param week_col  - Pandas Series of point's weeks
    ### @param  groups_size - Dictionary of groups size (List) per week (Dictionary Key)
    ### @returns ValueError or None

    for week in groups_size:
        dict_group_size = sum(groups_size[week])
        file_group_size = week_col.value_counts().ix[week]

        if  dict_group_size != file_group_size:
            err = '''Week {} groups size doesn't valid! 
            the size in in the file is {}, but the size in groups_size dictionary is {}'''.format(week,
                                                                                                  file_group_size,
                                                                                                  dict_group_size)

            raise ValueError(err)


def find_next_weekday(weekday, time):

    ### This function finds the next date of a chosen weekday and returns it with chosen time

    ### @param weekday - String with the chosen weekday to find
    ### @param time - String with the chosen time for the output ("HH:MM")
    ### @returns Datetime

    weekdays_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day
    hour = time.hour
    minutes = time.minute

    date = datetime(year, month, day, hour, minutes)

    weekday_ix = weekdays_names.index(weekday.lower())

    while date.weekday() != weekday_ix or date < today:
        date += timedelta(1)
    return date


def set_names_by_weeks(data):

    ### This function sets a Dictionary of names by weeks, according to data in
    ### the uploaded file (weeks are Keys and names are lists of points names)

    ### @param data - Pandas DataFrame with columns of point's weeks & names
    ### returns Dictionary of names by weeks

    names_by_weeks = {}

    for week in data.Week.unique():
        names_by_weeks[week] = data[data.Week == week].Name.tolist()

    return names_by_weeks