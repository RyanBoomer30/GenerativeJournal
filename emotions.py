from nrclex import NRCLex

def getemotions(str):
    text_object = NRCLex(str)
    data = text_object.raw_emotion_scores
    return data

print(getemotions("The times are difficult! Our sales have been disappointing for the past three quarters for our data analytics product suite. We have a competitive data analytics product suite in the industry. However, we are not doing a good job at selling it, and this is really frustrating."))