"""
 Googleスプレッドシートからデータを取得してDataFrameに変換するモジュール
"""
import os
import pandas as pd
import urllib.request
from app.util import exit_error
from dotenv import find_dotenv, load_dotenv

def get_excel_path():
	load_dotenv()
	if find_dotenv() == "":
		exit_error("env file not found")

	XLSX_FILE_PATH = os.getenv("EXCEL_FILE_PATH")
	if XLSX_FILE_PATH == None:
		exit_error("fetch excel data failed")

	return XLSX_FILE_PATH

def fetch_data(sheet_url: str | None = None) -> pd.DataFrame:
	"""
	指定されたGoogleスプレッドシートのURLからExcelファイルをダウンロードし、DataFrameに変換して返す
	
	Parameters:
	-----------
	sheet_url : str | None
		GoogleスプレッドシートのエクスポートURL。
		省略時は環境変数 EXCEL_FILE_PATH から取得する。
	
	Returns:
	--------
	pd.DataFrame
		ダウンロードしたデータを含むDataFrame
	"""
	if sheet_url is None:
		sheet_url = get_excel_path()

	# 一時的にExcelファイルを保存するパス
	temp_excel_path = './list/name_tags.xlsx'
	
	# Excelファイルをダウンロード
	urllib.request.urlretrieve(sheet_url, temp_excel_path)
	
	# DataFrameに読み込み
	df = pd.read_excel(temp_excel_path)
	
	return df