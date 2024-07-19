from Code.VietnameseTextPreprocessor import VietnameseTextPreprocessor

if __name__ == "__main__":
    input_path = '../Dataset/Root/data.csv'
    #V1
    path_stopwords1 = '../Dataset/Stopwords/stopwords_project_v1.txt'
    output_path1 = '../Dataset/Root/data_preprocessing_v1.csv'
    vietnameseTextPreprocessor1 = VietnameseTextPreprocessor(path_stopwords1)
    vietnameseTextPreprocessor1.process_file(input_path, output_path1)
    #V2
    path_stopwords2 = '../Dataset/Stopwords/stopwords_project_v2.txt'
    output_path2 = '../Dataset/Root/data_preprocessing_v2.csv'
    vietnameseTextPreprocessor2 = VietnameseTextPreprocessor(path_stopwords2)
    vietnameseTextPreprocessor2.process_file(input_path, output_path2)


