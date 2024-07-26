from sklearn.decomposition import TruncatedSVD
import joblib


class SVD:
    def __init__(self, n_components=600):
        self.svd = TruncatedSVD(n_components=n_components)

    def fit_transform(self, X):
        return self.svd.fit_transform(X)

    def transform(self, X):
        return self.svd.transform(X)

    def save_model(self, path_save):
        return joblib.dump(self.svd, path_save)

    def load_model(self, path_load):
        self.svd = joblib.load(path_load)
        return
