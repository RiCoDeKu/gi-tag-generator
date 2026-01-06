"""
1枚あたりの名札を生成するモジュール
"""
import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from app.qr import create_qr_codes_from_excel # QRコード生成関数

def create_card(logo_path, name_jp, name_en, faculty, department, grade, role, message, message2, campus, url, caption):
    # 名刺サイズ (91mm x 55mm) を高解像度で作成 (300dpi想定: 1075x650 px)
    width, height = 1075, 650

    # カラー定義
    # 各キャンパスのロゴから抽出した色
    tus_katsushika 	= (46,  167, 68)      	# 葛飾キャンパス: グリーン
    tus_noda		= (243, 152, 0)          # 野田キャンパス: オレンジ
    tus_kagurazaka 	= (0,   160, 193)      	# 神楽坂キャンパス: シアン
    tus_freshman 	= (101, 5,   42)         # 新入生: えんじ色
    
    # campusに合わせてtus_colorを選択
    if "葛飾" in campus or "Katsushika" in campus:
        tus_color = tus_katsushika
    elif "野田" in campus or "Noda" in campus:
        tus_color = tus_noda
    elif "神楽坂" in campus or "Kagurazaka" in campus:
        tus_color = tus_kagurazaka
    else:
        tus_color = tus_freshman  # デフォルト
    
    dark_gray = (64, 64, 64)
    white = (255, 255, 255)

    # キャンバス作成 (白背景)
    canvas = Image.new('RGBA', (width, height), white)
    draw = ImageDraw.Draw(canvas)

    # --- フォント設定 ---
    try:
        # macOSの日本語フォントを使用 (ヒラギノ角ゴシック W6 = 太字)
        font_large = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 60)  # 氏名用
        font_medium = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 32)  # 学部・学科用
        font_small = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 24)  # 役職・メッセージ用
        font_tag = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 28)  # キャンパスタグ用
        font_english_name = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 38)  # 英名用
    except:
        # フォントが見つからない場合はデフォルト
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_english_name = ImageFont.load_default()

    # NaN値を空文字列に変換
    if pd.isna(role):
        role = ""
    if pd.isna(message):
        message = ""
    if pd.isna(message2):
        message2 = ""

    # --- 1. ロゴの透かし配置 (Watermark) ---
    try:
        logo = Image.open(logo_path).convert("RGBA")

        # ロゴをキャンバスの高さに合わせてリサイズ (余白を考慮して90%程度)
        # 高品質なリサイズのためにLANCZOSを使用
        logo_h = int(height * 0.85)
        logo_ratio = logo_h / logo.height
        logo_w = int(logo.width * logo_ratio)
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

        # 透明度調整 (Alpha値を変更)
        # 完全に透明=0, 不透明=255。ここでは 45 に設定
        logo_data = logo.getdata()
        new_data = []
        for item in logo_data:
            # 色情報はそのまま、アルファ値だけ変更
            if item[3] > 0: # もともと透明でない部分のみ
                new_data.append((item[0], item[1], item[2], 45))
            else:
                new_data.append(item)
        logo.putdata(new_data)

        # 中央に配置
        bg_x = (width - logo_w) // 2
        bg_y = (height - logo_h) // 2

        # アルファ合成のために貼り付け
        canvas.alpha_composite(logo, (bg_x, bg_y))

    except Exception as e:
        print(f"Logo load error: {e}")
        # ロゴがない場合のプレビュー用円形
        draw.ellipse((width//2 - 200, height//2 - 200, width//2 + 200, height//2 + 200), fill=(200, 200, 200, 50))

    # --- 2. テキスト配置 ---
    # レイアウト座標 (px単位)
    margin_x = 80

    # 役職 (Committee Role) - 空でない場合のみ表示
    if role:
        role_text = str(role)
        role_box_x1 = margin_x
        role_box_y1 = 160
        role_box_x2 = margin_x + 300
        role_box_y2 = 200
        draw.rectangle([role_box_x1, role_box_y1, role_box_x2, role_box_y2], fill=tus_color)
        
        # テキストの幅を取得して中央揃え
        role_bbox = draw.textbbox((0, 0), role_text, font=font_small)
        role_text_width = role_bbox[2] - role_bbox[0]
        role_text_height = role_bbox[3] - role_bbox[1]
        role_box_width = role_box_x2 - role_box_x1
        role_box_height = role_box_y2 - role_box_y1
        role_text_x = role_box_x1 + (role_box_width - role_text_width) // 2
        role_text_y = role_box_y1 + (role_box_height - role_text_height) // 2
        draw.text((role_text_x, role_text_y), role_text, fill=white, font=font_small)

    # 氏名 (Name) - Big & Bold
    draw.text((margin_x, 220), name_jp, fill=dark_gray, font=font_large)
    
    # 英名 (English Name)
    draw.text((margin_x, 290), name_en, fill=dark_gray, font=font_english_name)

    # 学部・学科 (Dept)
    draw.text((margin_x, 370), faculty, fill=dark_gray, font=font_medium)
    draw.text((margin_x, 420), f"{department} / {grade}", fill=dark_gray, font=font_medium)

    # 一言メッセージ (Message) - Bottom Left - 空でない場合のみ表示
    if message or message2:
        draw.line((margin_x, 520, margin_x + 600, 520), fill=(200,200,200), width=2)
    if message:
        draw.text((margin_x, 530), str(message), fill=dark_gray, font=font_small)
    if message2:
        if message:
            draw.text((margin_x, 565), str(message2), fill=dark_gray, font=font_small)
        else:
            draw.text((margin_x, 530), str(message2), fill=dark_gray, font=font_small)

    # キャンパス (Campus Tag) - Top Right
    if campus in ["葛飾", "野田", "神楽坂"]:
        campus_text = campus+"キャンパス"
    else:
        campus_text = campus
    tag_w, tag_h = 250, 60
    tag_x = width - tag_w - 50
    tag_y = 50

    # 枠線のみのタグデザイン
    draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=30, outline=tus_color, width=3)
    
    # テキストの幅を取得して中央揃え
    campus_bbox = draw.textbbox((0, 0), campus_text, font=font_tag)
    campus_text_width = campus_bbox[2] - campus_bbox[0]
    campus_text_height = campus_bbox[3] - campus_bbox[1]
    campus_text_x = tag_x + (tag_w - campus_text_width) // 2
    campus_text_y = tag_y + (tag_h - campus_text_height) // 2
    draw.text((campus_text_x, campus_text_y), campus_text, fill=tus_color, font=font_tag)

    # QRコード - Bottom Right
    if url and caption and not pd.isna(caption):
        create_qr_codes_from_excel()
        if not os.path.exists(f'src/qr/{caption}.png'):
            raise FileNotFoundError(f"QR code for caption '{caption}' was not generated.")
        qr_size = 130
        qr_x = width - qr_size - 50
        qr_y = height - qr_size - 50

        try:
            qr_image = Image.open(f'src/qr/{caption}.png').convert("RGBA")
            # QRコードをエリアに合わせてリサイズ
            qr_image = qr_image.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
            # QRコードを貼り付け
            canvas.alpha_composite(qr_image, (qr_x, qr_y))
            # キャプションをQRコードの上に描画
            caption_text = str(caption)
            caption_bbox = draw.textbbox((0, 0), caption_text, font=font_small)
            caption_text_width = caption_bbox[2] - caption_bbox[0]
            caption_text_height = caption_bbox[3] - caption_bbox[1]
            caption_x = qr_x + (qr_size - caption_text_width) // 2
            caption_y = qr_y - caption_text_height - 8  # QRコードの上に少し余白を持たせて配置
            draw.text((caption_x, caption_y), caption_text, fill=dark_gray, font=font_small)
        except Exception as e:
            print(f"QR code load error: {e}")

        return canvas

    return canvas
