@echo off
setlocal

REM Kiểm tra xem Python đã được cài đặt hay chưa
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo Python is already installed.
    goto check_pip
)

REM Nếu Python chưa được cài đặt, tải xuống và cài đặt
echo Python is not installed. Installing Python...

REM Tải xuống bộ cài đặt Python từ trang chính thức
set "python_installer_url=https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe"
set "python_installer=python_installer.exe"

echo Downloading Python installer...
powershell -Command "Invoke-WebRequest -Uri '%python_installer_url%' -OutFile '%python_installer%'"

REM Chạy bộ cài đặt Python
echo Installing Python...
start /wait %python_installer% /quiet InstallAllUsers=1 PrependPath=1

REM Xóa bộ cài đặt
del %python_installer%

REM Kiểm tra cài đặt Python lại
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python installation failed. Please install Python manually.
    exit /b 1
)

:check_pip
REM Kiểm tra xem pip đã được cài đặt chưa
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo Pip is not installed. Installing pip...

    REM Tải xuống và cài đặt pip
    set "get_pip_url=https://bootstrap.pypa.io/get-pip.py"
    set "get_pip_script=get-pip.py"

    echo Downloading get-pip.py...
    powershell -Command "Invoke-WebRequest -Uri '%get_pip_url%' -OutFile '%get_pip_script%'"

    echo Installing pip...
    python %get_pip_script%

    REM Xóa script cài đặt pip
    del %get_pip_script%
)

REM Cài đặt các thư viện cần thiết từ requirements.txt
echo Installing required packages...
pip install -r requirements.txt

REM Chạy ứng dụng FastAPI
echo Starting the FastAPI application...
python run_api.py

REM Pause để giữ cửa sổ CMD mở sau khi ứng dụng kết thúc
pause
endlocal