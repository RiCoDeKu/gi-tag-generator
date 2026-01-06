"""
名札作成メインスクリプト
How to use:
1. 必要なライブラリをインストールします。
   pip install -r requirements.txt
2. スクリプトを実行します。
   python main.py
"""
from app.fetch import *
from app.generate import *
from app.layout import *
from app.qr import *
from app.util import *
from app.cleaner import *

def pbar_update(pbar, step_description):
	pbar.set_description(step_description)
	pbar.update(1)
def main():
	project_code = input("Enter the project code: ").strip()
	print(f"[INFO]Project Code: {project_code}")

	# Googleスプレッドシートからデータを取得
	df = fetch_data()

	# プロジェクトコードに基づいてデータを抽出
	p = project_dataframe_extraction(df, project_code=project_code)

	if len(p) == 0:
		print(f"[ERROR] No records found for project code: {project_code}")
		exit(1)

	# 名刺シートを作成
	create_business_card_sheets(project_code=project_code)
	clear_cached_data()
	print(f"[SUCCESS] Business cards generated successfully.")

if __name__ == "__main__":
	main()