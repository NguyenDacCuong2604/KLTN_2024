import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


def remove_min_df(X, min_df):
    X = X.fillna('')
    word_counts = {}
    for text in X:
        words = text.split()
        for word in words:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
    filtered_words = {word for word, count in word_counts.items() if count >= min_df}
    return X.apply(lambda x: ' '.join([word for word in x.split() if word in filtered_words]))


class Vectorization:
    def __init__(self):
        self.model_tfidf = TfidfVectorizer()

    def fit_transform(self, X, min_df=0):
        X = remove_min_df(X, min_df)
        return self.model_tfidf.fit_transform(X)

    def get_vector_size(self):
        return len(self.model_tfidf.get_feature_names_out())

    def get_feature_names_out(self):
        return self.model_tfidf.get_feature_names_out()

    def transform(self, X):
        X = X.fillna('')
        return self.model_tfidf.transform(X).toarray()

    def transform_text(self, text):
        return self.model_tfidf.transform([text]).toarray()

    def save_model(self, path_save_model):
        return joblib.dump(self.model_tfidf, path_save_model)

    def load_model(self, path_model):
        self.model_tfidf = joblib.load(path_model)
        return
