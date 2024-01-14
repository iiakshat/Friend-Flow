import re
import string


# HTML TAGS :
def removeHtml(text):
    pattern = re.compile("<.*?>")
    return pattern.sub(r'', text)


# URLS :
def removeUrl(text):
    p =re.compile(r"https?://\S+|www\.\S+")
    return p.sub(r'', text)

# PUNCTUATION :
exclude = string.punctuation
def removePunc(text):
    return text.translate(str.maketrans('','', exclude))


# FINAL :
def textPreprocess(messages, stopwords):
    processed_msgs = []
    for i in messages.values:
        html = removeHtml(i)
        link = removeUrl(html)
        punc = removePunc(link)
        final_msg = punc.lower().split()

        for word in final_msg:
            if word not in stopwords:
                processed_msgs.append(word)

    return ' '.join(processed_msgs)
