"""
キャッシュされた情報をクリアするためのモジュール
"""
import pandas as pd
import shutil
import os

def clear_cached_data():
	# QRコードのキャッシュを削除
	qr_path = "src/qr"
	if os.path.exists(qr_path):
		shutil.rmtree(qr_path)
		os.makedirs(qr_path)

	# 一時的なExcelファイルの中身データのみを削除し，空のExcelファイルを作成
	excel_path = './list/name_tags.xlsx'
	if os.path.exists(excel_path):
		os.remove(excel_path)
	pd.DataFrame().to_excel(excel_path, index=False)
	return