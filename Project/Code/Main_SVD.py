from Code.Model_SVM import Model_SVM
from Code.SVD import SVD
from Code.Vectorization import Vectorization
import pandas as pd

from Code.VietnameseTextPreprocessor import VietnameseTextPreprocessor

if __name__ == "__main__":
    #v1
    path_data_train = '../Dataset/Root/data_preprocessing_v2.csv'
    path_save_model_vector = '../Model/tfidf_v2.model'
    df = pd.read_csv(path_data_train)

    X_train = df['input']
    y_train = df['label']

    vectorization = Vectorization()
    vectorization.load_model('../Model/tfidf_v2.model')
    X_train_vector = vectorization.transform(X_train)

    svd = SVD()
    X_train_svd = svd.fit_transform(X_train_vector)

    model1 = Model_SVM()
    model1.fit(X_train_svd, y_train)

    #Test

    path_file_test = '../Dataset/Root/test_singlelabel.csv'
    df = pd.read_csv(path_file_test)
    X_test = df['Trích yếu']
    y_test = df['ID phòng xử lý']
    # Tiền xử lý
    vietnameseTextPreprocessor = VietnameseTextPreprocessor()
    X_test_preprocessing = X_test.apply(lambda x: vietnameseTextPreprocessor.process_text(x))

    #Test SVD
    X_test_vector_v1 = vectorization.transform(X_test_preprocessing)
    X_test_svd = svd.transform(X_test_vector_v1)

    y_pred_v1 = model1.predict(X_test_svd)

    model1.get_metrics(y_test, y_pred_v1)

    model1.get_confusion_matrix(y_test, y_pred_v1)

    #Test SVM
    vectorization_2 = Vectorization()
    vectorization_2.load_model('../Model/tfidf_v2.model')

    X_test_vector_v2 = vectorization_2.transform(X_test_preprocessing)

    model_svm_v2 = Model_SVM()
    model_svm_v2.load_model('../Model/svm_v2.model')

    y_pred_v2 = model_svm_v2.predict(X_test_vector_v2)

    model_svm_v2.get_metrics(y_test, y_pred_v2)

    model_svm_v2.get_confusion_matrix(y_test, y_pred_v2)

