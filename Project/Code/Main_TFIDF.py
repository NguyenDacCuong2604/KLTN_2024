from Code.Model_SVM import Model_SVM
from Code.SVD import SVD
from Code.Vectorization import Vectorization
import pandas as pd

from Code.VietnameseTextPreprocessor import VietnameseTextPreprocessor

if __name__ == "__main__":
    path_data_train = '../Dataset/Root/data_preprocessing_v2.csv'
    path_save_model_vector = '../Model/tfidf_v2.model'
    df = pd.read_csv(path_data_train)

    X_train = df['input']
    y_train = df['label']

    vectorization = Vectorization(use_idf=False)
    X_train_vector = vectorization.fit_transform(X_train)

    vectorization.save_model('../Model/tfidf_not_useidf.model')

    model1 = Model_SVM()
    model1.fit(X_train_vector, y_train)

    model1.save_model('../Model/svm_not_useidf.model')

    #Test
    path_file_test = '../Dataset/Root/test_singlelabel.csv'
    df = pd.read_csv(path_file_test)
    X_test = df['Trích yếu']
    y_test = df['ID phòng xử lý']
    # Tiền xử lý
    vietnameseTextPreprocessor = VietnameseTextPreprocessor()
    X_test_preprocessing = X_test.apply(lambda x: vietnameseTextPreprocessor.process_text(x))

    X_test_vector_v1 = vectorization.transform(X_test_preprocessing)

    y_pred_v1 = model1.predict(X_test_vector_v1)

    model1.get_metrics(y_test, y_pred_v1)

    model1.get_confusion_matrix(y_test, y_pred_v1)


