import telebot
import requests


token = "telegram_bot_token"
weather_api_key = "weather_api_key"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def greet_humam(message):
    bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={59.937}&lon={30.308}&appid={weather_api_key}'
    response = requests.get(url)
    status = response.status_code
    if status==200:
        weather = response.json()
        bot.send_message(message.chat.id, weather["weather"][0]["description"])
    else:
        bot.send_message(message.chat.id, "weather is not available")

bot.polling()