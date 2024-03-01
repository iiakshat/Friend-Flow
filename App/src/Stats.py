import emoji
from collections import Counter
from .TextPreprocessor import *
from .ChartGenerator import *
from .Emotions import getEmotions
import base64
from io import BytesIO
from matplotlib import use
import matplotlib.pyplot as plt
from wordcloud import WordCloud

use('Agg')

Links = []


def counter(user, df):
    global Links
    links = []
    queue = []
    longest_msg = ''
    msg_length = 0

    if user:
        df2 = df[df['user']==user]
        msgs = df2.shape[0]
        media = df2['media'].sum()
        
        for sentence in df2['message']:

            if len(sentence) > msg_length:
                longest_msg = sentence
                msg_length = len(longest_msg)

                if len(queue) > 2:
                    queue.pop(0)
                queue.append(longest_msg)

            link = extractUrl(sentence)
            if link:
                links.extend(link)

    else:
        msgs = df.shape[0]
        media = df['media'].sum()

        for sentence in df['message']:

            if len(sentence) > msg_length:
                longest_msg = sentence
                msg_length = len(longest_msg)

                if len(queue) > 2:
                    queue.pop(0)
                queue.append(longest_msg)

            link = extractUrl(sentence)
            if link:
                links.extend(link)

    queue.append(msg_length)
    Links = links.copy()
    return msgs, len(links), media, queue[::-1]


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

    pieChart = generate_encoded_pie_chart(val, name, explode, colors)
    return pieChart, name[0], x
    

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
    wordcloud_img = f'<img src="data:image/png;base64,{encoded_img}" alt="Wordcloud">'
    
    return wordcloud_img, common_words


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

    if selected_user != 'all': df = df[df['user'] == selected_user]

    dates = df['date'].dt.date
    df.loc[:,'date_only'] = dates

    time_df = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    daily_timeline = df.groupby('date_only').count()['message'].reset_index()
    weekly_active = df['day_name'].value_counts()
    monthly_active = df['month'].value_counts()

    time = []
    for i in range(time_df.shape[0]):
        time.append(time_df['month'][i] + " " + str(time_df['year'][i]))

    time_df['time_period'] = time

    # Making Conclusion based on the Activity :
    beg_Date = str(df['date_only'].iloc[0])[-2:]
    beg_Mon = str(df['month'].iloc[0])
    beg_year = str(df['year'].iloc[0])

    if beg_Date == '01':
        beg_Date = '1st'
    elif beg_Date == '02':
        beg_Date = '2nd'
    elif beg_Date == '03':
        beg_Date = '3rd'
    else:
        beg_Date = beg_Date + 'th' if beg_Date[0] != '0' else beg_Date[1] + 'th'

    conclusion1 = f'You all started talking on {beg_Date} of {beg_Mon}, {beg_year}.'  if df['user'].nunique() > 3 else f'You both started talking on {beg_Date} of {beg_Mon}, {beg_year}.'
    average_messages_per_day = df.shape[0] // df['date_only'].nunique()
    active_day =  weekly_active.idxmax()
    active_time = int(df['hr'].value_counts().idxmax())
    if active_time:
        active_time = str(active_time - 12) + " PM" if active_time > 12 else str(active_time) + ' AM'
    else:
        active_time = '12 AM'

    if selected_user != 'all':
        conclusion2 = f''' {selected_user} does {average_messages_per_day} Messages a day, {round(df['message'].apply(len).mean(), 2)} Characters long 
                        and mostly texts on {active_day} at {active_time}. '''
        
    else:
        conclusion2 = f''' Both of you send an average of {average_messages_per_day} Messages a day, 
                            and mostly texts on {active_day} at {active_time}. '''

    conclusion = conclusion1 + conclusion2

    # Enoding the Graphs for HTML :
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


# Emotions or Chat Mood detector (Best suited for English Chats) :
def emotions(selected_user, df):
    if selected_user != 'all': df = df[df['user'] == selected_user]

    Emotions = getEmotions(df['message'])
    val = list(Emotions.values())
    labels = Emotions.keys()
    explode = [0.07, 0, 0, 0, 0, 0]
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#9376e0', '#ff74b1']
    if val[-1] > 0.5 * sum(val):
        return generate_encoded_pie_chart(val[:-1], labels[:-1], explode[:-1], colors[:-1])

    pieChart = generate_encoded_pie_chart(val, labels, explode, colors)
    return pieChart