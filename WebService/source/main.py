from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
import sys

from SVM import SVM
from Vectorization import Vectorization
from VietnameseTextPreprocessor import VietnameseTextPreprocessor


# Cập nhật đường dẫn tương đối khi đóng gói ứng dụng
def get_asset_path(filename):
    if getattr(sys, 'frozen', False):
        # Nếu ứng dụng đang chạy trong chế độ đóng gói
        return os.path.join(sys._MEIPASS, 'assets', filename)
    else:
        # Nếu ứng dụng đang chạy trong môi trường phát triển
        return os.path.join('assets', filename)

# Kiểm tra và tải mô hình
def check_and_load_models():
    # Đường dẫn tới các file mô hình
    tfidf_model_path = get_asset_path('tfidf.model.txt')
    svm_model_path = get_asset_path('svm.model.txt')
    stopwords_path = get_asset_path('stopwords_project.txt')

    # Kiểm tra và tải mô hình TF-IDF
    if not os.path.exists(tfidf_model_path):
        print("Không tìm thấy file mô hình TF-IDF.")
        return None, None, None

    try:
        vectorization = Vectorization()
        vectorization.load_model(tfidf_model_path)
        print("Mô hình TF-IDF đã được tải thành công.")
    except EOFError:
        print("Lỗi EOF khi tải mô hình TF-IDF.")
        return None, None, None
    except Exception as e:
        print(f"Lỗi khi tải mô hình TF-IDF: {e}")
        return None, None, None

    # Kiểm tra và tải mô hình SVM
    if not os.path.exists(svm_model_path):
        print("Không tìm thấy file mô hình SVM.")
        return None, None, None

    try:
        svm_model = SVM()
        svm_model.load_model(svm_model_path)
        print("Mô hình SVM đã được tải thành công.")
    except EOFError:
        print("Lỗi EOF khi tải mô hình SVM.")
        return None, None, None
    except Exception as e:
        print(f"Lỗi khi tải mô hình SVM: {e}")
        return None, None, None
    try:
        vietnameseTextPreprocessor = VietnameseTextPreprocessor(stopwords_path)
        print("Preprocessor đã được tải thành công.")
    except Exception as e:
        print(f"Lỗi khi tải Preprocessor: {e}")
        return None, None, None
    return vietnameseTextPreprocessor, vectorization, svm_model

# Kiểm tra và tải các mô hình
vietnameseTextPreprocessor, vectorization, svm_model = check_and_load_models()

# Kiểm tra xem các mô hình đã được tải thành công chưa
if None in [vietnameseTextPreprocessor, vectorization, svm_model]:
    print("Failed to load models. Exiting...")
    sys.exit(1)  # Dừng chương trình nếu không tải được mô hình

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
    print("Starting FastAPI server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)