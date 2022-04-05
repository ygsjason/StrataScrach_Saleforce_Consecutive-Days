# Import your libraries
import pandas as pd

# Start writing code
df = sf_events

## Method 1
# Sort df by id and date
df = df.sort_values(['user_id', 'date'])

# Find the time different between 2 rows with the group
df['day_diff'] = df.groupby('user_id')['date'].diff().dt.days

# Flag the day_diff is T if day_diff >1
df['flag'] = df.day_diff.gt(1)

# Distinguish different period of consective day
df['t_grp'] = df.flag.cumsum()

# Calculate the Consecutive days across the df
df['cst_day'] = df.groupby(['user_id', 't_grp'])['date'].transform('count')

# Quick way to calculate tp_grp in one line
df['tp_group'] = df.groupby('user_id')['date'].diff().dt.days.gt(1).cumsum()


# Get the id who were active for 3 day in row or more
df3 = df[df['cst_day']>=3]

# Subtract the user_id 
df3.user_id.drop_duplicates()

##Method 2
#De-duplicate the subset and subtract date portion from date column
df1 = df[['user_id', 'date']].drop_duplicates()
df1['date'] = df1.date.dt.date

# Sort df1 by user_id and date
df2 = df1.sort_values(['user_id', 'date'])

# Find the pre-date and pre-pre-date within the group
df2['pre'] = df2.groupby('user_id')['date'].shift(1)

df2['ppre'] = df2.groupby('user_id')['date'].shift(2)

# Check if the user is active for 3 consecutive days
df2['check'] = (df2['date'] - df2['pre']).dt.days
df2['check2'] = (df2['pre'] - df2['ppre']).dt.days

df2[(df2['check'] == 1) & (df2['check2'] == 1)]['user_id']

#df3 = df[['user_id', 'cumday']]
#df3.groupby(['user_id', 'cumday']).size().reset_index(name = 'days')
#df['days'] = df.groupby(['user_id', 'cumday'])['date'].transform('count')
