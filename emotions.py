from nrclex import NRCLex

def getemotions(str):
    text_object = NRCLex(str)
    data = text_object.raw_emotion_scores
    return data

print(getemotions("Today is a really dark and rainy day"))