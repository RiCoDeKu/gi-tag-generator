# GI 名札ジェネレーター

Google スプレッドシートから名札データを取得し、名刺画像を作成して A4 面付けを行います。
このリポジトリは `main.py` と `app/` 配下のモジュールを中心に構成されています。

## クイックスタート

```bash
pip install -r requirements.txt
python main.py
```

スクリプトはプロジェクトコードの入力を求め、シートをダウンロードして
`output/<project_code>/page<N>.png` に画像を書き出します。

## データフロー

- `app/fetch.py` が Google スプレッドシートを `list/name_tags.xlsx` にダウンロードします。
- `app/layout.py` が `list/name_tags.xlsx` を読み込み、プロジェクトコードで抽出し、
  名札を生成して A4 に面付けします。
- `app/generate.py` が名札 1 枚分の画像を描画します（QR がある場合は埋め込み）。
- `app/qr.py` が `src/qr/` に QR 画像を生成します。
- `app/cleaner.py` が `main.py` の最後で `src/qr/` を削除し、
  `list/name_tags.xlsx` を空のファイルに戻します。

## 必須列（列名は完全一致）

Excel の列名は下記の通りにしてください。コードから列名で参照しています。

```
プロジェクトコード
キャンパス
学年
苗字
名前
Middle Name
Last Name
First Name
学部
学科
役割
ひとことメッセージ
ひとことメッセージ（2行目）
URL
キャプション
```

補足:

- `URL` と `キャプション` は任意ですが、両方が揃っている場合のみ QR を描画します。
- `Middle Name` は空でも構いません。存在する場合のみ英名に含まれます。

## 出力

- A4 面付け画像: `output/<project_code>/page<N>.png`
- QR キャッシュ: `src/qr/*.png`

`main.py` は生成後に `clear_cached_data()` を呼び出し、`src/qr/` を削除し
`list/name_tags.xlsx` を空に戻します。データや QR を残したい場合は
`main.py` の該当行をコメントアウトしてください。

## ロゴとデザイン

- キャンパスごとのロゴ選択は `app/layout.py` で行っています。
  - `葛飾` または `Katsushika` -> `src/katsushika.png`
  - `野田` または `Noda` -> `src/noda.png`
  - `神楽坂` または `Kagurazaka` -> `src/kagurazaka.png`
  - それ以外 -> `src/other.png`
- フォントは macOS のヒラギノ角ゴ（`/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc`）
  を読み込みます。見つからない場合は Pillow のデフォルトフォントになります。
  他のフォントを使用したい場合はこの部分を変更してください．

## シート URL の変更

別の Google スプレッドシートを使う場合は `app/fetch.py` のデフォルト URL を変更します。

```python
fetch_data(sheet_url="...")
```

## モジュール一覧

- `main.py`: CLI エントリーポイント。プロジェクトコードの入力を受けて処理を実行します。
- `app/fetch.py`: Google シートを Excel としてダウンロードします。
- `app/layout.py`: プロジェクト抽出と A4 面付けを担当します。
- `app/generate.py`: 名札 1 枚の描画を行います。
- `app/qr.py`: QR 画像を生成します。
- `app/util.py`: 文字列の正規化ユーティリティ。
- `app/cleaner.py`: QR キャッシュ削除と Excel の初期化を行います。
