import time
import pandas as pd
import re as re #Python RegEx library

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#string to display the time period the user selects for filtering
FILTER_PERIOD = ""

# month lists to use to get user input for month and conversion to Month name (january, february, ... , june)
month_full = ['january', 'february', 'march', 'april', 'may', 'june']
month_abr = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']


def get_filters():
    """Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    """

    global FILTER_PERIOD 

    print('Hello! Let\'s explore some US bikeshare data!')

    #use regex patterns to check user input, ignoring case
    input_pattern_city = re.compile(r"^chicago|new york city|washington$", re.IGNORECASE)
    pattern_filter = re.compile(r"^month|day|both|none$", re.IGNORECASE)
    
    # get user input for city (chicago, new york city, washington)
    while True:
        try:
            city = input('\nPlease enter the city you\'d like to explore: Chicago, New York City or Washington?\nCity: ').lower()
            match_city = input_pattern_city.match(str.strip(city))
            if match_city:
                print('\nWe\'ll explore {}!'.format(match_city.string.title()))
                break
            else:
                print('Oops! That doesn\'t appear to be a valid city input, check your spelling and try again :-)\n')
        except ValueError as ve:
            print('It appears you entered an incorrect value! Please try again :-)')
        except BaseException as e:
            print('Oops! That doesn\'t appear to be a valid city input, check your spelling and try again :-)\n')
        
    #get users choice of filters
    while True:
        try:
            time_filter = input('\nWould you like to filter by month, day, both or not at all? - type \'none\' for not at all\nFilter: ').lower()
            match_filter = pattern_filter.match(str.strip(time_filter))
            if match_filter:
                if match_filter.string == 'both':
                    month = month_input()
                    day = day_input()
                    FILTER_PERIOD = match_filter.string + ' - ' + month_full[month -1].title() + ', ' + day
                    break
                elif match_filter.string == 'month':
                    month = month_input()
                    day = None
                    FILTER_PERIOD = match_filter.string + ' - ' + month_full[month-1].title()
                    break
                elif match_filter.string == 'day':
                    month = None
                    day = day_input()
                    FILTER_PERIOD = match_filter.string + ' - ' + day
                    break
                elif match_filter.string == 'none':
                    FILTER_PERIOD = match_filter.string
                    month = None
                    day = None
                    break
            else:
                print('That does not appear to be a correct filter option!. Please check your spelling and try again :-)')
        except ValueError as ve:
            print('It appears you entered an incorrect value! Please try again :-)')
        except BaseException as be:
            print('That does not appear to be a correct filter option!. Please check your spelling and try again :-)')

    print('-'*40)
    return city, month, day


def month_input():
    """Prompts the user for a 'month' input and returns the integer value representing the month"""
    
    #pattern to check user input against
    month_pattern = re.compile(r"^january|jan|february|feb|march|mar|april|apr|may|june|jun$",re.IGNORECASE)

    #get user input for the month
    while True:
        try:
            month_input = input('\nEnter the month you\'d like to view - January to June - either the full month name or its first 3 letters\nMonth: ').lower()
            month_match = month_pattern.match(str.strip(month_input))
            if month_match:
                if len(month_match.string) == 3:
                    month = month_abr.index(month_match.string) + 1
                else:
                    month = month_full.index(month_match.string) + 1
                break
            else:
                print('Oops! That doesn\'t appear to be a valid month input, check your spelling and try again :-)\n')

        except ValueError as ve:
            print('Oops! Appears you\'ve enterred an incorrect value, check your spelling and try again :-)\n')
        except BaseException as be:
            print('Oops! That doesn\'t appear to be a valid month input, check your spelling and try again :-)\n')

    return month


def day_input():
    """Prompts the user for a day of the week to use in filtering data and returns the day of week as a text string"""

    #pattern to check user input against
    day_pattern = re.compile(r"^monday|tuesday|wednesday|thursday|friday|saturday|sunday$", re.IGNORECASE)

    #get user input for the day of the week
    while True:
        try:
            day_input = input('\nEnter the week day you\'d like to view - please use full week day name \nWeek day: ').lower()
            day_match = day_pattern.match(str.strip(day_input))
            if day_match:
                day = day_match.string.title()
                break
            else:
                print('Oops! That doesn\'t appear to be a valid day input, check your spelling and try again :-)\n')
        except ValueError as ve:
            print('Oops! Appears you enterred an incorrect value, check your spelling and try again :-)\n')
        except BaseException as be:
            print('Oops! That doesn\'t appear to be a valid day input, check your spelling and try again :-)\n')

    return day



def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #load data set from CSV file in same folder
    df = pd.read_csv(CITY_DATA[city])

    #convert Start Time to a datetime type to get month, day columns to filter on
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #add month (as integer vlaue) and Day_of_Week (as day text name) columns to the dataframe based on 'Start Time'
    df['Month'] = df['Start Time'].dt.month 
    df['Day_of_Week'] = df['Start Time'].dt.day_name()

    #filter the dataframe by month if requried
    if month != None:
        df = df.loc[df['Month'] == month]

    #filter dataframe by day if required
    if day != None:
        df = df.loc[df['Day_of_Week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.

    Args:
        (DataFrame) df - dataframe, based on filtered raw data, to base analysis on 
        (str) month - name of the month the data in df is filtered on, or "None" if no month filter applied
        (str) day - name of the day of the week the data in df is filtered on, or "None" if no day filter applied    
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if no month specified as a filter
    if month == None:
        print("The most frequent month of Travel is: ", month_full[(df['Month'].mode()[0])-1].title() )

    # display the most common day of week if no day specified as a filter
    if day == None:
        print("Most frequently on a - ", df['Day_of_Week'].mode()[0])

    # add an hour column based on Start Time
    df['Hour'] = df['Start Time'].dt.hour
    # display the most common start hour
    print("Most often during this hour: {}:00, with a Count of: {}".format(df['Hour'].mode()[0], df['Hour'].value_counts()[df['Hour'].mode()[0]]))

    # disply the filter period used
    print("\nfilter used: {}".format(FILTER_PERIOD))

    print("\nThis took %s seconds to calculate!" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    Args:
        (DataFrame) df - dataframe, based on filtered raw data, to base analysis on
    
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most used Start Station is: {}, with a count of: {} ".format(df['Start Station'].mode()[0], df['Start Station'].value_counts()[df['Start Station'].mode()[0]]))

    # display most commonly used end station
    print("The most used End Station is: {}, with a count of: {} ".format(df['End Station'].mode()[0], df['End Station'].value_counts()[df['End Station'].mode()[0]]))

    # create a Trip column as a combination of Start and End Stations
    df['Trip'] = df['Start Station'] + " -to- " + df['End Station']
    
    # display most frequent combination of start station and end station trip
    print("The most frequently taken Trip is from: ", df['Trip'].mode()[0])

    # disply the filter period used
    print("\nfilter used: {}".format(FILTER_PERIOD))

    print("\nThis took %s seconds to calculate!" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    Args:
        (DataFrame) df - dataframe, based on filtered raw data, to base analysis on
    
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total duration across all trips (s): ", df['Trip Duration'].sum())

    # display mean travel time
    print("Average duration for trips (s): ", df['Trip Duration'].mean())

    # disply the filter period used
    print("\nfilter used: {}".format(FILTER_PERIOD))

    print("\nThis took %s seconds to calculate!" % (time.time() - start_time))
    print('-'*40)



def user_stats(df, city):
    """Displays statistics on bikeshare users.
    
    Args:
        (DataFrame) df - dataframe, based on filtered raw data, to base analysis on
        (str) city - string containing the name of the city the bikeshare data originates from
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of the bikeshare user types: ')
    for ind, val in df['User Type'].value_counts().items():
        print('{}: {}'.format(ind, val))
    
    # Display counts of gender
    if city != 'washington':
        print('\nCounts of each Gender of our bikeshre users: ')
        for ind, val in df['Gender'].value_counts().items():
            print('{}: {}'.format(ind, val))

    # Display earliest, most recent, and most common year of birth
        print('\nYears of birth of our bikeshare users:')
        print('Earliest: ',int(df['Birth Year'].min()))
        print('Most Recent: ', int(df['Birth Year'].max()))
        print('Most common: ', int(df['Birth Year'].mode()[0]))


    # disply the filter period used
    print("\nfilter used: {}".format(FILTER_PERIOD))

    print("\nThis took %s seconds to calculate!" % (time.time() - start_time))
    print('-'*40)


def raw_data_view(df):
    """ Prompts the user to view the loaded raw data 5 rows at a time.
    
    Args:
        (DataFrame) df - dataframe, based on filtered raw data, to base analysis on
    
    """

    print('\nViewing raw data 5 data entires (rows) at a time...\n')

    i = 0 #to keep track of df index for data disply

    #output 5 rows of data
    while i < len(df):
        print(df.iloc[i:i+5].to_markdown())

        #prompt the user to continue viewing raw data or not
        user_continue = input('\ncontinue... enter \'no\' or \'n\' to exit\n').lower()
        if user_continue == 'no' or user_continue == 'n':
            break

        i += 5

    print('\n','-'*40)


def main():
    while True:
        city, month, day = get_filters()

        print('\nOne moment while we load the data and calculate your stats...!\n')

        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw_data = input('\nWould you like to view the raw data? Enter \'yes\' \\ \'y\' to view or anything else not to!\n').lower()
        if raw_data == 'yes' or raw_data == 'y':
            raw_data_view(df)

        restart = input('\nWould you like to restart? enter \'no\' or \'n\' to exit \n')
        if restart.lower() == 'no' or restart.lower() == 'n':
            break


if __name__ == "__main__":
	main()
