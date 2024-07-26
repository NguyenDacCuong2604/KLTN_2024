from Code.VietnameseTextPreprocessor import VietnameseTextPreprocessor

if __name__ == "__main__":
    input_path = '../Dataset/Root/data.csv'
    #Không sử dụng stopwords
    output_path_not_stopwords = '../Dataset/Root/data_preprocessing_not_stopwords.csv'
    vietnameseTextPreprocessorNotStopwords = VietnameseTextPreprocessor(remove_np=False, multi_label=False)
    vietnameseTextPreprocessorNotStopwords.process_file(input_path, output_path_not_stopwords)
    #Sử dụng stopwords của vietnamese-stopwords-dash
    path_stopwords_vietnamese = '../Dataset/Stopwords/vietnamese-stopwords-dash.txt'
    output_path_stopwords_vietnamese = '../Dataset/Root/data_preprocessing_stopwords_vietnamese.csv'
    vietnameseTextPreprocessorStopwordsVietnamese = VietnameseTextPreprocessor(path_stopwords=path_stopwords_vietnamese, remove_np=False, multi_label=False)
    vietnameseTextPreprocessorStopwordsVietnamese.process_file(input_path, output_path_stopwords_vietnamese)
    #Sử dụng stopwords của project
    path_stopwords_project = '../Dataset/Stopwords/stopwords_project.txt'
    output_path_stopwords_project = '../Dataset/Root/data_preprocessing_stopwords_project.csv'
    vietnameseTextPreprocessorStopwordsProject = VietnameseTextPreprocessor(path_stopwords=path_stopwords_project, multi_label=False)
    vietnameseTextPreprocessorStopwordsProject.process_file(input_path, output_path_stopwords_project)


