import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


class Vectorization:
    def __init__(self):
        self.model_tfidf = TfidfVectorizer()

    def transform_text(self, text):
        return self.model_tfidf.transform([text]).toarray()

    def load_model(self, path_model):
        self.model_tfidf = joblib.load(path_model)
        return
