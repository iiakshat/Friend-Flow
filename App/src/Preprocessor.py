import re
import pandas as pd

def dateConversion(df):
    df['Hour'] = df.date.dt.hour
    df['Minute'] = df.date.dt.minute
    df['Day'] = df.date.dt.day
    df['Month'] = df.date.dt.month_name()
    df['Year'] = df.date.dt.year

def userSeperator(df):
    usernames = []
    messages = []
    pattern = '([\w\W]+?):\s'

    for chat in df['messages']:
        
        content = re.split(pattern, chat)

        if content[1:]:
            usernames.append(content[1])
            messages.append(content[2])

        else:
            usernames.append('Zuckerberg')
            messages.append(content[0])
        
    df['message'] = messages
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

# with open('./instance/temp/one-to-one.txt', 'r', encoding='utf-8') as f:
#     t = f.read()

# print(preprocess(t))