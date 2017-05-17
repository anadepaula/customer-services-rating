#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Author: Ana de Paula, anaspaula17@gmail.com
# Date: may/2017

# coding=utf-8

import os
import json
import sys
import argparse
from time import strftime
from os.path import join, dirname
from watson_developer_cloud import NaturalLanguageUnderstandingV1 \
    as NaturalLanguageUnderstanding
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
import watson_developer_cloud.natural_language_understanding.features.v1 \
    as features
from audio_recorder.recorder import Recorder

ALLOWED_EXTENSIONS = ('wav','flac','ogg','l16','webm','mulaw','basic')
ALLOWED_MODELS = ('ar-AR_BroadbandModel', 'en-UK_BroadbandModel',
'en-UK_NarrowbandModel', 'en-US_NarrowbandModel', 'es-ES_BroadbandModel',
'es-ES_NarrowbandModel', 'fr-FR_BroadbandModel', 'ja-JP_BroadbandModel',
'ja-JP_NarrowbandModel', 'pt-BR_BroadbandModel', 'pt-BR_NarrowbandModel',
'zh-CN_BroadbandModel', 'zh-CN_NarrowbandModel', 'en-US_BroadbandModel')
LANGUAGES=('en','fr','es','pt','ar','zh','ja')
SENTIMENT_KEYWORD_EMOTION=('en')
SENTIMENT_KEYWORD=('fr','es')
SENTIMENT=('pt','ar')
NONE=('zh','ja')

#------------------------------------------------------------------------------#

def get_audio_and_extension(path_to_audio_file):
    if path_to_audio_file == None:
        path_to_audio_file = './recordings/audio_'+strftime("%m-%d-%y_%H:%M:%S")+'.wav'
        recorder = Recorder(path_to_audio_file)
        print("Say something, please.")
        recorder.record_to_file()
        print("Audio recorded!\n")
        extension='wav'

    elif os.path.isfile(path_to_audio_file):
        extension = path_to_audio_file.split('.')
        extension = extension[len(extension)-1]
        if extension not in ALLOWED_EXTENSIONS:
            print ("Your audio file should have one of the following extensions:")
            for i in ALLOWED_EXTENSIONS:
                print('{} '.format(i))
            sys.exit()

    else:
        print("Sorry, the file does not exist! Try again.")
        sys.exit()

    return path_to_audio_file, extension

#------------------------------------------------------------------------------#

def transcribe_audio(audio_file,extension,model):

    if model not in ALLOWED_MODELS:
        print("The specified model is not valid. Try \'python run.py -h\' for help")
        sys.exit()

    username = 'ff833930-186c-473b-bfa0-33987add2831'
    password = '3nS6UxNhOXn5'

    speech_to_text = SpeechToText(
        username=username,
        password=password,
        x_watson_learning_opt_out=False,
    )

    with open(join(dirname(__file__), audio_file), 'rb') as audio:
        result =  speech_to_text.recognize(
            audio,
            content_type='audio/'+extension,
            model=model
        )

    try:
        transcripted_text = result['results'][0]['alternatives'][0]['transcript']
    except:
        print("I'm sorry, the audio is blank! Try again.")
        sys.exit()

    return transcripted_text.rstrip()

#------------------------------------------------------------------------------#

def get_text_data(text,language):

    natural_language_understanding = NaturalLanguageUnderstanding(
        version = '2017-02-27',
        username = '530e87c4-575f-4fbe-9cb0-94e937329e81',
        password = 'To4ZAQZBjUTg'
    )

    return natural_language_understanding.analyze(
        text = text,
        features = [features.Emotion(), features.Sentiment(), features.Keywords()],
        language=language
    )


#------------------------------------------------------------------------------#

def write_in_file(text,text_data):
    #print(json.dumps(text_data, indent=4, sort_keys=True))
    filename = './results/results_'+text_data['language']+'.csv'
    with open (filename,'a') as results_output:
        results_output.write(text)
        if text_data['language'] in NONE:
            print("Watson Developer Cloud does not support natural language "
                "understanding in this language.")

        else:
            sentiments = text_data['sentiment']['document']
            results_output.write((',{},{}'.format(
                sentiments['label'],sentiments['score'])).encode('utf-8'))
            print('The text have a {} feeling, with score of {}.'.format(
                sentiments['label'],sentiments['score']))

            if text_data['language'] in SENTIMENT:
                print("Watson Developer Cloud does not support keyword and emotion "
                    "spotting in this language.")

            else:
                keywords = text_data['keywords']
                keywords_list=[]
                for i in keywords:
                    keywords_list.append(i['text'])
                    print ("'"'{}'"' is in the text with relevance {}.".format(
                        i['text'], i['relevance']))
                    results_output.write((','+';'.join(keywords_list)).encode('utf-8'))
                if text_data['language'] in SENTIMENT_KEYWORD:
                    print("Watson Developer Cloud does not support emotion "
                        "spotting in this language.")
                else:
                    emotions = text_data['emotion']['document']['emotion']
                    for i in emotions.keys():
                        print ("Level of {}: {}".format(i,emotions[i]))
                    results_output.write((',{},{},{},{},{}\n'.format(
                        emotions['anger'],emotions['joy'],emotions['sadness'],
                        emotions['fear'],emotions['disgust'])).encode('utf-8'))

    print("Data saved in '"'{}'"'.".format(filename))

#------------------------------------------------------------------------------#

def main():

    parser = argparse.ArgumentParser(
        description=('Client to process audio using Watson Developer Cloud')
    )
    parser.add_argument(
        '-in', action = 'store', dest='file_path',
        help = 'absolute file path, if an existing audio will be used. '
            'Leave blank for record an audio.'
    )

    parser.add_argument(
        '-model', action = 'store', dest='model',
        default = 'en-US_BroadbandModel',
        help = 'insert one of the following models or leave blank for using '
            '\'en-US_BroadbandModel\': '
            'ar-AR_BroadbandModel, en-UK_BroadbandModel, '
            'en-UK_NarrowbandModel, en-US_NarrowbandModel, '
            'es-ES_BroadbandModel, es-ES_NarrowbandModel, '
            'fr-FR_BroadbandModel, ja-JP_BroadbandModel, '
            'ja-JP_NarrowbandModel, pt-BR_NarrowbandModel, '
            'zh-CN_BroadbandModel, zh-CN_NarrowbandModel'
    )

    args = parser.parse_args()
    audio_file, extension = get_audio_and_extension(args.file_path)

    print("Transcribing audio")
    transcripted_text = (transcribe_audio(audio_file,extension,args.model)).encode('utf-8')
    print('Getting text data')
    transcripted_text_data = get_text_data(transcripted_text,args.model[:2])
    print("Audio text: '"'{}'"'.".format(transcripted_text))
    print("Writing in file")
    write_in_file(transcripted_text,transcripted_text_data)

    print("All done!")

#------------------------------------------------------------------------------#

if __name__ == '__main__':
    try:
        main()
    except:
        sys.exit()
