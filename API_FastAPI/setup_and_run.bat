@echo off
setlocal

REM Kiểm tra xem pip đã được cài đặt chưa
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo Pip is not installed. Installing pip...

    REM Tải xuống và cài đặt pip
    set "get_pip_url=https://bootstrap.pypa.io/get-pip.py"
    set "get_pip_script=get-pip.py"

    echo Downloading get-pip.py...
    powershell -Command "Invoke-WebRequest -Uri %get_pip_url% -OutFile %get_pip_script%"

    echo Installing pip...
    python %get_pip_script%

    REM Xóa script cài đặt pip
    del %get_pip_script%
)

REM Cài đặt các thư viện cần thiết từ requirements.txt bằng pip của Python đã cài đặt
echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Chạy ứng dụng FastAPI
echo Starting the FastAPI application...
python main.py

REM Pause để giữ cửa sổ CMD mở sau khi ứng dụng kết thúc
pause
endlocal