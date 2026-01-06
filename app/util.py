"""
ユーティリティ関数を提供するモジュール
"""
import pandas as pd

def normalize_text(text):
    """テキストの正規化: NaNを空文字列に変換"""
    if pd.isna(text):
        return ""
    return str(text)
