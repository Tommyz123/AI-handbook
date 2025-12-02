@echo off
chcp 65001 > nul
echo ==========================================
echo   Employee Handbook Q&A System
echo ==========================================
echo.

REM 检查虚拟环境
if not exist "venv" (
    echo 📦 创建虚拟环境...
    echo.
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ❌ 虚拟环境创建失败
        echo.
        echo 解决方案: 请确保已安装 Python 3.8+
        echo   1. 下载并安装 Python: https://www.python.org/downloads/
        echo   2. 安装时勾选 "Add Python to PATH"
        echo   3. 重新运行此脚本
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
    echo.
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装/更新依赖
echo 📥 安装/更新依赖包...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo.
echo ✅ 依赖安装完成
echo.
echo ==========================================
echo   启动应用...
echo ==========================================
echo.
echo 应用将在浏览器中自动打开
echo 按 Ctrl+C 停止应用
echo.

REM 启动应用
streamlit run app.py

pause
