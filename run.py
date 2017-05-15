import os
import json
from os.path import join, dirname
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NaturalLanguageUnderstanding
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
import watson_developer_cloud.natural_language_understanding.features.v1 as features
from speech_sentiment_python.recorder import Recorder

#------------------------------------------------------------------------------#

def transcribe_audio(path_to_audio_file):

    username = 'ff833930-186c-473b-bfa0-33987add2831'
    password = '3nS6UxNhOXn5'

    speech_to_text = SpeechToText(
        username=username,
        password=password,
        x_watson_learning_opt_out=False
    )

    with open(join(dirname(__file__), path_to_audio_file), 'rb') as audio_file:
        return speech_to_text.recognize(
            audio_file,
            content_type='audio/wav'
        )

#------------------------------------------------------------------------------#

def get_text_data(text):

    natural_language_understanding = NaturalLanguageUnderstanding(
        version = '2017-02-27',
        username = '530e87c4-575f-4fbe-9cb0-94e937329e81',
        password = 'To4ZAQZBjUTg'
    )

    result = natural_language_understanding.analyze(
        text = text,
        features = [features.Emotion(), features.Sentiment(),
                    features.Keywords()]
    )
    return result

#------------------------------------------------------------------------------#

def main():
    recorder = Recorder("speech.wav")

    print("Say something in english, please.")
    recorder.record_to_file()
    print("Audio recorded!\n")


    print("Transcribing audio....")
    result = transcribe_audio('speech.wav')
    print('Done!\n')

    text = result['results'][0]['alternatives'][0]['transcript']
    print('Audio text: '"'{}'"'\n'.format(text))

    print('Getting text data...')
    result = get_text_data(text)
    print('Done!\n')

    keywords = {}
    for i in result['keywords']:
        keywords[i['text']] = i['relevance']
    emotions = result['emotion']['document']['emotion']
    sentiments = result['sentiment']['document']

    for word in keywords.keys():
        print (''"'{}'"' is in the text with relevance {}'.format(
            word, keywords[word]))

    for element in emotions.keys():
        print ("Level of {}: {}".format(element,emotions[element]))

    print('The text have, a {} feeling, with score of {}\n'.format(
        sentiments['label'],sentiments['score']))

#------------------------------------------------------------------------------#

if __name__ == '__main__':
    try:
        main()
    except:
        print("IOError detected, restarting...")
        main()
