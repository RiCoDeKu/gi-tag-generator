"""
 Googleスプレッドシートからデータを取得してDataFrameに変換するモジュール
"""
import pandas as pd
import urllib.request

def fetch_data(sheet_url: str="https://docs.google.com/spreadsheets/d/1hdCBMAIsiq7Y8tMe-Q525zOmgNOU5ER4QImkaDgoDTc/export?format=xlsx") -> pd.DataFrame:
	"""
	指定されたGoogleスプレッドシートのURLからExcelファイルをダウンロードし、DataFrameに変換して返す
	
	Parameters:
	-----------
	sheet_url : str
		GoogleスプレッドシートのエクスポートURL
	
	Returns:
	--------
	pd.DataFrame
		ダウンロードしたデータを含むDataFrame
	"""
	# 一時的にExcelファイルを保存するパス
	temp_excel_path = './list/name_tags.xlsx'
	
	# Excelファイルをダウンロード
	urllib.request.urlretrieve(sheet_url, temp_excel_path)
	
	# DataFrameに読み込み
	df = pd.read_excel(temp_excel_path)
	
	return df