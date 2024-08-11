from sklearn.svm import SVC
import joblib


class SVM:
    def __init__(self):
        self.model = SVC()

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

    def load_model(self, path_model):
        self.model = joblib.load(path_model)
        return
