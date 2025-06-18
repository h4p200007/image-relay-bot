import discord
import os
import datetime

# --- 初期設定 ---
TOKEN = os.getenv("TOKEN")
投稿チャンネルID = int(os.getenv("POST_CHANNEL_ID"))
表示チャンネルID = int(os.getenv("VIEW_CHANNEL_ID"))
カウンターファイル = 'counter_v2.txt'

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
    client.start_time = datetime.datetime.utcnow()  # Bot起動時刻を記録
    print(f'✅ Botログイン成功：{client.user}')

@client.event
async def on_message(message):
    if message.channel.id != 投稿チャンネルID:
        return
    if message.author.bot:
        return
    if message.created_at < client.start_time:
        return  # Bot起動より前の投稿は無視（重複防止）

    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("image"):
                count = get_counter()
                target_channel = client.get_channel(表示チャンネルID)
                await target_channel.send(content=f'# {count:03d}', file=await attachment.to_file())
                update_counter(count + 1)

client.run(TOKEN)
