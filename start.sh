#!/bin/bash

echo "=========================================="
echo "  Employee Handbook Q&A System"
echo "=========================================="
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    echo ""
    echo "注意: 如果遇到错误，请先运行:"
    echo "  sudo apt install python3.12-venv"
    echo ""
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ 虚拟环境创建失败"
        echo ""
        echo "解决方案 1: 安装 python3-venv"
        echo "  sudo apt install python3.12-venv"
        echo "  然后重新运行此脚本"
        echo ""
        echo "解决方案 2: 使用系统 Python（不推荐）"
        echo "  pip install -r requirements.txt --break-system-packages"
        echo "  streamlit run app.py"
        exit 1
    fi
    echo "✅ 虚拟环境创建成功"
    echo ""
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装/更新依赖
echo "📥 安装/更新依赖包..."
echo ""
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 依赖安装失败"
    exit 1
fi

echo ""
echo "✅ 依赖安装完成"
echo ""
echo "=========================================="
echo "  启动应用..."
echo "=========================================="
echo ""
echo "应用将在浏览器中自动打开"
echo "按 Ctrl+C 停止应用"
echo ""

# 启动应用
streamlit run app.py
