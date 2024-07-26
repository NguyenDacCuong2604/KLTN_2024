from Code.Model_SVM import Model_SVM
from Code.SVD import SVD
from Code.Vectorization import Vectorization
import pandas as pd

from Code.VietnameseTextPreprocessor import VietnameseTextPreprocessor

if __name__ == "__main__":

    path_file_test = '../Dataset/Root/test_singlelabel.csv'
    df = pd.read_csv(path_file_test)
    X_test = df['Trích yếu']
    y_test = df['ID phòng xử lý']
    #Tiền xử lý
    vietnameseTextPreprocessor = VietnameseTextPreprocessor(remove_np=False)
    X_test_preprocessing = X_test.apply(lambda x: vietnameseTextPreprocessor.process_text(x))

    #Test trường hợp sử dụng stopwords project với min df = 6
    vectorization_stopwords_project = Vectorization()
    vectorization_stopwords_project.load_model('../Model/tfidf_stopwords_project_min_df_6.model')

    X_test_vector_stopwords_project = vectorization_stopwords_project.transform(X_test_preprocessing)

    model_svm_stopwords_project = Model_SVM()
    model_svm_stopwords_project.load_model('../Model/svm_stopwords_project_min_df_6.model')

    y_pred_stopwords_project = model_svm_stopwords_project.predict(X_test_vector_stopwords_project)

    model_svm_stopwords_project.get_metrics(y_test, y_pred_stopwords_project)

    model_svm_stopwords_project.get_confusion_matrix(y_test, y_pred_stopwords_project)

    # #Test trường hợp sử dụng SVD
    # vectorization_stopwords_project = Vectorization()
    # vectorization_stopwords_project.load_model('../Model/tfidf_stopwords_project_svd.model')
    #
    # X_test_vector_stopwords_project = vectorization_stopwords_project.transform(X_test_preprocessing)
    #
    # svd = SVD()
    # svd.load_model('../Model/svd.model')
    #
    # X_test_vector_svd = svd.transform(X_test_vector_stopwords_project)
    #
    # model_svm_stopwords_project = Model_SVM()
    # model_svm_stopwords_project.load_model('../Model/svm_stopwords_project_svd.model')
    #
    # y_pred_stopwords_project = model_svm_stopwords_project.predict(X_test_vector_svd)
    #
    # model_svm_stopwords_project.get_metrics(y_test, y_pred_stopwords_project)
    #
    # model_svm_stopwords_project.get_confusion_matrix(y_test, y_pred_stopwords_project)