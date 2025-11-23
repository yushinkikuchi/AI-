import discord
import google.generativeai as genai
import os
from keep_alive import keep_alive # サーバーを立ち上げるための魔法

# ==========================================
# 設定エリア（環境変数から読み込む）
# ==========================================
# 自分のPCでは動かなくなりますが、サーバー上で動くようになります
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini APIの設定
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Discordボットの設定
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} としてログインしました！')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        clean_text = message.content.replace(f'<@{client.user.id}>', '').strip()
        if not clean_text: return

        try:
            async with message.channel.typing():
                response = model.generate_content(clean_text)
                await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"エラー: {e}")

# サーバーを常時稼働させるためのウェブサーバーを起動
keep_alive()

# ボット起動
client.run(DISCORD_TOKEN)