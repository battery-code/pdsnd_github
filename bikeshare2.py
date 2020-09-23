import time
import pandas as pd

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

    ## get user input for city.
    ## prevent/reduce user input errors (Newyork or New York or New York City) by requesting only one letter for the city

    print ("\nWhich city's statistics would you like to see?")
    while True:
        city = input("Choose a city by entering a letter.\nc for Chicago or n - New york or w - Washington:").lower()
        if city not in ("c","n","w"):
            print("\nInvalid Entry!")
            print("-"*14)
        else:
            break

    ## converting input to full city name to keep the values returned by this function named properly. CITY_DATA dictionary's keys were not changed to a letter to keep code readable. 
    if city == "c":
        city = "chicago"
    elif city == "n":
        city = "new york city"
    else:
        city = "washington"

    print('*'*40)

    ## get user input for month and day filters
    ## prevent/reduce user input error by requesting only a number

    print("\nWould you like to include all months or filter data for one specific month?")
    while True:
        month = input("Enter a digit from 0 to 6 corresponding to:\n0-include all months\n1-January\n2-February\n3-March\n4-April\n5-May\n6-June\n:")
        if month not in ("0","1","2","3","4","5","6"):
            print("\nInvalid Entry!")
            print("-"*14)
        else:
            break

    print('*'*40)


    print("\nWould you like to include all days of week or filter for one specific day?")
    while True:
        day = input("Enter a digit from 0 to 7 corresponding to:\n0-include all days\n1-Monday\n2-Tuesday\n3-Wednesday\n4-Thursday\n5-Friday\n6-Saturday\n7-Sunday\n:")
        if day not in ("0","1","2","3","4","5","6","7"):
            print("\nInvalid Entry!")
            print("-"*14)
        else:
            break

    #convert type of inputs from str to int
    month = int(month)
    day = int(day)

    # print("City= ",city)
    # print("Month= ",month)
    # print("Day= ",day)             

    print('*'*50)

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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 0:
        df = df[(df.month == month)]
        
    # filter by day of week if applicable
    if day != 0:
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nThe Most Frequent Times of Travel:\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is:",df["month"].mode()[0])
    
    # display the most common day of week
    print("The most common day of week is:",df["day_of_week"].mode()[0])
     
    # display the most common start hour
    print("The most common hour is:",df["hour"].mode()[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nThe Most Popular Stations and Trip:\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used starting station is:\n",df["Start Station"].mode()[0])
    # display most commonly used end station
    print("The most commonly used ending station is:\n", df["End Station"].mode()[0])
    # display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station is:\n", (df["Start Station"] + ' AND ' + df["End Station"]).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nTrip Duration Statistics:\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time in minutes is:",df["Trip Duration"].sum())

    # display mean travel time
    print("The mean travel time in minutes is:",df["Trip Duration"].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nUser Statistics:\n')
    start_time = time.time()

    # Display counts of user types
    print("The user types and their count is:\n",df["User Type"].value_counts(ascending=False))

    # Display counts of gender only if the data is available
    ## It was pre-stated that gender data is not available for one city hence this check is added only here
    if df.get("Gender") is not None:
        print("\nThe gender split is:\n",df["Gender"].value_counts(ascending=False))

    # Display earliest, most recent, and most common year of birth only if the data is available
    ## It was pre-stated that year of birth data is not available for one city hence this check is added only here
    if df.get("Birth Year") is not None:
        print("\nThe earliest year of birth of users is:",int(df["Birth Year"].min()))
        print("The latest year of birth of users is:",int(df["Birth Year"].max()))
        print("The most common year of birth of users is:",int(df["Birth Year"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data from CSV files 5 lines at a time based on user input"""
    start_time = time.time()

    # Find out if user wishes to see raw data
    while True:
        data = input('Would you like to see the raw data? Enter y for yes and n for no.\n:').lower()
        if data not in ("y","n"):
            print("\nInvalid Entry!")
            print("-"*14)
        else:
            break
    
    ## Print 5 rows of data at a time and request user each time if more raw data is desired
    n=0   #set row number counter to zero
    while data == 'y':
        print(df.iloc[n:n+5])
        n += 5
        while True:
            data = input('Would you like to see more raw data? Enter y for yes and n for no.\n:').lower()
            if data not in ("y","n"):
                print("\nInvalid Entry!")
                print("-"*14)
            else:
                break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    print('*'*50)
    print('Hello! Welcome to the US bikeshare data center!\nLet\'s look at some interesting statistics!')
    print('*'*50)

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #Loop to check if the filters applied creates an empty dataframe
        if len(df.index) == 0:
            print('! '*30)
            print("There is no data for the selected, month and day, filters.\nPlease select different filters.")
            print('! '*30)
            print()
            continue

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        while True:
            restart = input('Would you like to restart? Enter y for yes or n for no.\n:')
            if restart not in ("y","n"):
                print("\nInvalid Entry!")
                print("-"*14)
            else:
                break

        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
