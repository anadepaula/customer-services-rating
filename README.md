# Customer Services Rating using Watson Developer Cloud

## About

The program was designed to be used in customer services rating; after the service, the customer should talk about its experience.
In this case, the audio recorded would be sent to the Speech-To-Text services for transcription, and the transcription would be sent the Natural Language Understanding services to be analyzed in three categories:
* sentiment, an scale between -1 and 1 indicating the level of positivity, where -1 is absolutely negative and is absolutely positive
* emotions, where the level of five emotions (joy, sadness, fear, anger and disgust) would be indicated between 0 and 1;
* keyword spotting, where the most important expressions are indicated with a level of relevance between 0 and 1.


## Using

### Requirements

Is mandatory to install the requirements listed in `requirements.txt`. This can be done using `pip` with:
`pip install -r requirements.txt`

Is required to set a dotenv with the credentials for using the Watson Developer Cloud Services. For getting these, you should register on [Bluemix](https://www.ibm.com/watson/developercloud), create the Speech-To-Text and Natural Language Understanding APIs and get the credentials. The dotenv file should follow this model:

        `BLUEMIX-STT-USERNAME=speech-to-text_user`
        `BLUEMIX-STT-PASSWORD=speech-to-text_password`
        `BLUEMIX-NLU-USERNAME=natural-language-understanding_user`
        `BLUEMIX-NLU-PASSWORD=natural-language-understanding_password`

### Languages

The program can make the analysis in a role of languages. Therefore, the three categories are supported only in english, the other languages can be used, but will be made an parcial analysis. The default language is US english, but this can be changed by using the flag `-language LANGUAGE`, where `LANGUAGE`

**Available languages:**

Code for the `-language` flag | Language | Supported categories
----------|----------|---------------------
none (default) | US english | sentiment, keyword and emotion
en-UK | UK english | sentiment, keyword and emotion
es-ES | spanish | sentiment and keyword spotting
fr-FR | french | sentiment and keyword spotting
pt-BR | brazilian portuguese | sentiment
ar-AR | arabic | sentiment

### Audio
The analysis is based in audio files. The audio files can be recorded on running the program or can be uploaded. By default,  the audio is recorded when the running begins. It is possible to change this using the flag `-in FILE_PATH`, where `FILE_PATH` is the path of the audio file. The allowed audio extensins are `wav`, `flac`, `ogg`, `l16`, `webm`, `mulaw`, `basic`


When recording an audio, is important to stay in a quiet place, otherwise the audio quality may not be good. The audio is recorded automatically -- the programs detects the silence after the speech and interrupts the recording; then, it is better to avoid long pauses.


### Flags

The flag `-h|--help` can be used to show the instructions to change the language or to input a existing file audio.

## Results

The results are saved in `.csv` files in the directory `./results/`. They can be analyzed running the program `processing.py`. As before, the language can be defined with the `-language` flag, and the default is US english. The analysis shows informations about the ratings made: keywords counting, with relevance rate, and average sentiments and emotions level.


This program was developed by
[Ana de Paula](https://github.com/anadepaula)
in may,2017.
