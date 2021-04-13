from django.apps import AppConfig
import joblib
import nltk
from nltk.stem import WordNetLemmatizer
import os

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Put the POS tagger in the classpath
    os.environ['CLASSPATH'] = "singularity/bin/stanford-postagger.jar"

    # Download the required models
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)

    bestSGDClassifier = joblib.load("users/static/users/models/model.jbl")
    tfidfVectorizer = joblib.load("users/static/users/models/tfidfVectorizer.jbl")
    truncatedSVD = joblib.load("users/static/users/models/truncatedSVD.jbl")
    wordNetLemmatizer = WordNetLemmatizer()
    wordNetLemmatizer.lemmatize('apple')

    def ready(self):
        import users.signals