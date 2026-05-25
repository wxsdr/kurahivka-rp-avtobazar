from flask import Flask, request, jsonify
import discord
import threading

TOKEN = "ТОКЕН_БОТА"

app = Flask(__name__)

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

@app.route("/api/contact-seller", methods=["POST"])
def contact_seller():

    data = request.json

    seller_id = int(data["sellerDiscordId"])

    buyer_name = data["buyerName"]

    buyer_id = data["buyerDiscordId"]

    car_name = data["carName"]

    car_link = data["carLink"]

    async def send_dm():

        user = await bot.fetch_user(seller_id)

        if user:

            message = f"""
🚗 **[Kurahivka RP Автобазар] Нова заявка!**

Привіт!

Гравець <@{buyer_id}> цікавиться твоїм авто **{car_name}**

Напиши йому в Discord та домовтесь про продаж 🚘

🔗 Оголошення:
{car_link}
"""

            await user.send(message)

    bot.loop.create_task(send_dm())

    return jsonify({"status":"ok"})

def run_flask():
    app.run(host="0.0.0.0", port=5000)

threading.Thread(target=run_flask).start()

bot.run(TOKEN)
