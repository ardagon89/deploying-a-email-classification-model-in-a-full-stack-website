from bs4 import BeautifulSoup
from copy import deepcopy
import json
import pandas as pd
import nltk
from nltk.corpus import wordnet
from nltk.tokenize.stanford import StanfordTokenizer
import os
from os import walk
from pathlib import Path
import re
from sklearn.feature_extraction._stop_words import ENGLISH_STOP_WORDS
import string
from users.apps import UsersConfig

def upload_files(files, id):
    Path('users/static/users/uploads/'+str(id)).mkdir(parents=True, exist_ok=True)
    for file in files:
        with open('users/static/users/uploads/'+str(id)+'/'+file.name,'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

def get_results(request):
    wordNetLemmatizer = UsersConfig.wordNetLemmatizer #deepcopy(UsersConfig.wordNetLemmatizer)
    punctuations = list(set(string.punctuation))
    stopWords = ENGLISH_STOP_WORDS.union(['', ' ', 'say', 's', 'u', 'ap', 'afp', '...', 'n', '\\'])

    # Read the dataset to split the data into text and topic
    def readDataset(path):
        topic = []
        text = []

        _, _, files = next(walk(path))
        for file in files:
            with open(path+'\\'+file, 'r', encoding='windows-1252') as f:
                content = f.read()
                topic.append(None)
                text.append(content)
                    
        return text, topic

    # Get the POS tag for each tag
    def getPOSTag(tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return None
            
    # Lemmatize the text
    def lemmatize(text):
        result = []
        for word, tag in text:
            wordnetTag = getPOSTag(tag)
            if wordnetTag is None:
                result.append(wordNetLemmatizer.lemmatize(word))
            else:
                result.append(wordNetLemmatizer.lemmatize(word, pos=wordnetTag))
        return result
        
    # Preprocess the text
    def preprocess(text):
        beautifulSoup = BeautifulSoup(text, "lxml")
        
        # Get the document text
        text = beautifulSoup.get_text()
        
        # Remove special characters which have special meaning
        text = re.sub('<[^>]*>', '', text)
        
        # Tokenize the text
        text = StanfordTokenizer().tokenize(text)
        
        # Convert the tokens to lowercase
        text = [item.lower() for item in text]
        
        # Tag the text with their POS tags
        text = nltk.pos_tag(text)
        
        # Lemmatize the tokens
        text = lemmatize(text)
        
        # Remove the numbers from the tokens
        text = [re.sub('[0-9]+', '', each) for each in text]
        
        # Remove the punctuations from the text
        text = [w for w in text if w not in punctuations]
        
        # Remove the stopwords from the tokens
        text = [w for w in text if w not in stopWords]
        
        return text
        
    # Read the testing dataset
    text, topic = readDataset('users/static/users/uploads/'+str(request.user.id)+'/')
    dfTest = pd.DataFrame([text, topic]).T
    dfTest.columns= ['text', 'topic']

    dfTest['preprocessed_text'] = dfTest['text'].apply(preprocess)
    featuresTest = dfTest['preprocessed_text'].astype('str')

    tfidfVectorizer = UsersConfig.tfidfVectorizer #deepcopy(UsersConfig.tfidfVectorizer)
    featuresTest = tfidfVectorizer.transform(featuresTest)

    truncatedSVD = UsersConfig.truncatedSVD #deepcopy(UsersConfig.truncatedSVD)
    featuresTest = truncatedSVD.transform(featuresTest)

    # Predict the document categories using the trained model
    bestSGDClassifier = UsersConfig.bestSGDClassifier #deepcopy(UsersConfig.bestSGDClassifier)
    dfTest['prediction'] = bestSGDClassifier.predict(featuresTest)

    # Mapping between text categories and their unique IDs
    topicID = {'alt.atheism': 0,
                'comp.graphics': 1,
                'comp.os.ms-windows.misc':2,
                'comp.sys.ibm.pc.hardware':3,
                'comp.sys.mac.hardware':4,
                'comp.windows.x':5,
                'misc.forsale':6,
                'rec.autos':7,
                'rec.motorcycles':8,
                'rec.sport.baseball':9,
                'rec.sport.hockey':10,
                'sci.crypt':11,
                'sci.electronics':12,
                'sci.med':13,
                'sci.space':14,
                'soc.religion.christian':15,
                'talk.politics.guns':16,
                'talk.politics.mideast':17,
                'talk.politics.misc':18,
                'talk.religion.misc':19}

    reverse_topicID = {topicID[key]:key for key in topicID}

    # Map the categories to their ids in the test dataset
    dfTest['category'] = dfTest['prediction'].map(reverse_topicID)

    for f in os.listdir('users/static/users/uploads/'+str(request.user.id)):
        os.remove(os.path.join('users/static/users/uploads/'+str(request.user.id), f))

    json_result = dfTest.reset_index().to_json(orient ='records')
    result = json.loads(json_result)

    return result