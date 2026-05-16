import streamlit as st
import random
import string
from pathlib import Path

# =========================
# 基础配置
# =========================

st.set_page_config(
    page_title="图书管理系统",
    page_icon="📚",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

BASE_DIR = Path(__file__).parent


# =========================
# 页面美化 CSS
# =========================

st.markdown(
    """
    <style>
    /* 隐藏右上角的菜单按钮（三个点） */
    .stApp header {
        display: none;
    }
    
    /* 隐藏顶部的 Streamlit 默认横幅 */
    .stAppDeployButton {
        display: none;
    }
    
    /* 隐藏 Footer（底部信息） */
    footer {
        display: none;
    }
    
    /* 隐藏 Fork 按钮所在区域 */
    .stApp > header {
        display: none;
    }
    
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }

    .sub-title {
        text-align: center;
        font-size: 16px;
        color: #7f8c8d;
        margin-bottom: 30px;
    }

    .captcha-box {
        background-color: #f1f5f9;
        border: 2px dashed #3b82f6;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        font-size: 26px;
        letter-spacing: 8px;
        font-weight: bold;
        color: #2563eb;
        margin-bottom: 10px;
    }

    .book-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 18px;
    }

    .book-title {
        font-size: 20px;
        font-weight: bold;
        color: #1f2937;
    }

    .book-info {
        color: #4b5563;
        line-height: 1.8;
    }
    </style>
    """,
    unsafe_allow_html=True
)
