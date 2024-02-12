import base64
from io import BytesIO
from wordcloud import WordCloud
from matplotlib import use
import matplotlib.pyplot as plt

use('Agg')

# Word Cloud :
def wordcloud_Generator(wordcloud):
    
    plt.imshow(wordcloud, interpolation='bilinear', alpha=0.8)
    plt.axis('off')
    graph_data = BytesIO()
    plt.savefig(graph_data, format='png', bbox_inches='tight', pad_inches=0)
    graph_data.seek(0)
    encoded_img = base64.b64encode(graph_data.getvalue()).decode('utf-8')
    graph_html = f'<img src="data:image/png;base64,{encoded_img}" alt="Matplotlib Graph">'
    
    return graph_html


# Simple Plotter : 
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


# Pie Chart Generator :
def generate_encoded_pie_chart(val, labels, explode, colors):
    fig1, ax1 = plt.subplots()
    fig1.set_facecolor('None') 
    ax1.pie(val, colors = colors, labels=labels, autopct='%1.1f%%', 
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

    return graph_html


# Bar Chart Generator :
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