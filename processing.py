import argparse
import copy
import os

LANGUAGES = ("en-US","en-UK","fr-FR","es-ES","pt-BR","ar-AR")

def keywords_analysis(keywords_data):
    keyword_dict={}
    phrases_list=[]
    keywords_properties = {"keyword":"",
                           "count":0,
                           "relevance":[]}
    if not os.path.isfile(keywords_data):
        print("There is no data in keywords for this language.")
    else:
        path_to_file = open (keywords_data, 'r')
        for line in path_to_file:
            field = line.split(',')
            for i in field:
                keyword_info=i.split(':')
                if len(keyword_info)==2:
                    print(keyword_info[0])
                    print(keyword_dict.keys())
                    print(keyword_info[0] not in keyword_dict.keys())
                    if keyword_info[0] not in keyword_dict.keys():
                        temp_keyword_dict = copy.deepcopy(keywords_properties)
                        temp_keyword_dict['keyword'] = keyword_info[0]
                        temp_keyword_dict['relevance'].append(float(keyword_info[1]))
                        keyword_dict[keyword_info[0]] = temp_keyword_dict
                    keyword_dict[keyword_info[0]]['count'] +=1
                    print(keyword_info[0] not in keyword_dict.keys())
                    print(keyword_dict[keyword_info[0]]['count'])

                else:
                    phrases_list.append(keyword_info[0])
        print("These are the ratings made: \n\t"+"\n\t".join(phrases_list))
        for i in keyword_dict:
            print("The expression '"'{}'"' was cited {} and its average"
                "relevance is {}.".format(i[""]))


def sentiment_and_emotion_analysis(path_to_file):
    print("hello! come back later, we're not ready yet.")
    '''
    if not os.path.isfile(path_to_file):
        print("There is no data in keywords for this language.")
    else:
        open (path_to_file, 'r') as file:
'''
def main():
    parser = argparse.ArgumentParser(
        description = ("This program analyse the data obtained by"
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
    print(args.language)
    keywords_data = "./results/keywords_{}.csv".format(args.language)
    print(keywords_data)
    sentiment_and_emotion_data = "./results/results_{}.csv".format(args.language)
    keywords_analysis(keywords_data)
    sentiment_and_emotion_analysis(sentiment_and_emotion_data)


if __name__ == '__main__':
    try:
        main()
    except:
        raise
