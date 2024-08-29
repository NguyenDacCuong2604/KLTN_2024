from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib


class SVM:
    def __init__(self, kernel='rbf', gamma='scale', C=1, probability=True):
        self.kernel = kernel
        self.gamma = gamma
        self.C = C
        self.probability = probability
        self.model = None

        self.validate_parameters()
        self.model = SVC(kernel=self.kernel, gamma=self.gamma, C=self.C, probability=self.probability)

    def validate_parameters(self):
        # Validate kernel
        valid_kernels = ['linear', 'poly', 'rbf', 'sigmoid']
        if self.kernel not in valid_kernels and not callable(self.kernel):
            raise ValueError(f"Invalid kernel: {self.kernel}. Must be one of {valid_kernels} or a callable.")

        # Validate gamma
        if self.gamma not in ['scale', 'auto']:
            if not isinstance(self.gamma, (int, float)) or self.gamma <= 0:
                raise ValueError(f"Invalid gamma: {self.gamma}. Must be 'scale', 'auto', or a positive number.")

        # Validate C
        if not isinstance(self.C, (int, float)) or self.C <= 0:
            raise ValueError(f"Invalid C: {self.C}. Must be a positive number.")

        # Validate probability
        if not isinstance(self.probability, bool):
            raise ValueError(f"Invalid probability: {self.probability}. Must be a boolean.")

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

    def evaluate(self, X_test, y_test):
        predictions = self.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        return accuracy, report
