import time
import pandas as pd
import numpy as np
import json as json

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
    # TO DO: get user input which city they would like to view data for (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to explore: Chicago, New York City, or Washington? \n").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("Sorry, please choose Chicago, New York City, or Washington.")
            continue
        else:
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to view data for? January, February, March, April, May, or June? If you wish to view all months, type 'all'. \n")
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("Sorry, please choose a month between January and June or 'all'.")
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day would you like to view data for? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? If you wish to view all days, type 'all'. \n")
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("Sorry, please choose a correct day of the week or 'all'.")
            continue
        else:
            break

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
    #load data to dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #filter by month and day
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #filter by month
    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = month.index(month) + 1

        #filter by month for new dataframe
        df = df[df['month'] == month]

    #filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("Most Common Month:", popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("Most Common Day:", popular_day)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("Most Common Hour:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print("Most Commonly Used Start Station:", start_station)

    # TO DO: display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print("Most Commonly Used End Station:", end_station)

    # TO DO: display most frequent combination of start station and end station trip
    combo_station = df.groupby(['Start Station', 'End Station']).count()
    print("Most Commonly Used Combination of Start and End Stations:", start_station, " & ", end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = sum(df['Trip Duration'])
    total_round = round(total_travel)
    print("Total Travel Time:", total_round/86400, " Days")

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    mean_round = round(mean_travel)
    print("Mean Travel Time:", mean_round/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Types:\n", user_types)

    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("Gender Types:\n", gender)
    except KeyError:
        print("Gender Types: No gender data available for month selected.")

    # TO DO: Display earliest, most recent, and most common year of birth
    #convert year to int
    df['Birth Year'] = df['Birth Year'].fillna(0).astype(int)

    try:
        earliest = df['Birth Year'].min()
        print("Earliest Year of Birth:\n", earliest)
    except:
         print("Earliest Year of Birth: No birth data available for month selected.")

    try:
        most_recent = df['Birth Year'].max()
        print("Most Recent Year of Birth:\n", most_recent)
    except:
         print("Most Recent Year of Birth: No birth data available for month selected.")

    try:
        most_common = df['Birth Year'].value_counts().idxmax()
        print("Most Common Year of Birth:\n", most_common)
    except:
         print("Most Common Year of Birth: No birth data available for month selected.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    #prompt user whether they would like to see raw data and convert response to lower case
    i = 0
    rows = df.shape[0]
    raw = input("Would you like to view the raw data for the filters selected?\n").lower()

    for i in range(0, rows, 5):


        if raw == 'no':
            break
        #convert data to json then split data and print
        elif raw == 'yes':
            raw_data = df.iloc[i:i + 5].to_json(orient='split')
            new_row = json.loads(raw_data)
            json_row = json.dumps(new_row, indent=2)
            print(json_row)


     #prompt user whether they would like to view 5 more rows of data

        raw = input("Would you like to view 5 more rows of data?\n")

        #if user chooses yes, display next 5 rows
        if raw == 'yes':
           print(df[i:i+5])
        elif raw == 'no':
            break




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
