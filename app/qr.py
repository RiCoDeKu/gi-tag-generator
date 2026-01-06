"""
QRコードの生成と保存を行うモジュール
"""
import qrcode
import pandas as pd
import os

def create_qr_codes_from_excel(excel_path='./list/name_tags.xlsx', output_dir='src/qr', qr_path=None, caption=None):
    """
    ExcelファイルからURLを読み込み、各URLに対してQRコードを生成して保存する
    
    Parameters:
    -----------
    excel_path : str
        Excelファイルのパス
    output_dir : str
        QRコードを保存するディレクトリ
    """
    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)
    
    if qr_path and caption:
        # QRコードを生成
        qr = qrcode.QRCode(
            version=1,  # QRコードのサイズ (1-40)
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高い誤り訂正
            box_size=10,  # 各ボックスのピクセル数
            border=4,  # 境界の幅
        )
        
        qr.add_data(qr_path)
        qr.make(fit=True)
        
        # QRコード画像を作成
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # ファイル名を生成（キャプションを使用）
        safe_name = str(caption).replace(' ', '_').replace('/', '_').replace('\\', '_')
        filename = f"{safe_name}.png"
        
        # 保存
        output_path = os.path.join(output_dir, filename)
        qr_image.save(output_path)
        return
    else:
        # Excelファイルを読み込み
        df = pd.read_excel(excel_path)
        
        # URLカラムが存在するか確認
        if 'URL' not in df.columns:
            print("[ERROR]'URL'カラムが見つかりません")
            return
        
        # 各行に対してQRコードを生成
        for index, row in df.iterrows():
            url = row['URL']
            if pd.notna(url):
                # QRコードを生成
                qr = qrcode.QRCode(
                    version=1,  # QRコードのサイズ (1-40)
                    error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高い誤り訂正
                    box_size=10,  # 各ボックスのピクセル数
                    border=4,  # 境界の幅
                )
                
                qr.add_data(url)
                qr.make(fit=True)
                
                # QRコード画像を作成
                qr_image = qr.make_image(fill_color="black", back_color="white")
                
                # ファイル名を生成（キャプションを使用）
                if 'キャプション' in df.columns and not pd.isna(row['キャプション']):
                    # ファイル名に使えない文字を置換
                    safe_name = str(row['キャプション']).replace(' ', '_').replace('/', '_').replace('\\', '_')
                    filename = f"{safe_name}.png"
                else:
                    filename = f"qr_{index + 1}.png"
                
                # 保存
                output_path = os.path.join(output_dir, filename)
                qr_image.save(output_path)
        return