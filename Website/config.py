import os
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/thesis')
