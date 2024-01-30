def is_ignore_word(message, ignore_list):
    return any(word in message.lower() for word in ignore_list)

def average_reply_time(df, ignore_list):
    ignore_flag = False
    a,b = df['user'].unique()
    try:
        current_user = df.user[0]
    except:
        current_user = df.user[1]
        
    reply_times = { a : [], b : [] }

    null_time = df.date[0] - df.date[0]
    current_user_start_time = df.date[0]
    time_diff = null_time

    for index, row in df.iterrows():
        # Another User
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
                ignore_flag = False

            reply_times[row['user']].append(time_diff.total_seconds() / 60)
            current_user_start_time = row['date']

        # Same user :
        else:
            # Last Message was Bye.
            if ignore_flag:
                ignore_flag = False
                current_user_start_time = row['date']

            # User reply also byee.
            if is_ignore_word(row['message'], ignore_list):
                ignore_flag = True   
            
            reply_times[row['user']].append(0)

    if reply_times:
        reply_time1 = sum(reply_times[a]) / df.shape[0]
        reply_time2 = sum(reply_times[b]) / df.shape[0]

        avg_time = {a : round(reply_time1, 2), 
                    b : round(reply_time2, 2)}
        
        if reply_time1 > reply_time2:
            conclusion = f'{b} replies {round(reply_time1 - reply_time2, 2)} Mins earlier than {a}'
        else:
            conclusion = f'{a} replies {round(reply_time1 - reply_time2, 2)} Mins earlier than {b}'

    else:
        avg_time = 0,0
        conclusion = 'No Messages'

    return avg_time, conclusion

# import pandas as pd

# conversation_data = {
#     'user': ['A', 'A', 'B', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'B'],
#     'message': ['This is the notebook, I was talking about.', "I'll give it to you, read it.", 'Thanks.', 'byee.', 'See you.', 'Hii', 'How was your day?', 'Nice, wbu?', 'Nice.', 'Okay, Byee.', 'Byee'],
#     'date': ['5:00 PM', '5:10 PM', '5:20 PM', '5:25 PM', '5:30 PM', '6:00 PM', '6:30 PM', '6:40 PM', '11:00 PM', '11:10 PM', '11:40 PM'],
#     'date2': ['5:00 PM', '5:10 PM', '5:20 PM', '5:25 PM', '5:30 PM', '6:00 PM', '6:30 PM', '6:40 PM', '11:00 PM', '11:10 PM', '11:40 PM'],
#     'answer': ['0', '0', '20', '0', '10', '0', '30', '10', '260', '10', '0']
# }

# df = pd.DataFrame(conversation_data)
# df['date'] = pd.to_datetime(df['date'])

# ignore_list = ["byee", "bye", "see you", "take care"]

# result = average_reply_time(df, ignore_list)
# print(result)
