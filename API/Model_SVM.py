from sklearn.svm import SVC
import joblib
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report


class Model_SVM:
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

    def get_confusion_matrix(self, y_test, y_pred):
        cm = confusion_matrix(y_test, y_pred)
        labels = sorted(list(set(self.model.classes_)))

        # Vẽ biểu đồ ma trận nhầm lẫn
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, xticklabels=labels, yticklabels=labels)
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.show()

    def classification_report(self, y_test, y_pred):
        return classification_report(y_test, y_pred)

    def get_metrics(self, y_test, y_pred):
        # Tính độ chính xác
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy}")

        # Tính độ chính xác dự báo dương (Precision)
        precision = precision_score(y_test, y_pred, average='weighted')
        print(f"Precision: {precision}")

        # Tính khả năng phát hiện đúng (Recall)
        recall = recall_score(y_test, y_pred, average='weighted')
        print(f"Recall: {recall}")

        # Tính điểm F1 (F1 Score)
        f1 = f1_score(y_test, y_pred, average='weighted')
        print(f"F1 Score: {f1}")
