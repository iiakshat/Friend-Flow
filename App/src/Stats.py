import base64
from io import BytesIO
from wordcloud import WordCloud
from .TextPreprocessor import *
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import emoji

links = []

def counter(user, df):
    global links
    if user:
        longest_msg = ''
        df2 = df[df['user']==user]
        msgs = df2.shape[0]
        media = df2['media'].sum()
        
        for sentence in df2['message']:
            if len(sentence) > len(longest_msg):
                longest_msg = sentence
            link = extractUrl(sentence)
            if link:
                links.extend(link)

        return msgs, len(links), media, longest_msg

    else:
        longest_msg = ''
        msgs = df.shape[0]
        media = df['media'].sum()

        for sentence in df['message']:
            if len(sentence) > len(longest_msg):
                longest_msg = sentence
            link = extractUrl(sentence)
            if link:
                links.extend(link)

        return msgs, len(links), media, longest_msg


def most_busy_users(suser, df):
    data = round((df['user'].value_counts()/df.shape[0])*100,2)
    try:
        data.drop("Zuckerberg",inplace=True)
    except:
        print('You have no whatsapp notifications.')
    x = ''

    if len(df['user'].unique()) < 4:
        ff = data
        name = ff.index.tolist()
        val = ff.tolist()
        explode = [0.07, 0]
        colors = ['#D2E0FB', '#8EACCD']

    else:
        x = data.get(suser)
        ff = data.head(5)
        name = ff.index.tolist()
        val = ff.tolist()

        rem = 100-sum(val)
        explode = [0.07, 0, 0, 0, 0, 0]
        
        name.append('Others')
        val.append(rem)
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#9376e0', '#ff74b1']

    fig1, ax1 = plt.subplots()
    fig1.set_facecolor('None') 
    ax1.pie(val, colors = colors, labels=name, autopct='%1.1f%%', 
            startangle=90, pctdistance=0.85, explode = explode)
    centre_circle = plt.Circle((0,0),0.70,fc='none')

    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')  
    plt.tight_layout()

    graph_data = BytesIO()
    plt.savefig(graph_data, format='png', transparent=True)
    graph_data.seek(0)
    encoded_img = base64.b64encode(graph_data.getvalue()).decode('utf-8')
    graph_html = f'<img src="data:image/png;base64,{encoded_img}" alt="Matplotlib Graph">'
    return graph_html, name[0], x
    

def frequent_words(df, selected_user):
    with open('././Data/stopwords.txt', 'r') as f:
        stopwords = f.read()

    if selected_user:
        new_df = df[df['user']==selected_user]

    else:
        new_df = df[df['user']!='Zuckerberg']


    ''' Null is common message for notifications like 
        missed video call, opened (when a media is shared
        in one time view and other party views.), etc.'''

    new_df = new_df[~new_df['message'].isin(['<Media omitted>\n', 
                                             'This message was deleted\n',
                                             'You deleted this message\n',
                                             'null\n', '\n'
                                             ])]

    total_words = textPreprocess(new_df['message'], stopwords)

    #   Whenever a user shares a contact with a friend the contact is 
    #   shared as contact.vsf file. We don't want this to be considered
    #   for analysis, so we'll have to remove this.

    if len(total_words) < 4:
        return None, {}
    
    final = removeContacts(' '.join(total_words))
    common_words = Counter(final.split(' '))


    wordcloud = WordCloud(width=500, 
                   height=500, 
                   scale=3, 
                   min_font_size=10,
                   background_color=None,
                   mode="RGBA",
                   contour_width=0,
                   contour_color='transparent',
                   collocations=False).generate(final)

    plt.imshow(wordcloud, interpolation='bilinear', alpha=0.8)
    plt.axis('off')
    graph_data = BytesIO()
    plt.savefig(graph_data, format='png', bbox_inches='tight', pad_inches=0)
    graph_data.seek(0)
    encoded_img = base64.b64encode(graph_data.getvalue()).decode('utf-8')
    graph_html = f'<img src="data:image/png;base64,{encoded_img}" alt="Matplotlib Graph">'

    return graph_html, common_words


def most_common_emoji(selected_user,df):
    if selected_user:
        df = df[df['user'] == selected_user]

    all_emojis = set(emoji.EMOJI_DATA)

    emojis = []
    for message in df['message']:
        emojis.extend([i for i in message if i in all_emojis])

    top_emojis = {}
    for i in Counter(emojis).most_common(5):
        top_emojis[emoji.emojize(i[0])] = i[1]
    return top_emojis

def activity(selected_user,df):

    if selected_user != 'all':
        df = df[df['user'] == selected_user]

    df['date_only'] = df['date'].dt.date

    time_df = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    daily_timeline = df.groupby('date_only').count()['message'].reset_index()
    weekly_active = df['day_name'].value_counts()
    monthly_active = df['month'].value_counts()

    time = []
    for i in range(time_df.shape[0]):
        time.append(time_df['month'][i] + " " + str(time_df['year'][i]))

    time_df['time_period'] = time

    # Making Conclusion based on the Activity :
    beginning = time_df.iloc[0,3]
    ending = time_df.iloc[time_df.shape[0]-1,3]
    st_month = int(time_df.iloc[0,1])
    end_month = int(time_df.iloc[time_df.shape[0]-1,1])
    gap_m = abs(st_month - end_month)
    gap_m = str(gap_m) + ' Months' if gap_m else ''
    gap_y = int(time_df.iloc[time_df.shape[0]-1,0]) - int(time_df.iloc[0,0])

    if beginning > ending:
        if selected_user != 'all':
            conclusion = f"{selected_user} lost their interest from {beginning} to {ending} messages in {gap_y} Years {gap_m}"

        else:
            if df.user.unique().shape[0] <4:
                selected_user = 'Both of you lost your'
            else:
                selected_user = 'All the users lost their'
            conclusion = f"{selected_user} interest from {beginning} to {ending} messages in {gap_y} Years {gap_m}"
            
    else:
        if selected_user != 'all':
            conclusion = f"{selected_user} gained interest from {beginning} to {ending} messages in {gap_y} Years {gap_m} "
        
        else:
            if df.user.unique().shape[0] <4:
                selected_user = 'Both of you'
            else:
                selected_user = 'All the users'
            conclusion = f"{selected_user} gained interest from {beginning} to {ending} messages in {gap_y} Years {gap_m}"

    time_df_img = generate_encoded_image(time_df, 'Monthly Activity', 'time_period', 'message', 'No. of Messages', 'Time Period')
    daily_timeline_img = generate_encoded_image(daily_timeline, 'Daily Activity', 'date_only', 'message', 'No. of Messages', 'Time Period')
    weekly_active_img = generate_encoded_bar_chart(weekly_active, 'Users Active Weekly', 'Days', 'No. of Messages')
    monthly_active_img = generate_encoded_bar_chart(monthly_active, 'Users Active Monthly', 'Months', 'No. of Messages')

    graphs = {'month_wise': time_df_img, 
              'daily' : daily_timeline_img, 
              'weekly' : weekly_active_img,
              'monthly' : monthly_active_img, 
              'conclusion' : conclusion}

    return graphs


def generate_encoded_image(df, title, x_col, y_col, y_label, x_label):
    fig, ax = plt.subplots()
    ax.plot(df[x_col], df[y_col], color='white')
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.xticks(rotation='vertical')
    plt.tight_layout()

    graph_data = BytesIO()
    plt.savefig(graph_data, format='png', transparent=True)
    graph_data.seek(0)
    encoded_img = base64.b64encode(graph_data.getvalue()).decode('utf-8')
    graph_html = f'<img src="data:image/png;base64,{encoded_img}" alt="Matplotlib Graph">'
    
    return graph_html

def generate_encoded_bar_chart(series, title, x_label, y_label):
    fig, ax = plt.subplots()
    ax.bar(series.index, series.values, color='white')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()

    graph_data = BytesIO()
    plt.savefig(graph_data, format='png', transparent=True)
    graph_data.seek(0)
    encoded_img = base64.b64encode(graph_data.getvalue()).decode('utf-8')
    graph_html = f'<img src="data:image/png;base64,{encoded_img}" alt="Matplotlib Graph">'

    return graph_html
