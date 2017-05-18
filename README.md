# Customer services rate using Watson Developer Cloud

## About

The program was designed to be used in customer services rating; after the service, the customer should talk about its experience.
In this case, the audio recorded would be sent to the Speech-To-Text services for transcription, and the transcription would be sent the Natural Language Understanding services to be analyzed in three dimensions:
* sentiment, an scale between -1 and 1 indicating the level of positivity, where -1 is absolutely negative and is absolutely positive
* emotions, where the level of five emotions (joy, sadness, fear, anger and disgust) would be indicated between 0 and 1;
* keyword spotting, where the most important expressions are indicated with a level of relevance between 0 and 1.


## Using

Is mandatory to install the requirements listed in `requirements.txt`. This can be done using `pip` with:
`pip install -r requirements.txt`

Is required to set a dotenv with the credentials for the Speech-to-text and Natural Language Understanding services in the format:

        `BLUEMIX-STT-USERNAME=speech-to-text_user`
        `BLUEMIX-STT-PASSWORD=speech-to-text_password`
        `BLUEMIX-NLU-USERNAME=natural-language-understanding_user`
        `BLUEMIX-NLU-PASSWORD=natural-language-understanding_password`

The program can make the analysis in a role of languages and audio formats, in case of existing files. By default, the language is US english and the audio is recorded when the running begins. It is possible to change this using the flags `-in FILE_PATH` and `-language LANGUAGE`. The available languages and audio extensins are descripted below. Also, it is possible to see the options with the flag `-h|--help`.


**Allowed extensions**:
`wav`, `flac`, `ogg`, `l16`, `webm`, `mulaw`, `basic`


**Available languages:**

Flag name | Language
----------|---------
blank (default) | US english
en-UK | UK english
fr-FR | french
es-ES | spanish
pt-BR | brazilian portuguese
ar-AR | arabic


The results are saved in `.csv` files in the directory `./results/`. They can be analyzed running the program `processing.py`. As before, the language can be defined with the `- language` flag. The analysis shows informations about the ratings made: keywords counting, with relevance rate, and average sentiments and emotions level.


This program was developed by
[Ana de Paula](https://github.com/anadepaula)
in may,2017.
