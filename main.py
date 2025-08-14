import discord
from discord import app_commands
from discord.ui import Modal, TextInput
import gspread
from google.oauth2.service_account import Credentials
import os
import os
import json

# Secretから情報を読み込む
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']

# 書き込みたいGoogleスプレッドシートの名前
SPREADSHEET_NAME = '許諾申請リスト'
# --- 設定項目ここまで ---

# Google Sheets APIのスコープ設定
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# 認証情報の設定
try:
    # 変更後のコード
    gcp_json_credentials_dict = json.loads(os.environ['GCP_SA_KEY'])
    creds = Credentials.from_service_account_info(gcp_json_credentials_dict, scopes=SCOPES)
    gc = gspread.authorize(creds)
    spreadsheet = gc.open(SPREADSHEET_NAME)
    worksheet = spreadsheet.sheet1 # 最初のシートを選択
    print("Googleスプレッドシートへの接続に成功しました。")
except Exception as e:
    print(f"Googleスプレッドシートへの接続に失敗しました: {e}")
    exit()


# Discord BotのIntents設定
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# テキスト入力用のモーダルを定義するクラス
class ReportModal(Modal, title='テキスト入力'):
    # モーダルの入力フィールドを定義
    content = TextInput(
        label='内容',
        style=discord.TextStyle.paragraph, # 複数行の入力を許可
        placeholder='ここにスプレッドシートに書き込みたい内容を入力してください。',
        required=True,
        max_length=1000,
    )

    # モーダルが送信されたときの処理
    async def on_submit(self, interaction: discord.Interaction):
        # 入力されたテキストを取得
        input_text = self.content.value
        
        try:
            # スプレッドシートの新しい行に書き込むデータ
            # ここでは[投稿者名, 内容]を書き込む例
            row_to_add = [interaction.user.display_name, input_text]
            
            # スプレッドシートの末尾に行を追加
            worksheet.append_row(row_to_add)
            
            # ユーザーへの返信
            await interaction.response.send_message(f'「{input_text[:30]}...」をスプレッドシートに記録しました！', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'エラーが発生しました: {e}', ephemeral=True)

# スラッシュコマンドを定義
@tree.command(name="report", description="モーダルを開いてテキストをスプレッドシートに記録します。")
async def report_command(interaction: discord.Interaction):
    # ReportModalのインスタンスを作成して表示
    await interaction.response.send_modal(ReportModal())


# Botが起動したときの処理
@client.event
async def on_ready():
    print(f'{client.user} としてログインしました。')
    # スラッシュコマンドをサーバーに同期
    await tree.sync()
    print("スラッシュコマンドの同期が完了しました。")


# Botを実行
client.run(DISCORD_BOT_TOKEN)
{
  "type": "service_account",
  "project_id": "kyodaku",
  "private_key_id": "30996f3ade0cd74395280caaa6be899bf7ce288e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCokM5kMi5JQrcR\n+L7chGqCG6b5NbAuvymw0vTUL50ZbD7Ek292aqA+kz4uSm2uMSoL0CU22qqzqZ5R\niSOSp4tDwubIpt+FfCMHSszbQEkDA6d3BBxqCXUYd4YRnlLd3HqIRDevdZSYpnoW\nnrYCdO6T8nJIaMTmJevlEhXSqXhtRUTtNKeCEK1N2t5NjBJNk5sbEhcVE3lafHkg\nhnzVOQW31/9sl2DD6f4jECZfD9rlV9+puxFN11n/sO8IQrPvw9lDGIwsL0FatGqI\ncdDYuGt2B3VG+K0Edd2eqFHDWrX2gQKT+4YEOJSwTGT7I19hiE7bGWqpsZZbC2Vx\n1mQ5CmmrAgMBAAECggEAQwDwcWZ6/Jb+0y93mosuFRKt0AC1zBcjmMx6Ej/s5/ad\niqD6XO0sTkNUI61lJKkZSAHQURohYXIKYumq0Lg1hNVbzCV80wARomvquzo163NP\n5WCmdMXWnEeibK1szhC+Sh0nr2CDFRyTihtDSP22+esU31B59+vZ9T+3mfnQS0pn\ncheV06YNGDlgLGydej2BCEU6PRwtulzd+Rk+ATd0x7YlvPGCBjurmEhKpN9BLdun\n5P79iQhGu4B4fZKk1CSRuKXiEsn9aqcfft9tjsyord7m/DP28VzjjvEul60krBWj\nndygxoqnXSsjL6FXzxsc6k3G2xuSQFdsL+leaYyCXQKBgQDtBd04rDwwFwHH99pg\nvQQMRQMDkgGhUQPwpAqJ2MAQ1KEdfxVHNZhKLCFVhD2ku8ZoyqyqGdXY8usogqbu\ntCiJC+1KATtYBve+MCHEx8zNLyZn05JKMhwKgAfA/X2Pc3BjelbPRLSCnCoO/KCr\nB9hV0fENTA8WG3ACaKpK4aNuVQKBgQC2D88gno3R/puk/wlEuzmkY57B9rNgvax5\nyQox54gJSDAuU9C8gEY8iqeKdPv3XcawrrVORElIhttssTg86zUiAaob5kVSXgGC\np1e7inbeNiNNmdB/TBwhkh4RD84pJfcUNteWVPTwuPBd4LWu2QH0c8eKvk3pNRIW\ndINETR53/wKBgBRuKfhlmDaI9SVYbuFhyYSJOk5Heo5+HjnS2fmxzjRlL5IMTzg5\nHWxfS2xEns+hQ+PqfGGZIn61yaFPSbZPnyLY/VYgrw3SY+5n1bFRi4ywIL5YVUbB\n9PrOuFxhPT5tM+XPOMZa5LhRX6q1CeBUJ8iV9RIxWSeNq+T5Qpx7wIuVAoGAZdjW\nMBNClvTtsRGS58Ys6s9n4m3VzwqMT9ytPVmeekLN4Ty2Cp1frUKLkyL6SVlGa1Rw\nzIXa0R3P5jAFm96gbJOty8m3gepgwexHYfyFnq1+dkzTnELBge4xr6290LsSS1aa\np9iC5Z8vp/Sq7lMrisqyF+V5xDoSEkm/nRffMZUCgYBlG0cuwMpzmLO2QSczk+qH\nxhDQCLBgneyWpFRswGCxpO9eK3u9C0qtNVCPH0ZWd41oV5Ma7Oi01J3FcPs5A69h\n7EA1Ct11zDlpU2UQAHhN8QkOzNW6Q6EQZPUBRO6fhOkw6uuYQpHdD2YaqLIjJEdo\nCcipjXU4ywuAjFEGLQoQcQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "discord-sheets-writer@kyodaku.iam.gserviceaccount.com",
  "client_id": "111056931483738948576",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/discord-sheets-writer%40kyodaku.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
