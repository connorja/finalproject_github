import time
import pandas as pd
#import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters(CITY_DATA):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) date_part - the date part being used to filter 
        (str) part - the name of the month or day chosen
       
    """
    month = ['January', 'February', 'March', 'April', 'May', 'June']
    day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    """ select the city."""
    city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()
    while city not in CITY_DATA:
        city = input('You typed "{}", please type Chicago, New York City, or Washington? '.format(city)).lower()
    print('You chose {}.'.format(city.title()))
    
    """ determine month, day or neither."""
    date_part = input('Would you like to filter the data by month, day, or not at all? ').lower().title()

    """bad input."""
    while date_part != 'Month' and  date_part != 'Day' and date_part != 'Not At All':
        date_part = input('Lets try again. Would you like to filter the data by month, day, or not at all? ').lower().title()
    
    """month chosen."""
    if date_part == 'Month':
        part = input('Which month - January, February, March, April, May, or June? ').lower().title()
        while part not in month:    
            part = input('Please type one of the following months - January, February, March, April, May, or June. ').lower().title()    
          
    """day chosen."""
    if date_part == 'Day':
        part = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ').lower().title()
        while part not in day:
            part = input('Please type one of the following days - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday. ').lower().title()
         
    """not at all chosen."""
    if date_part == 'Not At All':
        part = ''
    

    print('You chose the {} {}'.format(date_part,part))
    print('-'*40)
    return city, date_part, part


def load_data(city, date_part, part):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) data_part - month,  day or not at all
        (str) part - name of the day of week to filter by, or month name
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    """create dataframe and add filter columns."""
    df = pd.read_csv(CITY_DATA.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Hour'] = df['Start Time'].dt.hour
    df['Month'] = df['Start Time'].dt.month_name()
    df['Week Day'] = df['Start Time'].dt.day_name()
    
    if date_part == 'Day':
        df = df[(df['Week Day'] == part)]        
    elif date_part == 'Month':
        df = df[(df['Month'] == part)]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    popular_hour = df['Hour'].mode()[0]
    popular_week_day = df['Week Day'].mode()[0]
    popular_month = df['Month'].mode()[0]

    print('\nThe most common month of travel is {}. \nThe most common weekday is {}. \nThe most popular hour of the day is {}00 hrs.'.format(popular_month, popular_week_day, popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start = df['Start Station'].mode()[0]
    popular_end = df['End Station'].mode()[0]
    popular_trip = (df['Start Station'] +' to ' + df['End Station']).mode()[0]
    
    print('\nWhen starting a journey the most popular site is {}. \n{} is the most common ending destination. \nIf you are looking for a route {} is the most popular.'.format(popular_start, popular_end,popular_trip)) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """convert the travel time from seconds to days and hours for total and average"""
    total_travel = round(df['Trip Duration'].sum()/86400,2)
    avg_travel = round(df['Trip Duration'].mean()/60,2)

    print('\nThe total usage time is {} days. \nWhile the average trip is {} minutes.'.format(total_travel, avg_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    user_types = pd.Series(df['User Type'].value_counts())
    print('User Type Breakdown\n{}'.format(user_types))
    
    """if the dataframe has gender and birth year compute the following."""
    if 'Gender' and 'Birth Year' in df.columns:
        user_gender = pd.Series(df['Gender'].value_counts())
        user_birth_min = int(df['Birth Year'].min())
        user_birth_max = int(df['Birth Year'].max())
        user_birth_mode = int(df['Birth Year'].mode()[0])
        print('\nUser Gender\n{}'.format(user_gender))
        print('\nThe youngest user was born in {}.\nThe oldest user was born in {}.\nThe most common user was born in {}.'.format(user_birth_max, user_birth_min, user_birth_mode))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def row_data(df):
    """ determine the length of the data frame and iterate through untill the end position reaches the length.""" 
    
    length = len(df.index)
    start = 0
    end = start + 5
    
    while True:
        show_raw = input('Would you like to see the raw data? Yes/No ').lower().title()
        while show_raw != 'Yes' and show_raw != 'No':
            show_raw = input('Please enter Yes or No.').lower().title()
        if show_raw == 'No':
            print('No data will be shown')
            break 
        """Check for the end of the dataframe."""
        if end >= length :
            end = length
            pd.set_option('display.max_columns',20)
            print(df[start:end])
            print('\nThis is the end of the data.')
            break  
        pd.set_option('display.max_columns',20)    
        print(df[start:end])
        #print(length)
        #print(df.tail())
        start += 5
        end += 5   


def main():
    while True:
        city, date_part, part = get_filters(CITY_DATA)
        df = load_data(city, date_part, part)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart != 'yes' and restart != 'no':
            restart = input('\nPlease enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        """ need to add a loop to request a valid imput."""

if __name__ == "__main__":
	main()