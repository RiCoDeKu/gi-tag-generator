"""
ユーティリティ関数を提供するモジュール
"""
import os, sys
import pandas as pd
from typing import Literal

Color = Literal[
    "reset",
    "bold",
    "underline",
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
]

ANSI_CODES = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "underline": "\033[4m",
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}

def normalize_text(text):
    """テキストの正規化: NaNを空文字列に変換"""
    if pd.isna(text):
        return ""
    return str(text)

def get_color(color: Color) -> str:
    """ANSIエスケープシーケンスを返す。"""
    return ANSI_CODES[color]

def exit_error(msg: str) -> None:
	"""エラーメッセージを返し、強制終了する"""
	sys.stderr.write(f'[ERROR] {get_color("red")}{msg}{get_color("reset")}\n')
	sys.exit()