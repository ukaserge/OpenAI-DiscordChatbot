import os
import csv
import aiohttp
import time
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None
)


async def write_csv(content):
    with open('log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(content)



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    print('------')
    print('Ready!')


@bot.command()
async def ai(ctx, *, prompt):
    print("prompt: " + prompt)
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'https://api.openai.com/v1/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY']
            },
            json={
                'model': 'text-davinci-003',
                'prompt': prompt,
                'max_tokens': 512,
                'temperature': 0.9,
                'top_p': 1,
                'n': 1
            }
        ) as response:
            reply = "No reply"
            if response.status == 200:
                data = await response.json()
                reply = data['choices'][0]['text']
                try:
                    await ctx.reply(reply)
                except:
                    await ctx.send('エラーが発生しました')
            else:
                reply = "Error: " + str(response.status)
                await ctx.reply('エラー: {}'.format(response.status))
            await write_csv(prompt, reply)

bot.run(os.environ['DISCORD_BOT_TOKEN'])
