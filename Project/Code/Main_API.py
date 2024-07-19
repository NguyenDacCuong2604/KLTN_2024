from fastapi import FastAPI
from pydantic import BaseModel

from Model_SVM import Model_SVM
from Vectorization import Vectorization
from VietnameseTextPreprocessor import VietnameseTextPreprocessor

vietnameseTextPreprocessor = VietnameseTextPreprocessor('../Dataset/Stopwords/stopwords_project_v2.txt')
vectorization = Vectorization()
vectorization.load_model('../Model/tfidf_v2.model')
svm_model = Model_SVM()
svm_model.load_model('../Model/svm_v2.model')

app = FastAPI()


class TextInput(BaseModel):
    text: str


@app.get('/')
async def root():
    return {'message': 'Hello World!!!'}


@app.post('/predict/')
async def predict(text_input : TextInput):
    text_preprocessing = vietnameseTextPreprocessor.process_text(text_input.text)
    text_vector = vectorization.transform_text(text_preprocessing)
    prediction_proba = svm_model.predict_proba(text_vector)

    return {
        'text': text_input.text,
        'predict': prediction_proba
    }