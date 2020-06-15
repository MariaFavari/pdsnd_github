"""
This program provides statistical information for the bikeshare data dupplied by Udacity.

Returns:
    Statistics on the most frequent times of travel.
    Statistics on the most popular stations and trip.
    Statistics on the total and average trip duration.
    Statistics on bikeshare users.
    Raw data can be reviewed at user request.

"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city=str(input("Which city would you like to see data for Chicago, New York City or Washington?\n").lower())

            if city in CITY_DATA:
                print("You will be reviewing data for {}.\nLet's start".format(city.title()))
                break
        except:
            print("That's not a valid input, please try again\n")

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        try:
            month=str(input("Would you like to filter the data by month? Select January, February, March, April, May, June or all.?\n").lower())
            if month in months:
                print("You selected to review {} data.\n".format(month.title()))
                break
        except:
            print("That's not a valid input, please try again\n")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days=['M', 'Tu','W', 'Th', 'F', 'Sa', 'Su', 'all']
    while True:
        try:
            day=str(input('Would you like to filter the data by day? Please type M, Tu, W, Th, F, Sa, Su or all?\n'))
            if day in days:
                break
        except:
            print("That's not a valid input, please try again\n")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
        # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days=['M', 'Tu','W', 'Th', 'F', 'Sa', 'Su']
        day=days.index(day)
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month= df['month'].mode()[0]
    if popular_month==1:
        print('Most Popular month: January')
    elif popular_month==2:
        print('Most Popular month: February')
    elif popular_month==3:
        print('Most Popular month: March')
    elif popular_month==4:
        print('Most Popular month: April')
    elif popular_month==5:
        print('Most Popular month: May')
    else:
        print('Most Popular month: June')

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    if popular_day==0:
        print('Most Popular day of week: Monday')
    elif popular_day==1:
        print('Most Popular day of week: Tuesday')
    elif popular_day==2:
        print('Most Popular day of week: Wednesday')
    elif popular_day==3:
        print('Most Popular day of week: Thursday')
    elif popular_day==4:
        print('Most Popular day of week: Friday')
    elif popular_day==5:
        print('Most Popular day of week: Saturday')
    else:
        print('Most Popular day of week: Sunday')

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station= df['Start Station'].mode()[0]
    count_start_station = df['Start Station'].value_counts().max()
    print('Most Popular start station:', popular_start_station)
    print('Count of trips starting from the most popular start station:', count_start_station)

    # display most commonly used end station
    popular_end_station= df['End Station'].mode()[0]
    count_end_station = df['End Station'].value_counts().max()
    print('Most Popular end station:', popular_start_station)
    print('Count of trips ending in the most popular station:', count_end_station)

    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print("The most popular combination Start Station, End Station, respectively is:", popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])
    df['difference']=df['End Time']-df['Start Time']
    total_travel_time= (df['difference'].sum())
    print('Total travel time for this period:', total_travel_time)

    # display mean travel time
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])
    df['difference']=df['End Time']-df['Start Time']
    average_travel_time= (df['difference'].mean())
    print('Average travel time for this period:', average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if "Gender" not in df:
        print("There is not gender data available.")
    else:
        user_gender = df['Gender'].value_counts()
        print(user_gender)

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" not in df:
        print("There is not birth year data available.")
    else:
        user_birth_earliest = df['Birth Year'].min()
        user_birth_recent = df['Birth Year'].max()
        user_birth_common = df['Birth Year'].mode()[0]

        print("The earliest year of birth for bikeshare users is:",user_birth_earliest)
        print("The most recent year of birth for bikeshare users is:",user_birth_recent)
        print("The most common year of birth for bikeshare users is:",user_birth_common)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(city):
        """Displays raw data, displays five rows."""
        df = pd.read_csv(CITY_DATA[city])
        while True:
            display_data= input("\nWould you like to see raw data? Enter yes or no.\n")
            if display_data.lower() =="no":
                break
            elif display_data.lower() =="yes":
                print(df.sample(5))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
