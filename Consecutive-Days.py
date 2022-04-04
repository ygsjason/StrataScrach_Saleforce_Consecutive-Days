# Import your libraries
import pandas as pd

# Start writing code
df = sf_events

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
