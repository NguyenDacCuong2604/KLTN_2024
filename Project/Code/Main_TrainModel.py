from Code.Model_SVM import Model_SVM
import pandas as pd
from datetime import datetime
from Code.Vectorization import Vectorization

if __name__ == "__main__":
    #Không sử dụng stopwords
    print('Không sử dụng stopwords')
    path_data_train_not_stopwords = '../Dataset/Root/data_preprocessing_not_stopwords.csv'
    path_save_model_vector_not_stopwords = '../Model/tfidf_not_stopwords.model'
    path_save_model_not_stopwords = '../Model/svm_not_stopwords.model'
    df_not_stopwords = pd.read_csv(path_data_train_not_stopwords)

    X_train_not_stopwords = df_not_stopwords['input']
    y_train_not_stopwords = df_not_stopwords['label']

    vectorization_not_stopwords = Vectorization()
    current_time = datetime.now().timestamp()
    X_train_vector_not_stopwords = vectorization_not_stopwords.fit_transform(X_train_not_stopwords)
    print('Thời gian vector hóa')
    print((datetime.now().timestamp() - current_time) * 1000)
    print(vectorization_not_stopwords.get_vector_size())
    vectorization_not_stopwords.save_model(path_save_model_vector_not_stopwords)

    model_not_stopwords = Model_SVM()
    current_time = datetime.now().timestamp()
    model_not_stopwords.fit(X_train_vector_not_stopwords, y_train_not_stopwords)
    print('Thời gian train model')
    print((datetime.now().timestamp() - current_time) * 1000)
    model_not_stopwords.save_model(path_save_model_not_stopwords)

    # Sử dụng stopwords vietnamese
    print('Sử dụng stopwords vietnamese')
    path_data_train_stopwords_vietnamese = '../Dataset/Root/data_preprocessing_stopwords_vietnamese.csv'
    path_save_model_vector_stopwords_vietnamese = '../Model/tfidf_stopwords_vietnamese.model'
    path_save_model_stopwords_vietnamese = '../Model/svm_stopwords_vietnamese.model'
    df_stopwords_vietnamese = pd.read_csv(path_data_train_stopwords_vietnamese)

    X_train_stopwords_vietnamese = df_stopwords_vietnamese['input']
    y_train_stopwords_vietnamese = df_stopwords_vietnamese['label']

    vectorization_stopwords_vietnamese = Vectorization()
    current_time = datetime.now().timestamp()
    X_train_vector_stopwords_vietnamese = vectorization_stopwords_vietnamese.fit_transform(X_train_stopwords_vietnamese)
    print('Thời gian vector hóa')
    print((datetime.now().timestamp() - current_time) * 1000)
    print(vectorization_stopwords_vietnamese.get_vector_size())
    vectorization_stopwords_vietnamese.save_model(path_save_model_vector_stopwords_vietnamese)

    model_stopwords_vietnamese = Model_SVM()
    current_time = datetime.now().timestamp()
    model_stopwords_vietnamese.fit(X_train_vector_stopwords_vietnamese, y_train_stopwords_vietnamese)
    print('Thời gian train model')
    print((datetime.now().timestamp() - current_time) * 1000)
    model_stopwords_vietnamese.save_model(path_save_model_stopwords_vietnamese)

    # Sử dụng stopwords project
    print('Sử dụng stopwords project')
    path_data_train_stopwords_project = '../Dataset/Root/data_preprocessing_stopwords_project.csv'
    path_save_model_vector_stopwords_project = '../Model/tfidf_stopwords_project.model'
    path_save_model_stopwords_project = '../Model/svm_stopwords_project.model'
    df_stopwords_project = pd.read_csv(path_data_train_stopwords_project)

    X_train_stopwords_project = df_stopwords_project['input']
    y_train_stopwords_project = df_stopwords_project['label']

    vectorization_stopwords_project = Vectorization()
    current_time = datetime.now().timestamp()
    X_train_vector_stopwords_project = vectorization_stopwords_project.fit_transform(X_train_stopwords_project)
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
