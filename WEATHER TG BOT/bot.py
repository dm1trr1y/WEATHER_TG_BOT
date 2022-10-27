#Импортирование библиотек
import telebot
import time
import config
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
#Перевод языка инитерфейса OWM
config_dict = get_default_config()
config_dict['language'] = 'ru'

#создание переменных и присваивание ей токена 
bot = telebot.TeleBot(config.TOKEN, parse_mode=None)

owm = OWM('25195ab99d217e069c6e3e0afa92a45f', config_dict)
mgr = owm.weather_manager()


#команда "Старт"
@bot.message_handler(commands=['start'])
def send_welcome(message):
	
	bot.send_chat_action(message.chat.id, 'typing')
	bot.reply_to(message, "Привет, я - бот который показываю погоду на данный момент. Для того чтобы узнать погоду просто напиши название своего города и я скину тебе данные)")
	bot.send_sticker(message.chat.id, open('static/welcome.webp', 'rb'))

#Команда погода
@bot.message_handler(content_types=['text'])
def weather(message):
	
	bot.send_chat_action(message.chat.id, 'typing')
	bot.send_message(message.chat.id, "Прощитываю информацию о погоде (На самом деле в окно смотрю просто)...")
	bot.send_sticker(message.chat.id, open('static/find.webp', 'rb'))
	time.sleep(5.5)
	

	try:
		#Создание переменной для города и получение его названия из сообщения пользователя
		place = str(message.text)
		observation = mgr.weather_at_place(place)
		w = observation.weather
		#Переменные для данных о температуре и ветре
		temp = w.temperature('celsius')["temp"]
		witers = w.wind()["speed"] 
		witerd = w.wind()["deg"]
		

		# Вычисление направления ветра
		if 0 < witerd < 90:
			direct = "северо-восточный"
		elif 90 < witerd < 180:
			direct = "северо-западный"
		elif 180 < witerd < 270:
			direct = "юго-западный"
		elif 270 < witerd < 360:
			direct = "юго-восточный"		
		elif 0 == witerd == 360:
			direct = "восточный"
		elif witerd == 90:
			direct = "северный"
		elif witerd == 180:
			direct = "западный"
		elif witerd == 270:
			direct = "южный"

		# Предупреждение о направлении и скорости ветра
		if witers < 5:
			witerw = "Ещё легонький "+ direct +" ветерок."
		elif witers < 10:
			witerw = "Ещё "+ direct + " ветер."
		elif witers > 10:
			witerw = "Сильный "+ direct + " ветер."

		answer = "В городе " + str(place) + " сейчас " + w.detailed_status + ".\n"
		
		answer += "Температура примерно " + str(temp) + " °C\n" + "\nВетер "	+ str(direct) + " скоростью " + str(witers) + "м/с. \n"
		#Советы по поводу температуры
		if temp < 10:
			answer += "Сегодня холодно, быстро тепло одевайся. И ШАПКУ НЕ ЗАБУДЬ ИНАЧЕ МАМЕ РАССКАЖУ ЧТО ТЫ ШАПКУ НЕ НОСИШЬ"
		elif temp < 15:
			answer += "Прохладно, одевайся наполовину тепло. К примеру наверх худак, а вот на ноги можно шорты (если ты парень). А если ты девушка, одевай то что сейчас в тренде)"
		elif temp < 22:
			answer += "На улице очень тепло, так что сегодня в гардеробе только шорты и майка. И кепку не забудь, а то в голову напечёт будешь как мой создатель... "
		else:
			answer += "ЖАРА ЖАРА ЖАРА БЕГАЙ ГОЛЫШОМ (и про воду не забудь, а то умрешь)"




		bot.send_chat_action(message.chat.id, 'typing')
		bot.send_message(message.chat.id, answer)
		bot.send_sticker(message.chat.id, open('static/thanks.webp', 'rb'))

		
		print('It`s work is done. User using our bot.')
	except Exception as e:
		bot.reply_to(message, "Такого города я не знаю. Может не правильно ввёл?")
		print('ERROR! A city/town can`t be finded')
		print(e)


#Бесконечный повтор
bot.infinity_polling()