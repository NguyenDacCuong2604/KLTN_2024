from Code.Model_SVM import Model_SVM
import pandas as pd

from Code.Vectorization import Vectorization

if __name__ == "__main__":
    #v1
    path_data_train1 = '../Dataset/Root/data_preprocessing_v1.csv'
    path_save_model_vector1 = '../Model/tfidf_v1.model'
    path_save_model1 = '../Model/svm_v1.model'
    df1 = pd.read_csv(path_data_train1)

    X_train1 = df1['input']
    y_train1 = df1['label']

    vectorization1 = Vectorization()
    X_train_vector1 = vectorization1.fit_transform(X_train1)
    vectorization1.save_model(path_save_model_vector1)

    model1 = Model_SVM()
    model1.fit(X_train_vector1, y_train1)

    model1.save_model(path_save_model1)

    #v2
    path_data_train2 = '../Dataset/Root/data_preprocessing_v2.csv'
    path_save_model_vector2 = '../Model/tfidf_v2.model'
    path_save_model2 = '../Model/svm_v2.model'
    df2 = pd.read_csv(path_data_train2)

    X_train2 = df2['input']
    y_train2 = df2['label']

    vectorization2 = Vectorization()
    X_train_vector2 = vectorization2.fit_transform(X_train2)
    vectorization2.save_model(path_save_model_vector2)

    model2 = Model_SVM()
    model2.fit(X_train_vector2, y_train2)

    model2.save_model(path_save_model2)
