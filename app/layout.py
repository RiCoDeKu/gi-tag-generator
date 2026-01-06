"""
複数の名札を集約してA4シートに配置するモジュール
"""

# Install missing engine for pandas.read_excel
import os
import pandas as pd
from PIL import Image, ImageDraw
from app.generate import create_card
from app.util import normalize_text

def project_dataframe_extraction(df: pd.DataFrame, project_code: str):
    # project_codeに基づいてデータフレームを抽出する関数
    filtered = df[df["プロジェクトコード"].astype(str) == str(project_code)].copy()
    return filtered.reset_index(drop=True)

def create_business_card_sheets(project_code: str):
    # Excelファイルを読み込み
    df = pd.read_excel('./list/name_tags.xlsx')
    df = project_dataframe_extraction(df, project_code=project_code)
    # A4サイズ (210mm x 297mm) を300dpiで設定
    a4_width = int(210 * 300 / 25.4)  # 2480 px
    a4_height = int(297 * 300 / 25.4)  # 3508 px

    # 名刺サイズ
    card_width = 1075
    card_height = 650

    # A4に配置できる名刺の数 (横2枚、縦4枚 = 8枚/ページ)
    cards_per_row = 2
    cards_per_col = 4
    cards_per_page = cards_per_row * cards_per_col

    # 余白計算
    margin_x = (a4_width - cards_per_row * card_width) // (cards_per_row + 1)
    margin_y = (a4_height - cards_per_col * card_height) // (cards_per_col + 1)

    # ページ数を計算
    total_cards = len(df)
    total_pages = (total_cards + cards_per_page - 1) // cards_per_page

    print(f"[INFO] Total cards: [ {total_cards} ], Total pages: [ {total_pages} ]")

    # 点線を描画する関数
    def draw_dashed_line(draw, start, end, dash_length=20, gap_length=10, color=(150, 150, 150), width=2):
        x1, y1 = start
        x2, y2 = end
        
        # 線の長さと方向を計算
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2) ** 0.5
        
        if length == 0:
            return
        
        # 単位ベクトル
        ux = dx / length
        uy = dy / length
        
        # 点線を描画
        current_length = 0
        while current_length < length:
            # ダッシュの開始点
            start_x = x1 + ux * current_length
            start_y = y1 + uy * current_length
            
            # ダッシュの終了点
            end_length = min(current_length + dash_length, length)
            end_x = x1 + ux * end_length
            end_y = y1 + uy * end_length
            
            draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=width)
            
            current_length += dash_length + gap_length

    # 各ページを作成
    for page_num in range(total_pages):
        # A4キャンバス作成 (白背景)
        a4_canvas = Image.new('RGB', (a4_width, a4_height), (255, 255, 255))
        
        # このページに配置する名刺のインデックス範囲
        start_idx = page_num * cards_per_page
        end_idx = min(start_idx + cards_per_page, total_cards)
        
        # 名刺の配置位置を記録
        card_positions = []
        
        # 名刺を配置
        for i in range(start_idx, end_idx):
            row_data = df.iloc[i]
            
            # ロゴのPathをキャンパスに応じて選択
            campus = row_data['キャンパス']
            if '葛飾' in campus or 'Katsushika' in campus:
                logo_path = 'src/katsushika.png'
            elif '野田' in campus or 'Noda' in campus:
                logo_path = 'src/noda.png'
            elif '神楽坂' in campus or 'Kagurazaka' in campus:
                logo_path = 'src/kagurazaka.png'
            else:
                logo_path = 'src/other.png'  # デフォルト
            
            # 学年の変換
            if row_data['学年'] == 'B1':
                grade = '学部1年'
            elif row_data['学年'] == 'B2':
                grade = '学部2年'
            elif row_data['学年'] == 'B3':
                grade = '学部3年'
            elif row_data['学年'] == 'B4':
                grade = '学部4年'
            elif row_data['学年'] == 'M1':
                grade = '修士1年'
            elif row_data['学年'] == 'M2':
                grade = '修士2年'
            elif row_data['学年'] == 'D1':
                grade = '博士1年'
            elif row_data['学年'] == 'D2':
                grade = '博士2年'
            elif row_data['学年'] == 'D3':
                grade = '博士3年'
            else:
                grade = row_data['学年']

            # 氏名を変換
            name_jp = normalize_text(row_data['苗字']) + " " + normalize_text(row_data['名前'])
            
            # 氏名（英名）を変換
            # ミドルネームの有無を確認
            if (row_data['Middle Name'] is not None):
                name_en = normalize_text(row_data['Last Name']) + " " + normalize_text(row_data['Middle Name']) + " " + normalize_text(row_data['First Name'])
            else:
                name_en = normalize_text(row_data['Last Name']) + " " + normalize_text(row_data['First Name'])
            
            # 名刺を生成
            card = create_card(
                logo_path = logo_path,
                name_jp = name_jp,
                name_en = name_en,
                faculty = normalize_text(row_data['学部']),
                department = normalize_text(row_data['学科']),
                grade = str(grade),
                role = normalize_text(row_data['役割']),
                message = normalize_text(row_data['ひとことメッセージ']),
                message2 = normalize_text(row_data['ひとことメッセージ（2行目）']),
                campus = normalize_text(row_data['キャンパス']),
                url = normalize_text(row_data['URL']),
                caption = normalize_text(row_data['キャプション'])
            )
            
            # RGB変換
            card_rgb = card.convert('RGB')
            
            # ページ内での位置を計算 (Z字配置)
            card_index = i - start_idx
            row = card_index // cards_per_row
            col = card_index % cards_per_row
            
            # 配置位置計算
            x = margin_x + col * (card_width + margin_x)
            y = margin_y + row * (card_height + margin_y)
            
            # 名刺を貼り付け
            a4_canvas.paste(card_rgb, (x, y))
            
            # 位置を記録（切り取り線用）
            card_positions.append((x, y, x + card_width, y + card_height))
        
        # 切り取り線を描画
        draw = ImageDraw.Draw(a4_canvas)
        dash_color = (150, 150, 150)  # グレー
        
        # 各名刺の周りに切り取り線を描画
        for x1, y1, x2, y2 in card_positions:
            # 上辺
            draw_dashed_line(draw, (x1, y1), (x2, y1), color=dash_color, width=2)
            # 下辺
            draw_dashed_line(draw, (x1, y2), (x2, y2), color=dash_color, width=2)
            # 左辺
            draw_dashed_line(draw, (x1, y1), (x1, y2), color=dash_color, width=2)
            # 右辺
            draw_dashed_line(draw, (x2, y1), (x2, y2), color=dash_color, width=2)
        
        # ページを保存
        output_filename = f'./output/{project_code}/page{page_num + 1}.png'
        if not os.path.exists(f'./output/{project_code}/'):
            os.makedirs(f'./output/{project_code}/')
        a4_canvas.save(output_filename, format='PNG', dpi=(300, 300))