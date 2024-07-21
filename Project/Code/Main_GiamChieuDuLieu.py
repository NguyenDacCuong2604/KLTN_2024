from Code.Model_SVM import Model_SVM
import pandas as pd
from datetime import datetime

from Code.SVD import SVD
from Code.Vectorization import Vectorization

if __name__ == "__main__":
    # Giữ nguyên số chiều
    # print('Sử dụng stopwords project')
    # path_data_train_stopwords_project = '../Dataset/Root/data_preprocessing_stopwords_project.csv'
    # path_save_model_vector_stopwords_project = '../Model/tfidf_stopwords_project.model'
    # path_save_model_stopwords_project = '../Model/svm_stopwords_project.model'
    # df_stopwords_project = pd.read_csv(path_data_train_stopwords_project)
    #
    # X_train_stopwords_project = df_stopwords_project['input']
    # y_train_stopwords_project = df_stopwords_project['label']
    #
    # vectorization_stopwords_project = Vectorization()
    # current_time = datetime.now().timestamp()
    # X_train_vector_stopwords_project = vectorization_stopwords_project.fit_transform(X_train_stopwords_project)
    # print('Thời gian vector hóa')
    # print((datetime.now().timestamp() - current_time) * 1000)
    # print(vectorization_stopwords_project.get_vector_size())
    # vectorization_stopwords_project.save_model(path_save_model_vector_stopwords_project)
    #
    # model_stopwords_project = Model_SVM()
    # current_time = datetime.now().timestamp()
    # model_stopwords_project.fit(X_train_vector_stopwords_project, y_train_stopwords_project)
    # print('Thời gian train model')
    # print((datetime.now().timestamp() - current_time) * 1000)
    # model_stopwords_project.save_model(path_save_model_stopwords_project)

    # Loại bỏ bớt các term có tần suất xuất hiện từ 5 trở xuống
    print('Sử dụng stopwords project')
    path_data_train_stopwords_project = '../Dataset/Root/data_preprocessing_stopwords_project.csv'
    path_save_model_vector_stopwords_project = '../Model/tfidf_stopwords_project_min_df_6.model'
    path_save_model_stopwords_project = '../Model/svm_stopwords_project_min_df_6.model'
    df_stopwords_project = pd.read_csv(path_data_train_stopwords_project)

    X_train_stopwords_project = df_stopwords_project['input']
    y_train_stopwords_project = df_stopwords_project['label']

    vectorization_stopwords_project = Vectorization()
    current_time = datetime.now().timestamp()
    X_train_vector_stopwords_project = vectorization_stopwords_project.fit_transform(X_train_stopwords_project, min_df=6)
    print('Thời gian vector hóa')
    print((datetime.now().timestamp() - current_time) * 1000)
    print(vectorization_stopwords_project.get_vector_size())
    vectorization_stopwords_project.save_model(path_save_model_vector_stopwords_project)

    model_stopwords_project = Model_SVM()
    current_time = datetime.now().timestamp()
    model_stopwords_project.fit(X_train_vector_stopwords_project, y_train_stopwords_project)
    print('Thời gian train model')
    print((datetime.now().timestamp() - current_time) * 1000)
    model_stopwords_project.save_model(path_save_model_stopwords_project)

    # Dùng SVD với n = 1500
    print('Sử dụng stopwords project')
    path_data_train_stopwords_project = '../Dataset/Root/data_preprocessing_stopwords_project.csv'
    path_save_model_vector_stopwords_project = '../Model/tfidf_stopwords_project_svd.model'
    path_save_model_stopwords_project = '../Model/svm_stopwords_project_svd.model'
    df_stopwords_project = pd.read_csv(path_data_train_stopwords_project)

    X_train_stopwords_project = df_stopwords_project['input']
    y_train_stopwords_project = df_stopwords_project['label']

    vectorization_stopwords_project = Vectorization()
    current_time = datetime.now().timestamp()
    X_train_vector_stopwords_project = vectorization_stopwords_project.fit_transform(X_train_stopwords_project)
    print('Thời gian vector hóa')
    print((datetime.now().timestamp() - current_time) * 1000)
    print(vectorization_stopwords_project.get_vector_size())

    svd = SVD()
    current_time = datetime.now().timestamp()
    X_train_svd = svd.fit_transform(X_train_vector_stopwords_project)
    print('Thời gian SVD')
    print((datetime.now().timestamp() - current_time) * 1000)

    vectorization_stopwords_project.save_model(path_save_model_vector_stopwords_project)
    svd.save_model('../Model/svd.model')

    model_stopwords_project = Model_SVM()
    current_time = datetime.now().timestamp()
    model_stopwords_project.fit(X_train_svd, y_train_stopwords_project)
    print('Thời gian train model')
    print((datetime.now().timestamp() - current_time) * 1000)
    model_stopwords_project.save_model(path_save_model_stopwords_project)
