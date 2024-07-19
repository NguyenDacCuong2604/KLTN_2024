from Code.Model_SVM import Model_SVM
from Code.Vectorization import Vectorization
import pandas as pd

from Code.VietnameseTextPreprocessor import VietnameseTextPreprocessor

if __name__ == "__main__":

    path_file_test = '../Dataset/Root/test_singlelabel.csv'
    df = pd.read_csv(path_file_test)
    X_test = df['Trích yếu']
    y_test = df['ID phòng xử lý']
    #Tiền xử lý
    vietnameseTextPreprocessor = VietnameseTextPreprocessor()
    X_test_preprocessing = X_test.apply(lambda x: vietnameseTextPreprocessor.process_text(x))

    #Test trường hợp stopwords chưa thêm các từ DF top
    vectorization_1 = Vectorization()
    vectorization_1.load_model('../Model/tfidf_v1.model')

    X_test_vector_v1 = vectorization_1.transform(X_test_preprocessing)

    model_svm_v1 = Model_SVM()
    model_svm_v1.load_model('../Model/svm_v1.model')

    y_pred_v1 = model_svm_v1.predict(X_test_vector_v1)

    model_svm_v1.get_metrics(y_test, y_pred_v1)

    model_svm_v1.get_confusion_matrix(y_test, y_pred_v1)

    # Test trường hợp stopwords chứa các từ DF top
    vectorization_2 = Vectorization()
    vectorization_2.load_model('../Model/tfidf_v2.model')

    X_test_vector_v2 = vectorization_2.transform(X_test_preprocessing)

    model_svm_v2 = Model_SVM()
    model_svm_v2.load_model('../Model/svm_v2.model')

    y_pred_v2 = model_svm_v2.predict(X_test_vector_v2)

    model_svm_v2.get_metrics(y_test, y_pred_v2)

    model_svm_v2.get_confusion_matrix(y_test, y_pred_v2)