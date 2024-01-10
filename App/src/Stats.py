def messages(user, df):
    if user:
        df2 = df[df['user']==user]
        msgs = df2.shape[0]
        words = []
        for sentence in df2['message']:
            words.extend(sentence.split())
        return msgs, len(words)

    else:
        msgs = df.shape[0]
        words = []
        for sentence in df['message']:
            words.extend(sentence.split())
        return msgs, len(words)
