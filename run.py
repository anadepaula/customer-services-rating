import os
import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NaturalLanguageUnderstanding
import watson_developer_cloud.natural_language_understanding.features.v1 as features

def transcribe_audio():

    speech_to_text = SpeechToText(
        username='ff833930-186c-473b-bfa0-33987add2831',
        password='3nS6UxNhOXn5',
        x_watson_learning_opt_out=False
    )

    with open('./recordings/0001.wav', 'rb') as audio_file:
        return speech_to_text.recognize(
            audio_file, content_type='audio/wav', model='en-US_BroadbandModel')


def get_text_sentiment(text):

    natural_language_understanding = NaturalLanguageUnderstanding(
        version = '2017-02-27',
        username = '530e87c4-575f-4fbe-9cb0-94e937329e81',
        password = 'To4ZAQZBjUTg')

    return natural_language_understanding.analyze(
        text = text,
        features = [features.Emotion(), features.Sentiment(), features.Keywords()])

def main():

    print('Transcribing audio....')
    result = transcribe_audio()
    print('Done!\n')

    text = result['results'][0]['alternatives'][0]['transcript']
    print('Audio text: '"'{}'"'\n'.format(text))

    print('Getting text data...')
    result = get_text_sentiment(text)
    print('Done!\n')

    keywords = {}
    for i in result['keywords']:
        keywords[i['text']] = i['relevance']
    emotions = result['emotion']['document']['emotion']
    sentiments = result['sentiment']['document']


    for word in keywords.keys():
        print ('The expression '"'{}'"' is in the text with relevance {}'.format(
            word, keywords[word]))
    print('\n')

    for element in emotions.keys():
        print ("Level of {}: {}".format(element,emotions[element]))
    print('\n')

    print('The text have, predominantly, a {} feeling, with score of {}\n'.format(
        sentiments['label'],sentiments['score']))


if __name__ == '__main__':

    try:
        main()
    except:
        print('Error etc')
        main()
