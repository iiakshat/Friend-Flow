import re
import pandas as pd

def dateConversion(df):
    df['hr'] = df.date.dt.hour
    df['min'] = df.date.dt.minute
    df['day'] = df.date.dt.day
    df['month'] = df.date.dt.month_name()
    df['year'] = df.date.dt.year

def userSeperator(df):
    usernames = []
    messages = []
    media = []
    pattern = '([\w\W]+?):\s'

    for chat in df['messages']:
        
        content = re.split(pattern, chat)

        if content[1:]:
            usernames.append(content[1])            
            pt = "<Media omitted>"
            st = content[2]
            msg = re.split(pt, st)

            if len(msg)==1:
                media.append(0)
                messages.append(msg[0])

            else:
                media.append(1)
                messages.append(msg[1])


        else:
            usernames.append('Zuckerberg')
            media.append(0)
            messages.append(content[0])
        
    df['message'] = messages
    df['media'] = media
    df['user'] = usernames

def preprocess(filename):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[a-zA-Z]+\s-\s'
    texts = re.split(pattern, filename)[1:]
    dates = re.findall(pattern, filename)

    dic = {
    'messages' : texts,
    'date' : dates
    }

    df = pd.DataFrame(dic)

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p - ')
    dateConversion(df)
    userSeperator(df)

    df.drop(columns=['date','messages'], inplace=True)
    return df

# with open('./Data/flipkart.txt', 'r', encoding='utf-8') as f:
#     t = f.read()

# df = preprocess(t)
# from Stats import counter, most_busy_users

# print(most_busy_users('.',df))
