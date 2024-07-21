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
    vietnameseTextPreprocessor = VietnameseTextPreprocessor(remove_np=False)
    X_test_preprocessing = X_test.apply(lambda x: vietnameseTextPreprocessor.process_text(x))

    #Test trường hợp không sử dụng stopwords
    vectorization_not_stopwords = Vectorization()
    vectorization_not_stopwords.load_model('../Model/tfidf_not_stopwords.model')

    X_test_vector_not_stopwords = vectorization_not_stopwords.transform(X_test_preprocessing)

    model_svm_not_stopwords = Model_SVM()
    model_svm_not_stopwords.load_model('../Model/svm_not_stopwords.model')

    y_pred_not_stopwords = model_svm_not_stopwords.predict(X_test_vector_not_stopwords)

    model_svm_not_stopwords.get_metrics(y_test, y_pred_not_stopwords)

    model_svm_not_stopwords.get_confusion_matrix(y_test, y_pred_not_stopwords)

    #Test trường hợp sử dụng stopwords vietnamese
    vectorization_stopwords_vietnamese = Vectorization()
    vectorization_stopwords_vietnamese.load_model('../Model/tfidf_stopwords_vietnamese.model')

    X_test_vector_stopwords_vietnamese = vectorization_stopwords_vietnamese.transform(X_test_preprocessing)

    model_svm_stopwords_vietnamese = Model_SVM()
    model_svm_stopwords_vietnamese.load_model('../Model/svm_stopwords_vietnamese.model')

    y_pred_stopwords_vietnamese = model_svm_stopwords_vietnamese.predict(X_test_vector_stopwords_vietnamese)

    model_svm_stopwords_vietnamese.get_metrics(y_test, y_pred_stopwords_vietnamese)

    model_svm_stopwords_vietnamese.get_confusion_matrix(y_test, y_pred_stopwords_vietnamese)

    #Test trường hợp sử dụng stopwords project
    vectorization_stopwords_project = Vectorization()
    vectorization_stopwords_project.load_model('../Model/tfidf_stopwords_project.model')

    X_test_vector_stopwords_project = vectorization_stopwords_project.transform(X_test_preprocessing)

    model_svm_stopwords_project = Model_SVM()
    model_svm_stopwords_project.load_model('../Model/svm_stopwords_project.model')

    y_pred_stopwords_project = model_svm_stopwords_project.predict(X_test_vector_stopwords_project)

    model_svm_stopwords_project.get_metrics(y_test, y_pred_stopwords_project)

    model_svm_stopwords_project.get_confusion_matrix(y_test, y_pred_stopwords_project)