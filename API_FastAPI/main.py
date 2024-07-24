from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os

from Model_SVM import Model_SVM
from Vectorization import Vectorization
from VietnameseTextPreprocessor import VietnameseTextPreprocessor


# Kiểm tra và tải mô hình
def check_and_load_models():
    if not os.path.exists('Model/tfidf.model'):
        raise HTTPException(status_code=500, detail="TF-IDF model file not found.")

    if not os.path.exists('Model/svm.model'):
        raise HTTPException(status_code=500, detail="SVM model file not found.")

    vietnameseTextPreprocessor = VietnameseTextPreprocessor('Stopwords/stopwords_project.txt')
    vectorization = Vectorization()
    vectorization.load_model('Model/tfidf.model')
    svm_model = Model_SVM()
    svm_model.load_model('Model/svm.model')
    return vietnameseTextPreprocessor, vectorization, svm_model


vietnameseTextPreprocessor, vectorization, svm_model = check_and_load_models()

app = FastAPI()


class TextInput(BaseModel):
    text: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post('/predict/')
async def predict(request: TextInput):
    text = request.text
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    text_preprocessing = vietnameseTextPreprocessor.process_text(text)
    text_vector = vectorization.transform_text(text_preprocessing)
    prediction_proba = svm_model.predict_proba(text_vector)
    return {
        'text': text,
        'predict': prediction_proba
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)