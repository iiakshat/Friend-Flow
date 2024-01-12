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