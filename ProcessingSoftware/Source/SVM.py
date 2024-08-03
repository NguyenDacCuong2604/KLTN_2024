from sklearn.svm import SVC
import joblib


class SVM:
    def __init__(self):
        self.model = SVC(kernel='rbf', gamma='scale', C=1, probability=True)

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        probabilities = self.model.predict_proba(X)
        results = [
            {str(label): float(prob) for label, prob in zip(self.model.classes_, prob_array)}
            for prob_array in probabilities
        ]

        # Sắp xếp các từ điển theo giá trị prob
        sorted_results = [
            dict(sorted(prob_dict.items(), key=lambda item: item[1], reverse=True))
            for prob_dict in results
        ]

        return sorted_results

    def save_model(self, path_save_model):
        return joblib.dump(self.model, path_save_model)

    def load_model(self, path_model):
        self.model = joblib.load(path_model)
        return
