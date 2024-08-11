from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
import sys
import configparser

from starlette.middleware.cors import CORSMiddleware

from SVM import SVM
from Vectorization import Vectorization
from VietnameseTextPreprocessor import VietnameseTextPreprocessor


def read_config_file():
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    config_file_path = os.path.join(base_path, 'config.ini')
    # Read the configuration file
    config.read(config_file_path, encoding='utf-8')
    stopwords_project_path = config.get('General', 'stopwords_project_path')
    svm_model_path = config.get('General', 'svm_model_path')
    tf_idf_model_path = config.get('General', 'tf_idf_model_path')
    return stopwords_project_path, svm_model_path, tf_idf_model_path

def read_config_CORS():
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    config_file_path = os.path.join(base_path, 'config.ini')
    # Read the configuration file
    config.read(config_file_path, encoding='utf-8')
    allow_origins_str = config.get('CORS', 'allow_origins')
    allow_origins = [column.strip() for column in allow_origins_str.split(';')]
    host_api = config.get('CORS', 'host_api')
    port_api = config.getint('CORS', 'port_api')
    return allow_origins, host_api, port_api


# Kiểm tra và tải mô hình
def check_and_load_models():
    stopwords_project_path, svm_model_path, tfidf_model_path = read_config_file()

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
        vietnameseTextPreprocessor = VietnameseTextPreprocessor(stopwords_project_path)
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
    input("Press Enter to exit...")
    sys.exit(1)  # Dừng chương trình nếu không tải được mô hình


class TextInput(BaseModel):
    text: str


origins, host_api, port_api = read_config_CORS()

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
    uvicorn.run(app, host=host_api, port=port_api)
