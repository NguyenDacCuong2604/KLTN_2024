from Code.Model_SVM import Model_SVM
from Code.Vectorization import Vectorization
from Code.VietnameseTextPreprocessor import VietnameseTextPreprocessor

if __name__ == "__main__":
    vietnameseTextPreprocessor = VietnameseTextPreprocessor()

    vectorization = Vectorization()
    vectorization.load_model('../Model/tfidf_v1.model')

    model_svm = Model_SVM()
    model_svm.load_model('../Model/svm_v1.model')

    text_example = 'Kết quả thực hiện công tác cải cách hành chính Quý I năm 2023'

    print(model_svm.predict_proba(vectorization.transform_text(vietnameseTextPreprocessor.process_text(text_example))))
