#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Author:   Ana de Paula, anaspaula17@gmail.com
# Date:     may/2017

# coding=utf-8

import argparse
import copy
import os

LANGUAGES = ("en-US","en-UK","fr-FR","es-ES","pt-BR","ar-AR")

#------------------------------------------------------------------------------#

def keywords_analysis(keywords_data):
    if not os.path.isfile(keywords_data):
        print("There is no data in keywords for this language.")
    else:
        keyword_dict={}
        phrases_list=[]
        keywords_properties = {"keyword":"",
                               "count":0,
                               "relevance":[]}
        path_to_file = open (keywords_data, 'r')
        for line in path_to_file:
            field = line.split(',')
            for i in field:
                keyword_info=i.split(':')
                if len(keyword_info)==2:
                    if keyword_info[0] not in keyword_dict.keys():
                        temp_dict = copy.deepcopy(keywords_properties)
                        temp_dict['keyword'] = keyword_info[0]
                        temp_dict['relevance'].append(float(keyword_info[1]))
                        keyword_dict[keyword_info[0]] = temp_dict
                    keyword_dict[keyword_info[0]]['count'] +=1

                else:
                    phrases_list.append(keyword_info[0])
        print("These are the ratings made: \n\t"+"\n\t".join(phrases_list))
        for i in keyword_dict.keys():
            print("The expression '"'{}'"' was cited {} times in the rates and "
                "its average relevance is {}.".format(
                keyword_dict[i]["keyword"],keyword_dict[i]["count"],
                sum(keyword_dict[i]["relevance"])/
                len(keyword_dict[i]["relevance"])))

#------------------------------------------------------------------------------#

def sentiment_and_emotion_analysis(sentiment_and_emotion_data):
    if not os.path.isfile(sentiment_and_emotion_data):
        print("There is no data in sentiments and emotions for this language.")
    else:
        emotion_dict = {"anger":[],
                     "joy":[],
                     "sadness":[],
                     "fear":[],
                     "disgust":[]}
        sentiment=[]
        path_to_file = open (sentiment_and_emotion_data, 'r')
        for line in path_to_file:
            field = line.split(',')
            emotion_dict["anger"].append(float(field[2]))
            emotion_dict["joy"].append(float(field[3]))
            emotion_dict["sadness"].append(float(field[4]))
            emotion_dict["fear"].append(float(field[5]))
            emotion_dict["disgust"].append(float(field[6]))
            sentiment.append(float(field[7]))
        for i in emotion_dict.keys():
            print("The average rate of {} is {}".format(
                i,sum(emotion_dict[i])/len(emotion_dict[i])))
        sentiment_average=sum(sentiment)/len(sentiment)
        print("The average rate of sentiment is {}".format(sentiment_average))
        if sentiment_average > 0:
            print("In general, the rates are positive.")
        elif sentiment_average < 0:
            print("In general, the rates are negative.")
        else:
            print("In general, the rates are neutral.")

#------------------------------------------------------------------------------#

def main():
    parser = argparse.ArgumentParser(
        description = ("This program process the data obtained by"
            "'"'run.py'"'.")
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
    args = parser.parse_args()
    if args.language not in LANGUAGES:
        print ("The indicated language is not allowed. Try "
            "'"'python processing.py --help'"' "
            "for help.")
        sys.exit()
    keywords_data = "./results/keywords_{}.csv".format(args.language)
    sentiment_and_emotion_data = "./results/results_{}.csv".format(args.language)
    keywords_analysis(keywords_data)
    sentiment_and_emotion_analysis(sentiment_and_emotion_data)

#------------------------------------------------------------------------------#

if __name__ == '__main__':
    try:
        main()
    except:
        raise
