import os
import json
import sys
import argparse
import shutil
from time import strftime
from os.path import join, dirname
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NaturalLanguageUnderstanding
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
import watson_developer_cloud.natural_language_understanding.features.v1 as features
from audio_recorder.recorder import Recorder

ALLOWED_EXTENSIONS = ('wav','flac','ogg','l16','webm','mulaw','basic')

#------------------------------------------------------------------------------#

def get_audio_and_extension(path_to_audio_file):
    print("I'm here!")

    if path_to_audio_file == None:
        print('none')
        audio_file = './recordings/audio_'+strftime("%m-%d-%y_%H:%M")+'.wav'
        recorder = Recorder(audio_file)
        print("Say something in english, please.")
        recorder.record_to_file()
        print("Audio recorded!\n")
        extension='wav'

    elif os.path.isfile(path_to_audio_file):
        print('the file exists!')
        if not os.path.dirname(path_to_audio_file)=='./recordings':
            print('the file is not in recordings')
            '''
            try:
                shutil.copy(path_to_audio_file,'./recordings/')
            except:
                print("Sorry, cant copy the file! Try again.")
                raise
            '''
            shutil.copy(path_to_audio_file,'./recordings/'+path_to_audio_file+)
        audio_file = path_to_audio_file.split('/')
        audio_file = './recordings/' + audio_file(len(audio_file)-1)
        extension = path_to_audio_file.split('.')
        extension = extension(len(extension)-1)

        if extension not in ALLOWED_EXTENSIONS:
            print ("You should insert a valid audio file!")
            sys.exit()

    else:
        print("Sorry, the file does not exist! Try again.")
        sys.exit()

    return audio_file, extension

#------------------------------------------------------------------------------#

def transcribe_audio(audio_file,extension):

    username = 'ff833930-186c-473b-bfa0-33987add2831'
    password = '3nS6UxNhOXn5'

    speech_to_text = SpeechToText(
        username=username,
        password=password,
        x_watson_learning_opt_out=False
    )

    with open(join(dirname(__file__), audio_file), 'rb') as audio_file:
        return speech_to_text.recognize(
            audio_file,
            content_type='audio/'+extension
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
    # parse command line parameters
    parser = argparse.ArgumentParser(
        description=('client to process audio using Watson Developer Cloud')
    )
    parser.add_argument(
        '-in', action = 'store', dest='file_path',
        #default = './recordings/audio_'+strftime("%m-%d-%y_%H:%M")+'.wav',
        help = 'absolute file path, if an existing audio will be used.'
    )
    '''
    parser.add_argument(
        '-model', action = 'store', dest='model',
        default = 'en-US_BroadbandModel',
        help = 'insert the model, according to the sample rate and language.'
    )
    '''

    args = parser.parse_args()
    print(args)

    audio_file, extension = get_audio_and_extension(args.file_path)

    print(audio_file)
    print(extension)

    print("Transcribing audio....")
    transcription_result = transcribe_audio(audio_file,extension)
    print('Done!\n')

    try:
        transcripted_text = transcription_result['results'][0]['alternatives'][0]['transcript']
    except:
        print("I'm sorry, the audio is blank! Try again.")
        sys.exit()

    print('Audio text: '"'{}'"'\n'.format(transcripted_text))

    print('Getting text data...')
    language_processing_result = get_text_data(transcripted_text)
    print('Done!\n')

    keywords = {}
    for i in language_processing_result['keywords']:
        keywords[i['text']] = i['relevance']
    emotions = language_processing_result['emotion']['document']['emotion']
    sentiments = language_processing_result['sentiment']['document']

    for word in keywords.keys():
        print (''"'{}'"' is in the text with relevance {}'.format(
            word, keywords[word]))

    for element in emotions.keys():
        print ("Level of {}: {}".format(element,emotions[element]))

    print('The text have a {} feeling, with score of {}\n'.format(
        sentiments['label'],sentiments['score']))

    with open ('results/emotions.csv','a') as emotions_output:
        emotions_output.write('{},{},{},{},{},{}.{},{}\n'.format(
            args.file_path,emotions['anger'],emotions['joy'],
            emotions['sadness'],emotions['fear'],emotions['disgust'],
            sentiments['label'],sentiments['score']))

    with open ('results/keywords.csv','a') as keywords_output:
        keywords_output.write('{}'.format(args.file_path))
        for keyword in keywords.keys():
            keywords_output.write(';{}'.format(keyword))
        keywords_output.write('\n')

#------------------------------------------------------------------------------#

if __name__ == '__main__':
    try:
        main()
    except:
        sys.exit()
