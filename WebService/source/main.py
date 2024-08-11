from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
import sys

from starlette.middleware.cors import CORSMiddleware

from SVM import SVM
from Vectorization import Vectorization
from VietnameseTextPreprocessor import VietnameseTextPreprocessor


# Cập nhật đường dẫn tương đ[ối khi đóng gói ứng dụng
def get_asset_path(filename):
    return os.path.join('../assets', filename)

# Kiểm tra và tải mô hình
def check_and_load_models():
    # Đường dẫn tới các file mô hình
    tfidf_model_path = get_asset_path('tfidf.model')
    svm_model_path = get_asset_path('svm.model')
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

class TextInput(BaseModel):
    text: str

origins = [
    "http://localhost:8080",
    # Bạn có thể thêm các nguồn gốc khác vào đây nếu cần
]

app = FastAPI()

# Thêm CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, PUT, DELETE, v.v.)
    allow_headers=["*"],  # Cho phép tất cả các header
)

# Các route và logic còn lại của bạn
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
