import discord
from discord.ext import commands
from aiohttp import web
import asyncio
import json

# Твій токен бота з Discord Developer Portal
TOKEN = 'MTUwODU2ODkyNjM5NTgyNjIxOA.GpgK-C.6HQpdPS2fQKb1VhvlqN-QnFv5rVwMmkex2CBeY'
# Порт, на якому працюватиме веб-сервер бота
PORT = 5000

intents = discord.Intents.default()
intents.members = True # Обов'язково увімкни Server Members Intent в порталі!
bot = commands.Bot(command_prefix="!", intents=intents)

# Функція обробки HTTP-запитів від сайту
async def handle_contact_request(request):
    try:
        data = await request.json()
        seller_id = int(data.get('seller_id'))
        buyer_id = data.get('buyer_id')
        buyer_name = data.get('buyer_name')
        car_name = data.get('car_name')
        car_url = data.get('car_url')

        # Шукаємо продавця
        seller = await bot.fetch_user(seller_id)
        if not seller:
            return web.json_response({'status': 'error', 'message': 'Seller not found'}, status=404)

        # Формуємо красивий Embed
        embed = discord.Embed(
            title="🚗 Нова заявка на покупку авто!",
            description=f"Привіт! Гравець **{buyer_name}** цікавиться твоїм авто, яке ти виставив на автобазарі.",
            color=discord.Color.gold()
        )
        embed.add_field(name="Автомобіль", value=car_name, inline=False)
        embed.add_field(name="Покупець (Discord)", value=f"<@{buyer_id}>", inline=False)
        embed.add_field(name="Посилання на авто", value=f"[Перейти до оголошення]({car_url})", inline=False)
        embed.set_footer(text="Kurahivka RP | Автобазар")

        # Відправляємо в ПП
        await seller.send(embed=embed)
        
        # Додаємо CORS заголовки, щоб браузер дозволив запит з твого сайту
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
        return web.json_response({'status': 'success'}, headers=headers)

    except discord.Forbidden:
        # Якщо у продавця закриті ПП
        headers = {"Access-Control-Allow-Origin": "*"}
        return web.json_response({'status': 'error', 'message': 'DMs are closed'}, status=403, headers=headers)
    except Exception as e:
        headers = {"Access-Control-Allow-Origin": "*"}
        return web.json_response({'status': 'error', 'message': str(e)}, status=500, headers=headers)

# Обробка OPTIONS запитів для CORS (попередній запит браузера)
async def handle_options(request):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
    return web.Response(status=200, headers=headers)

async def web_server():
    app = web.Application()
    app.router.add_options('/api/contact', handle_options)
    app.router.add_post('/api/contact', handle_contact_request)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"Web server started on port {PORT}")

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')
    # Запускаємо веб-сервер паралельно з ботом
    bot.loop.create_task(web_server())

# Запуск бота
bot.run(TOKEN)
