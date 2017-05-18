#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Author:   Ana de Paula, anaspaula17@gmail.com
# Date:     may/2017

# coding=utf-8

import os
import json
import sys
import argparse
from time import strftime
from shutil import copyfile
from dotenv import load_dotenv
from os.path import join, dirname
import watson_developer_cloud.natural_language_understanding.features.v1 \
    as features
from watson_developer_cloud import NaturalLanguageUnderstandingV1 \
    as NaturalLanguageUnderstanding
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from audio_recorder.recorder import Recorder

# List of the allowed file extensions
ALLOWED_EXTENSIONS = ("wav","flac","ogg","l16","webm","mulaw","basic")

# Dictionary mapped by the languages' short name containing:
#   - the model name, for use in the Speech To Text API
#   - the supported categories of the language in the Natural language
#     understanding API.
LANGUAGES = {
    "en-US":{"model":"en-US_BroadbandModel",
        "supported_categories":("sentiment","keyword","emotion")},
    "en-UK":{"model":"en-UK_NarrowbandModel",
        "supported_categories":("sentiment","keyword","emotion")},
    "fr-FR":{"model":"fr-FR_BroadbandModel",
        "supported_categories":("sentiment","keyword")},
    "es-ES":{"model":"es-ES_NarrowbandModel",
        "supported_categories":("sentiment","keyword")},
    "pt-BR":{"model":"pt-BR_NarrowbandModel",
        "supported_categories":("sentiment")},
    "ar-AR":{"model":"ar-AR_BroadbandModel",
        "supported_categories":("sentiment")}
}

#------------------------------------------------------------------------------#
# Copy or record an audio file into the './recordings/' directory, depending
# on 'file input':
#   None: record an '.wav' as 'recorded_audio_m-d-y_H:M:S_LANGUAGE.wav';
#   Valid path: copy as 'copied_FILENAME_LANGUAGE_m-d-y_H:M:S.EXTENSION'
#               verify if the extension is one of the accepted by the
#               Speech To Text API.
def get_audio_and_extension(file_input,language):
    if file_input:
        file_data = (file_input.split("/"))
        file_data = file_data[len(file_data)-1]
        file_data = file_data.split(".")
        filename = file_data[0]
        extension = file_data[len(file_data)-1]
        if extension not in ALLOWED_EXTENSIONS:
            print ("Your audio file should be in of the following "
                "formats:\n\t{}".format("\n\t".join(ALLOWED_EXTENSIONS)))
            sys.exit()
        audio_file = "./recordings/copied_{}_{}_{}.{}".format(
            filename,language,strftime("%m-%d-%y_%H:%M:%S"),extension)
        try:
            copyfile(file_input, audio_file)
        except IOError:
            print ("Please, put the project in a writable directory.")
    else:
        audio_file = "./recordings/recorded_audio_{}_{}.wav".format(
            language,strftime("%m-%d-%y_%H:%M:%S"))
        recorder = Recorder(audio_file)
        print("Say something, please.")
        recorder.record_to_file()
        print("Audio recorded!")
        extension = "wav"
    return audio_file, extension

#------------------------------------------------------------------------------#

# Receives an valid audio file, its extension and a  valid model, send it to
# the Speech To Text services and receives a JSON with the transcription.
# Returns the transcripted audio.
# It may not recognize the speaking if:
#   there is no speaking;
#   the sample rate is below the one required by the model;
#   the voices are too low or the ambient is noisy.
# In any of those cases, the program is interrupted.

def transcribe_audio(audio_file, extension, model):

    username = os.environ.get("BLUEMIX-STT-USERNAME")
    password = os.environ.get("BLUEMIX-STT-PASSWORD")

    speech_to_text = SpeechToText(
        username = username,
        password = password,
        x_watson_learning_opt_out = False,
    )
    with open(audio_file, "rb") as audio:
        try:
            result = speech_to_text.recognize(
                audio,
                content_type = "audio/" + extension,
                model = model
            )
        except Exception as ex:
            print(ex)
            raise
    #print(json.dumps(result, indent=4, sort_keys=True))
    try:
        transcripted_text = result["results"][0]["alternatives"][0]["transcript"]
    except:
        print("I'm sorry, the audio is blank! If youre sure that there was"
            "an audio, it probably was below the microphone sensibility. Try "
            "speaking louder.")
        raise
    return transcripted_text.rstrip()

#------------------------------------------------------------------------------#

# Receives the transcripted text and its language and send it to the
# Natural Language Understanding services, receives back a JSON with
# the data and return it.
# The text is analyzed in three dimensions:
#   keywords spotting
#   emotions
#   sentiment
def get_text_data(text,language):

    natural_language_understanding = NaturalLanguageUnderstanding(
        version = "2017-02-27",
        username = os.environ.get("BLUEMIX-NLU-USERNAME"),
        password = os.environ.get("BLUEMIX-NLU-PASSWORD")
    )
    return natural_language_understanding.analyze(
        text = text,
        features = [features.Emotion(), features.Sentiment(), features.Keywords()],
        language = language
    )


#------------------------------------------------------------------------------#
# Receives the JSON string returned from the method 'get_text_data', split it
# according to the dimensions and saves the data in .csv files at the
# directory './results'. Shows information about the text in the screen.

def write_in_file(text,text_data,language):
    #print(json.dumps(text_data, indent=4, sort_keys=True))
    results_output = open("./results/results_" + language + ".csv",'a')
    keywords_output = open("./results/keywords_" + language + ".csv",'a')
    print("Audio text: '"'{}'"'.".format(text))
    sentiments = text_data["sentiment"]["document"]
    results_output.write(("{},{},{}".format(
        text, sentiments["label"], sentiments["score"])).encode("utf-8"))
    keywords_output.write(("{}".format(text)).encode("utf-8"))
    print("The text have a {} feeling, with score of {}.".format(
        sentiments["label"], sentiments["score"]))
    if "keyword" not in LANGUAGES[language]["supported_categories"]:
        print("Watson Developer Cloud does not support keyword and emotion "
            "spotting in this language.")
    else:
        keywords = text_data["keywords"]
        for i in keywords:
            keywords_output.write(",{}:{}".format(
                i["text"], i["relevance"]).encode("utf-8"))
            print ("'"'{}'"' is in the text with relevance {}.".format(
                i["text"], i["relevance"]))
        if "emotion" not in LANGUAGES[language]["supported_categories"]:
            print("Watson Developer Cloud does not support emotion "
                "spotting in this language.")
        else:
            emotions = text_data["emotion"]["document"]["emotion"]
            for i in emotions.keys():
                print ("Level of {}: {}".format(i, emotions[i]))
            results_output.write((",{},{},{},{},{}".format(emotions["anger"],
                emotions["joy"],emotions["sadness"],emotions["fear"],
                emotions["disgust"])).encode("utf-8"))
    keywords_output.write("\n")
    results_output.write("\n")
    keywords_output.close()
    results_output.close()

#------------------------------------------------------------------------------#

def main():
    # Parsing args
    parser = argparse.ArgumentParser(
        description = ("This program was made to process audio data using "
        "the Watson Developer Cloud's APIs '"'Speech To Text'"' and "
        "'"'Natural Language Understanding'"'. The program was designed "
        "to be used in customer services rating.")
    )
    parser.add_argument(
        "-in", action = "store", dest = "file_path",
        help = "absolute file path, if an existing audio will be used. "
            "Leave blank for record an audio."
    )
    parser.add_argument(
        "-language", action = "store", dest = "language", default = 'en-US',
        help = "insert one of the following languages or leave blank "
            "for using US english: "
            "'"'en-UK'"' for UK english, "
            "'"'fr-FR'"' for french, "
            "'"'es-ES'"' for spanish, "
            "'"'pt-BR'"' for brazilian portuguese or "
            "'"'ar-AR'"' for arabic. "
    )
    # Treating the args
    args = parser.parse_args()
    if args.language not in LANGUAGES.keys():
        print ("The indicated language is not allowed. Try "
            "'"'python run.py --help'"' "
            "for help.")
        sys.exit()
    if args.file_path and not os.path.isfile(args.file_path):
        print("Sorry, the file does not exist! Try again.")
        sys.exit()

    model = LANGUAGES[args.language]["model"]
    language = args.language
    # Handle audio data
    audio_file, extension = get_audio_and_extension(args.file_path,language)
    # Transcripting audio with the Speech To Text API
    print("Transcribing audio.")
    text = (transcribe_audio(audio_file,extension,model)).encode('utf-8')
    # Processing the audio with the Natural Language Understanding API
    print('Getting text data.')
    text_data = get_text_data(text,language[:2])
    # Writing data in the files
    print("Writing in file.")
    write_in_file(text,text_data,language)
    print("That's all! Thank you.")

#------------------------------------------------------------------------------#

if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    try:
        main()
    except:
        raise
