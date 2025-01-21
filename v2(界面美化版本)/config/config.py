# config.py
import os
import sys

# 获取项目根目录 (向上一级获取实际的项目根目录)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 将项目根目录添加到 Python 路径
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)