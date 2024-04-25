# download: discord | openai | py-cord
from openai import OpenAI
import discord
import os
import aiohttp
import io
from discord.ext import commands

# tokens
dalleToken = os.environ.get('openAIDalleToken')
discordToken = os.environ.get('dalleDiscordBotToken')

client = OpenAI(
    # token
    api_key = dalleToken
)

# creating bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)
bot.http_session = aiohttp.ClientSession()

@bot.slash_command(name="imagine", description="Uses DALL-E 3 to generate image")
async def imagine(ctx, prompt: str):
    # defer the response to avoid the "This interaction failed" error
    await ctx.defer()

    try:
        # make the request to the OpenAI API
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1,
        )
        
        # send the image to the channel
        if response.data[0]:
            image_data = response.data[0].url
            await ctx.respond(image_data)
        else:
            await ctx.respond("Try again. Can't generate image.")
            
    except Exception as e:
        await ctx.respond(f"Error: {e}")

# run the bot | discord token
bot.run(discordToken)