import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

cache = {}
def counter(user, df):
    global cache
    if user in cache:
        return cache[user]
    
    if user:
        df2 = df[df['user']==user]
        msgs = df2.shape[0]
        words = []
        for sentence in df2['message']:
            words.extend(sentence.split())
        media = sum(df2['media'])
        cache[user] = (msgs, len(words), media)

    else:
        msgs = df.shape[0]
        words = []
        media = sum(df['media']) 
        for sentence in df['message']:
            words.extend(sentence.split())
        cache[user] = (msgs, len(words),media)
    
    return cache[user]

def most_busy_users(suser, df):
    data = round((df['user'].value_counts()/df.shape[0])*100,2)
    data.drop("Zuckerberg",inplace=True)
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
    centre_circle = plt.Circle((0,0),0.70,fc='#DEF5E5')

    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')  
    plt.tight_layout()

    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    encoded_img = base64.b64encode(img_data.getvalue()).decode('utf-8')
    img_html = f'<img src="data:image/png;base64,{encoded_img}" alt="Matplotlib Graph">'
    
    return img_html, name[0], x
    
