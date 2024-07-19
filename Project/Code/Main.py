import os

from Code.PreProcessing import VietnameseTextPreprocessor

if __name__ == "__main__":
    path_stopwords = '../Dataset/Stopwords/stopwords_project_v2.txt'
    input_path = '../Dataset/Root/data.csv'
    output_path = '../Dataset/Root/data_preprocessing_v2.csv'

    vietnameseTextPreprocessor = VietnameseTextPreprocessor(path_stopwords)
    vietnameseTextPreprocessor.process_file(input_path, output_path)


