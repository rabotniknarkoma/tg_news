import telebot
import sqlite3
from pyowm import OWM


BOT = telebot.TeleBot(token='1958663412:AAF8xTmHRb1u3too4BX3Sg4FqnxRXuKJCuI')
USER = ''


def get_location(lat, lon):
    url = f'https://yandex.ru/pogoda/maps/nowcast?lat={lat}&lon={lon}&via=hnav&le_Lightnin=1'
    return url


def weather(city):
    owm = OWM('19e51096e0594fd9b2649ee37b68c4bc')
    mgr = owm.weather_manager()
    obs = mgr.weather_at_place(city)
    w = obs.weather
    location = get_location(obs.location.lat,obs.location.lon)
    temperature = w.temperature('celsius')
    return temperature, location


@BOT.message_handler(commands=['weather'])
def handle(message):
    BOT.send_message(message.chat.id, 'Введите название города')
    BOT.register_next_step_handler(message, get_weather)


def get_weather(message):
    city = message.text
    try:
        w = weather(city)
        temp = round(w[0]["feels_like"])
        BOT.send_message(message.chat.id, f'В городе "{city}" сейчас {round(w[0]["temp"])}°С,'
                                          f' чувствуется как {round(w[0]["feels_like"])}°С')
        BOT.send_message(message.chat.id, w[1])
        if temp < -20:
            BOT.send_message(message.chat.id, 'Доставайте валенки!')
        elif -20 < temp < 0:
            BOT.send_message(message.chat.id, 'Лучше надеть подштанники!')
        elif 0 < temp < 10:
            BOT.send_message(message.chat.id, 'Можно ходить в пальто!')
        elif 10 < temp < 20:
            BOT.send_message(message.chat.id, 'Лёгкой курточки хватит!')
        else:
            BOT.send_message(message.chat.id, 'На улице тепло!')
    except Exception:
        BOT.send_message(message.chat.id, 'Упс... Похоже такого города нет в базе')


@BOT.message_handler(commands=['change_mode'])
def handle(message):
    BOT.send_message(message.chat.id, 'Бот работает в двух режимах:\n1. Чтение новостей из выбранных источников\n'
                     + '2. Чтение новостей из выбранных категорий\n\n' + 'По умолчанию режим не стоит!')
    answer = BOT.send_message(message.chat.id, 'Отправь мне цифру выбранного режима.')
    BOT.register_next_step_handler(answer, saver1)


def saver1(message):
    num = message.text
    mode = []
    if num == '1':
        mode.append('resources')
    elif num == '2':
        mode.append('categories')
    else:
        BOT.send_message(message.chat.id, 'Пожалуйста, повторите попытку!\nДля этого введите команду /change_mode.')
        return
    table = sqlite3.connect('Users_db.sqlite')
    cur = table.cursor()
    users = [x[0] for x in cur.execute("""SELECT chat_id FROM Sources""").fetchall()]
    if message.chat.id not in users:
        cur.execute(f"""INSERT INTO Sources(chat_id) VALUES('{message.chat.id}')""")
    cur.execute(f"""UPDATE Sources SET mode='{mode[0]}', choice='' WHERE chat_id = '{message.chat.id}'""")
    table.commit()
    table.close()
    BOT.send_message(message.chat.id, 'Отлично, режим выбран!')


@BOT.message_handler(commands=['change_sources'])
def handle(message):
    table = sqlite3.connect('Users_db.sqlite')
    cur = table.cursor()
    users = [x[0] for x in cur.execute("""SELECT chat_id FROM Sources""").fetchall()]
    users_modes = [x[0] for x in cur.execute(f"""SELECT chat_id FROM Sources WHERE mode='resources'""").fetchall()]
    if message.chat.id not in users:
        BOT.send_message(message.chat.id, 'Пожалуйста, выберите режим!')
        table.commit()
        table.close()
        return
    if message.chat.id not in users_modes:
        BOT.send_message(message.chat.id, 'У вас выбран режим категорий!\nСмените режим, чтобы продолжить.')
        table.commit()
        table.close()
        return
    table.commit()
    table.close()
    BOT.send_message(message.chat.id, 'Список доступных источников:\n1. Риа\n2. Рамблер\n3. Рбк\n4. Вести' +
                                      '\n5. Газета')
    answer = BOT.send_message(message.chat.id, 'Отправь предпочитаемые источники через пробел.\n' +
                              'Указывать только цифры. Пример: 1 3 5')
    BOT.register_next_step_handler(answer, saver2)


def saver2(message):
    sources = []
    changed = message.text.split()
    for name in changed:
        if name == '1':
            sources.append('ria')
        elif name == '2':
            sources.append('rambler')
        elif name == '3':
            sources.append('rbc')
        elif name == '4':
            sources.append('vesti')
        elif name == '5':
            sources.append('gazeta')
        else:
            BOT.send_message(message.chat.id, 'Пожалуйста, введите источники заново!\n' +
                                              'Для этого введите команду /change_sources.')
            return
    table = sqlite3.connect('Users_db.sqlite')
    cur = table.cursor()
    cur.execute(f"""UPDATE Sources SET choice='{', '.join(sources)}' WHERE chat_id = '{str(message.chat.id)}'""")
    BOT.send_message(message.chat.id, 'Отлично! Источники изменены')
    table.commit()
    table.close()


@BOT.message_handler(commands=['change_categories'])
def handle(message):
    table = sqlite3.connect('Users_db.sqlite')
    cur = table.cursor()
    users = [x[0] for x in cur.execute("""SELECT chat_id FROM Sources""").fetchall()]
    users_modes = [x[0] for x in cur.execute(f"""SELECT chat_id FROM Sources WHERE mode='resources'""").fetchall()]
    if message.chat.id not in users:
        BOT.send_message(message.chat.id, 'Пожалуйста, выберите режим!')
        table.commit()
        table.close()
        return
    if message.chat.id in users_modes:
        BOT.send_message(message.chat.id, 'У вас выбран режим источников!\nСмените режим, чтобы продолжить.')
        table.commit()
        table.close()
        return
    table.commit()
    table.close()
    BOT.send_message(message.chat.id, 'Список доступных категорий:\n1. Экономика\n' +
                     '2. Интернет и СМИ\n3. Спорт\n4. Наука\n5. Культура')
    answer = BOT.send_message(message.chat.id, 'Отправь предпочитаемые категории через пробел.\n' +
                              'Указывать только цифры. Пример: 1 3 5')
    BOT.register_next_step_handler(answer, saver3)


def saver3(message):
    sources = []
    changed = message.text.split()
    for name in changed:
        if name == '1':
            sources.append('economics')
        elif name == '2':
            sources.append('internet')
        elif name == '3':
            sources.append('sport')
        elif name == '4':
            sources.append('science')
        elif name == '5':
            sources.append('culture')
        else:
            BOT.send_message(message.chat.id, 'Пожалуйста, введите категории заново!\n' +
                             'Для этого введите команду /change_categories.')
            return
    table = sqlite3.connect('Users_db.sqlite')
    cur = table.cursor()
    cur.execute(f"""UPDATE Sources SET choice='{', '.join(sources)}' WHERE chat_id = '{str(message.chat.id)}'""")
    table.commit()
    table.close()
    BOT.send_message(message.chat.id, 'Отлично! Категории изменены')


BOT.polling(none_stop=True, timeout=0)
