import discord
from discord import app_commands
from discord.ui import Modal, TextInput
import gspread
import os
import json
from google.oauth2.service_account import Credentials
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)

# --- 設定項目 ---
# Secretから情報を読み込む
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
SPREADSHEET_NAME = os.environ.get('SPREADSHEET_NAME', '日報') # 環境変数がなければ'日報'を使う

# --- Google認証情報の読み込み（修正箇所） ---
try:
    # 環境変数からJSON文字列を読み込む
    gcp_sa_key_str = os.environ.get('GCP_SA_KEY')
    if not gcp_sa_key_str:
        raise ValueError("環境変数 'GCP_SA_KEY' が設定されていません。")
    
    # JSON文字列を辞書オブジェクトに変換
    gcp_json_credentials_dict = json.loads(gcp_sa_key_str)

    # 認証情報の設定
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_info(gcp_json_credentials_dict, scopes=SCOPES)
    gc = gspread.authorize(creds)
    spreadsheet = gc.open(SPREADSHEET_NAME)
    worksheet = spreadsheet.sheet1
    logging.info("Googleスプレッドシートへの接続に成功しました。")

except Exception as e:
    logging.error(f"Googleスプレッドシートへの接続に失敗しました: {e}")
    # 接続に失敗したらBotを起動しない
    exit()
# --- ここまで ---

# Discord BotのIntents設定
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# （中略：モーダルやコマンドの定義は変更なし）
# ... あなたのReportModalやDailyReportModal、各コマンドのコードをここに ...
# ... 省略せずに、以前のコードをそのままここに配置してください ...

# Webサーバー部分
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Botが起動したときの処理
@client.event
async def on_ready():
    logging.info(f'{client.user} としてログインしました。')
    await tree.sync()
    logging.info("スラッシュコマンドの同期が完了しました。")

# Botを実行
if DISCORD_BOT_TOKEN:
    keep_alive()
    client.run(DISCORD_BOT_TOKEN)
else:
    logging.error("環境変数 'DISCORD_BOT_TOKEN' が設定されていません。")
