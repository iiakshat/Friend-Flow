from datetime import datetime, timedelta
from collections import defaultdict

def is_ignore_word(message, ignore_list):
    return any(word.lower() in message.lower() for word in ignore_list)

def average_reply_time(df, ignore_list):
    df['date'] = pd.to_datetime(df['date'])
    user_timings = {}
    ignore_flag = False
    current_user = 'A'
    reply_times = {}
    null_time = df.iloc[0, 2] - df.iloc[0, 2]
    current_user_start_time = df.iloc[0,2]
    time_diff = null_time

    for index, row in df.iterrows():
        if row['user'] != current_user:
            current_user = row['user']
            time_diff = row['date'] - current_user_start_time

            # Last Message was Bye.
            if ignore_flag:
                ignore_flag = False
                time_diff = null_time
                
            # User reply also byee.
            if is_ignore_word(row['message'], ignore_list):
                ignore_flag = True

            else:
                if row['user'] in reply_times:
                    reply_times[row['user']].append(time_diff.total_seconds() / 60)
                else:
                    reply_times[row['user']] = [time_diff.total_seconds() / 60]
                ignore_flag = False
                current_user_start_time = row['date']

        # same user :
        else:
            # Last Message was Bye.
            if ignore_flag:
                ignore_flag = False
                time_diff = null_time

            # User reply also byee.
            if is_ignore_word(row['message'], ignore_list):
                ignore_flag = True
            

        print(reply_times)

    if reply_times:
        avg_time = sum(reply_times['A']) / len(reply_times), sum(reply_times['B']) / len(reply_times)
    else:
        avg_time = 0

    user_timings[current_user] = {'avg_time': avg_time, 'reply_times': reply_times}
    return user_timings

import pandas as pd

conversation_data = {
    'user': ['A', 'A', 'B', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'B'],
    'message': ['This is the notebook, I was talking about.', "I'll give it to you, read it.", 'Thanks.', 'byee.', 'See you.', 'Hii', 'How was your day?', 'Nice, wbu?', 'Nice.', 'Okay, Byee.', 'Byee'],
    'date': ['5:00 PM', '5:10 PM', '5:20 PM', '5:25 PM', '5:30 PM', '6:00 PM', '6:30 PM', '6:40 PM', '11:00 PM', '11:10 PM', '11:40 PM']
}

df = pd.DataFrame(conversation_data)
df['date'] = pd.to_datetime(df['date'])

ignore_list = ["byee", "bye", "see you", "take care"]

result = average_reply_time(df, ignore_list)
print(result)