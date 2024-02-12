import text2emotion as t2e

counter = {'Happy': 0, 'Angry': 0, 'Surprise': 0, 'Sad': 0, 'Fear': 0, 'Neutral':0}
def emotionExtracter(emotions):
    for emotion in emotions:
        if emotions[emotion]:
            counter[emotion] += 1
            return
    counter['Neutral'] +=1


def getEmotions(message):
    global counter
    for sentence in message:
        emotionExtracter(t2e.get_emotion(sentence))

    return counter