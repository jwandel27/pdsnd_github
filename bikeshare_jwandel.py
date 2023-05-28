import time
import pandas as pd
import numpy as np
import tabulate

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
    # get user input for city (chicago, new york city, washington).
    while True:
        try:
            city = input("Enter the name of the city you would like to explore (Chicago, New York City or Washington): ").title().lower()
        except KeyboardInterrupt:
            restart_qa = input("Would you like to restart? Enter yes or no: ")
            if restart_qa == 'yes':
                continue
            else:
                exit()
        if city not in ['chicago', 'washington', 'new york city']:
            print("Sorry, that's not a valid name. Please try again.")
            continue
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Please enter a month between January and June inclusive. If you want to see all months, please type 'all': ").title().lower()
        except KeyboardInterrupt:
            restart_qa = input("Would you like to restart this part? Enter yes or no: ")
            if restart_qa == 'yes':
                continue
            else:
                exit()
        if month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print("Sorry, that's not a valid month. Please try again.")
            continue
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Now enter the name of the day please. If you want to see all days, please type 'all': ").lower().title()
        except KeyboardInterrupt:
            restart_qa = input("Would you like to restart this part? Enter yes or no: ")
            if restart_qa == 'yes':
                continue
            else:
                exit()
        if day not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']:
            print("Hmm. That's not a valid day. Please try again.")
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
    # load specified data into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # converting 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and hour from 'Start Time' and create two new columns for each
    df['month'] = df['Start Time'].dt.month
    df['day_name'] = df['Start Time'].dt.day_name()
    # checks if user input is part of the list of months and converts the input (str) to an int
    if month != "all":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    # if user don't want to filter by month, do nothing    
    else:
        pass
    # checks if user input results in a day filter
    if day != "All":
        df = df[df['day_name'] == day.title()]
    # if user don't want to filter by day, do nothing    
    else: 
        pass

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month is the {}th".format(popular_month))
    # display the most common day of week
    popular_day = df['day_name'].mode()[0]
    print("The most common day is {}".format(popular_day))
    # display the most common start hour
    popular_start_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common start hour is {}:00h".format(popular_start_hour))

    print("\nThis took %s seconds." % round((time.time() - start_time), 5))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    popular_start_stat = df['Start Station'].mode()[0]
    print("The most commonly start station is {}".format(popular_start_stat))
    # display most commonly used end station
    popular_end_stat = df['End Station'].mode()[0]
    print("The most commonly end station is: {}".format(popular_end_stat))
    #display least commonly used start station
    unpopular_start_stat = df['Start Station'].value_counts().index[-1]
    print("The least commonly start station is {}".format(unpopular_start_stat))
    #display least commonly used end station
    unpopular_end_stat = df['End Station'].value_counts().index[-1]
    print("The least commonly end station is {}".format(unpopular_end_stat))
    # display most frequent combination of start station and end station trip
    popular_comb = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most frequent combination of start- and end station trip is {}".format(popular_comb))
    
    print("\nThis took %s seconds." % round((time.time() - start_time), 5))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time. For better readability in minutes and hours
    total_travel_time = np.sum(df['Trip Duration'])
    total_minutes = round((total_travel_time / 60), 2)
    total_hours = round((total_minutes / 60), 2)
    print("The total trip duration is {} minutes or {} hours".format(total_minutes, total_hours))
    # display mean travel time. For better readability in minutes and hours
    mean_travel_time = round((np.mean(df['Trip Duration']) / 60), 2)
    print("The average trip duration is {} minutes".format(mean_travel_time))

    print("\nThis took %s seconds." % round((time.time() - start_time), 5))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print("The counts of user types are: \n{}\n".format(count_user_type))
    # Display counts of gender
    # Replace NaNs with 'Not specified' and display those too
    try: 
        user_gender = df['Gender'].fillna('Not specified').value_counts()
        print("The gender counts are: \n{}\n".format(user_gender))
        # Display earliest, most recent, and most common year of birth
        year_earliest = int(df['Birth Year'].min())
        print("The earliest birth year is {}".format(year_earliest))
        year_recent = int(df['Birth Year'].max())
        print("The most recent birth year is {}".format(year_recent))
        year_common = int(df['Birth Year'].mode()[0])
        print("The most common birth year is {}".format(year_common))
        # Display for how many users we don't have this data
        year_counts = df['Birth Year'].isna().sum().sum()
        print("No data on the year of birth available for {} users.".format(year_counts))
    # handling the fact that we don't have data about gender and birth year for Washington    
    except KeyError:
        print("There is no data available on gender and birth year for this city.")

    print("\nThis took %s seconds." % round((time.time() - start_time), 5))
    print('-'*40)

def get_raw_data(df):
    """
    prompt the user if they want to see 5 lines of raw data.
    Display the first 5 lines of that data if the answer is 'yes'.
    Continue these prompts and displaying the next 5 lines if the answer continue to be 'yes'.
    Stops if the answer is 'no'.
    """
    # defining 'a' and 'b' to display the raw data as chunks of 5 lines for each iteration
    a = 0
    b = 5
    while True:
        try:
            qa_data = input("Do you want to see the next 5 lines of raw data? Enter 'yes' or 'no': ")
        # ask for restart if user press ctrl+c
        except KeyboardInterrupt:
            restart_qa = input("Would you like to restart? Enter yes or no: ")
            if restart_qa == 'yes':
                continue
            else:
                exit()
        if qa_data == 'yes':
            print(df[a:b])
            a += 5
            b += 5
            continue
        elif qa_data == 'no':
            break
        else:
            print("That's not a valid input. Please try again.")
            continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
