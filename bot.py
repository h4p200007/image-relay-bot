import discord
import os

# --- 初期設定 ---
TOKEN = 'MTM4NDgwMjE4MjUyNzk3OTYxMA.Gfvmcd.VOcDR7Yi5cf9DNQjCRdKOl7KCPhQ6IRm7jA0Q4'
投稿チャンネルID = 1384806678184202360  # ← 投稿用チャンネルのID
表示チャンネルID = 1384806801605656587  # ← 表示用チャンネルのID
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
    print(f'✅ Botログイン成功：{client.user}')

@client.event
async def on_message(message):
    if message.channel.id != 1384806678184202360:
        return
    if message.author.bot:
        return
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("image"):
                count = get_counter()
                target_channel = client.get_channel(1384806801605656587)
                await target_channel.send(content=f'# {count:03d}', file=await attachment.to_file())
                update_counter(count + 1)


client.run(TOKEN)
