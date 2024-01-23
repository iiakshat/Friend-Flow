import re
import string


# HTML TAGS :
def removeHtml(text):
    pattern = re.compile("<.*?>")
    return pattern.sub(r'', text)

# URLS :
def removeUrl(text):
    p = re.compile(r"https?://\S+|www\.\S+")
    return p.sub(r'', text)

def extractUrl(text):
    p = re.compile(r"https?://\S+|www\.\S+")
    return p.findall(text)

# PUNCTUATION :
exclude = string.punctuation
def removePunc(text):
    text = re.sub(f'[{exclude}]', ' ', text)
    text = re.sub(' +', ' ', text)
    return text

# CONTACTS :
def removeContacts(text):
    p =re.compile(r"[A-z0-9+]*\.vcf\s\([a-z]*\s[a-z]*\)")
    return p.sub(r'', text)
    
# FINAL :
def textPreprocess(messages, stopwords):
    processed_msgs = []
    for i in messages.values:
        html = removeHtml(i.lower())
        link = removeUrl(html)
        punc = removePunc(link)
        final_msg = punc.split()

        for word in final_msg:
            if word not in stopwords:
                processed_msgs.append(word)
                                                        
    return ' '.join(processed_msgs)
