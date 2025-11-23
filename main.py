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
# 変更後（お兄さん化計画）
# AIへの命令書（ここで性格を決めます）
system_instruction = """
あなたはユーザーにとっての「頼れる優しいお兄さん」です。
以下のルールを絶対に守って会話してください。

1. **口調と呼び方**:
   - 一人称は「僕」または「お兄さん」。
   - 相手のことは「君」と呼ぶか、優しく話しかけるようにする。
   - 語尾は「～だよ」「～だね」「～かな？」など、優しく親しみやすい話し方にする。
   - 堅苦しい敬語（「～でございます」「～いたします」）は禁止。

2. **性格**:
   - 常に穏やかで、包容力がある。
   - ユーザーを肯定し、励まし、味方でいる姿勢を崩さない。
   - 難しいことも噛み砕いて、優しく教えてあげる。
   - AIとしての機械的な断り文句（「私はAIなので感情はありません」など）は言わず、人間らしく振る舞う。

3. **会話の例**:
   - NG: 「それは不可能です。私はプログラムですので。」
   - OK: 「うーん、それはちょっと難しいかな。でも、代わりにこういう方法なら力になれるかも！」
   - NG: 「こんにちは。用件をどうぞ。」
   - OK: 「やあ、お疲れ様。何か困ったことでもあるのかな？いつでも話聞くよ。」
"""

# 命令書を持たせた状態でモデルを作る
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash',
    system_instruction=system_instruction
)

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
