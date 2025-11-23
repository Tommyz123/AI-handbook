#!/usr/bin/env python3
"""
一键安装和启动脚本
自动安装依赖并启动应用
"""
import subprocess
import sys
import os

def install_dependencies():
    """安装依赖包"""
    print("📦 正在安装依赖包...")
    print("=" * 60)
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("\n✅ 依赖安装完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 依赖安装失败: {e}")
        return False

def create_env_file():
    """创建 .env 文件"""
    if not os.path.exists(".env"):
        print("\n📝 创建配置文件...")
        try:
            with open(".env", "w") as f:
                f.write("MODE=free\n")
                f.write("OPENAI_API_KEY=\n")
            print("✅ 配置文件创建完成！")
        except Exception as e:
            print(f"❌ 配置文件创建失败: {e}")
    else:
        print("\n✅ 配置文件已存在")

def create_directories():
    """创建必要的目录"""
    print("\n📁 创建必要的目录...")
    directories = ["cache", "cache/vector_store", "logs"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ 目录创建完成！")

def start_app():
    """启动应用"""
    print("\n🚀 启动应用...")
    print("=" * 60)
    print("应用将在浏览器中打开")
    print("按 Ctrl+C 停止应用")
    print("=" * 60 + "\n")
    
    try:
        subprocess.call([
            sys.executable, "-m", "streamlit", "run", "app.py"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 应用已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("  员工手册智能问答系统 - 安装向导")
    print("=" * 60)
    
    try:
        # 1. 安装依赖
        if not install_dependencies():
            print("\n请手动安装依赖: pip install -r requirements.txt")
            sys.exit(1)
        
        # 2. 创建配置文件
        create_env_file()
        
        # 3. 创建目录
        create_directories()
        
        # 4. 启动应用
        print("\n" + "=" * 60)
        print("  安装完成！正在启动应用...")
        print("=" * 60)
        start_app()
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
