import random
from collections import namedtuple

import telebot
import requests


token = "telegram_bot_token"
weather_api_key = "weather_api_key"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def greet_humam(message):
    bot.send_message(message.chat.id, "Hello!")


coordinates = namedtuple('Coordinates', ('latitude', 'longitude'))
cities = {
    'Yerevan': coordinates(40.178, 40.505),

}

users = {}
@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    user_city = users.get(message.chat.id)

    if user_city and user_city in cities:
        coordinates = cities[user_city]
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={coordinates.latitude}&lon={coordinates.longitude}&appid={weather_api_key}'
        response = requests.get(url)
        status = response.status_code
        if status==200:
            weather = response.json()
            bot.send_message(message.chat.id, weather["weather"][0]["description"])
        else:
            bot.send_message(message.chat.id, "weather is not available")
    else:
        bot.send_message(message.chat.id, "ERROR")


@bot.message_handler(commands=['setup'])
def ask_city(message):
    bot.send_message(message.chat.id, "Каков ваш город?")
    bot.register_next_step_handler(message, proceed_city)

def proceed_city(message):
    bot.send_message(message.chat.id, f'крутой город - {message.text}!')
    users[message.chat.id] = message.text
@bot.message_handler(commands=['send_picture'])
def send_picture(message):
    url = f'https://photostorage.explorest.com/usa/washington/mmatti-mount-shuksan-picture-compressed.jpg'
    bot.send_photo(message.chat_id, url)

bot.polling()