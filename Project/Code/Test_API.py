import pyvi
import os
import sklearn_crfsuite
import pycrfsuite
import tqdm

# Lấy đường dẫn đến thư mục cài đặt của thư viện pyvi
pyvi_path = os.path.dirname(pycrfsuite.__file__)
print(pyvi_path)