import discord
import os
import datetime
from datetime import timezone  # タイムゾーン対応

# --- 初期設定 ---
TOKEN = os.getenv("TOKEN")
投稿チャンネルID = int(os.getenv("POST_CHANNEL_ID"))
表示チャンネルID = int(os.getenv("VIEW_CHANNEL_ID"))
カウンターファイル = 'counter.txt'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

def get_counter():
    if not os.path.exists(カウンターファイル):
        with open(カウンターファイル, 'w') as f:
            f.write('1')
        return 1
    with open(カウンターファイル, 'r') as f:
        return int(f.read())

def update_counter(n):
    with open(カウンターファイル, 'w') as f:
        f.write(str(n))

@client.event
async def on_ready():
    client.start_time = datetime.datetime.now(timezone.utc)  # aware datetime
    client.ignore_until = client.start_time + datetime.timedelta(seconds=5)  # 起動後5秒間の投稿を無視
    print(f'✅ Botログイン成功：{client.user}')

@client.event
async def on_message(message):
    if message.channel.id != 投稿チャンネルID:
        return
    if message.author.bot:
        return
    if message.created_at < client.ignore_until:
        return  # Bot起動直後の投稿は無視

    # !reset コマンド処理
    if message.content and message.content.strip() == '!reset':
        update_counter(1)
        await message.channel.send('🔁 カウンターを #001 にリセットしました。')
        return

    # 添付画像の処理
    if message.attachments:
        for attachment in message.attachments:
            if not attachment.content_type or not attachment.content_type.startswith("image"):
                continue
            count = get_counter()
            target_channel = client.get_channel(表示チャンネルID)
            await target_channel.send(content=f'# {count:03d}', file=await attachment.to_file())
            update_counter(count + 1)

client.run(TOKEN)
