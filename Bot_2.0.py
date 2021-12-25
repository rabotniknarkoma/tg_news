import telebot
from bs4 import BeautifulSoup
import requests
import time
import sqlite3


DICT_OF_LAST = {}
with open('last_news.txt', 'r') as f:
    files = f.read().split('\n')
    for s in files[:-1]:
        if len(s.split()) > 1:
            DICT_OF_LAST[s.split()[0]] = s.split()[1:]
        else:
            DICT_OF_LAST[s.split()[0]] = []
BOT = telebot.TeleBot(token='1958663412:AAF8xTmHRb1u3too4BX3Sg4FqnxRXuKJCuI')
USER = ''


class SourceValues:
    def __init__(self):
        self.ria = 'https://ria.ru/world/'
        self.rambler = 'https://news.rambler.ru/'
        self.rbc = 'https://www.rbc.ru/newspaper/'
        self.bbc = 'https://www.bbc.com/russian'
        self.gazeta = 'https://www.gazeta.ru/news/'
        self.economics = 'https://lenta.ru/rubrics/economics/'
        self.internet = 'https://lenta.ru/rubrics/media/'
        self.sport = 'https://lenta.ru/rubrics/sport/'
        self.science = 'https://lenta.ru/rubrics/science/'
        self.culture = 'https://lenta.ru/rubrics/culture/'
        self.class_ria = 'list-item__title'
        self.class_rambler = 'Jn9tH'
        self.class_rbc = 'newspaper-page__news'
        self.class_bbc = 'bbc-1fxtbkn evnt13t0'
        self.class_gazeta = 'b_ear-title'

    def get_ria(self):
        url = self.ria
        headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' +
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll('a', self.class_ria)
        news = []
        for i in range(4, -1, -1):
            if texts[i]['href'] not in DICT_OF_LAST['ria']:
                href = self.ria + texts[i]['href']
                txt = texts[i].text
                news.append((txt, href))
                DICT_OF_LAST['ria'].append(texts[i]['href'])
                while len(DICT_OF_LAST['ria']) > 5:
                    DICT_OF_LAST['ria'] = DICT_OF_LAST['ria'][1:]
        return news

    def get_rambler(self):
        url = self.rambler
        headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' +
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll('a', self.class_rambler)
        texts_of_news = soup.findAll('div', '_3CVkE')
        news = []
        for i in range(4, -1, -1):
            if texts[i]['href'] not in DICT_OF_LAST['rambler']:
                href = texts[i]['href']
                txt = texts_of_news[i].text
                news.append((txt, href))
                DICT_OF_LAST['rambler'].append(texts[i]['href'])
                while len(DICT_OF_LAST['rambler']) > 5:
                    DICT_OF_LAST['rambler'] = DICT_OF_LAST['rambler'][1:]
        return news

    def get_rbc(self):
        url = self.rbc
        headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' +
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll('a', self.class_rbc)
        news = []
        for i in range(4, -1, -1):
            if texts[i]['href'] not in DICT_OF_LAST['rbc']:
                href = texts[i]['href']
                txt = texts[i].text
                news.append((txt, href))
                DICT_OF_LAST['rbc'].append(texts[i]['href'])
                while len(DICT_OF_LAST['rbc']) > 5:
                    DICT_OF_LAST['rbc'] = DICT_OF_LAST['rbc'][1:]
        return news

    def get_bbc(self):
        url = self.bbc
        headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' +
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll('a', self.class_bbc)
        news = []
        for i in range(4, -1, -1):
            if texts[i]['href'] not in DICT_OF_LAST['bbc']:
                href = self.bbc.split('/russian')[0] + texts[i]['href']
                txt = texts[i].text
                news.append((txt, href))
                DICT_OF_LAST['bbc'].append(texts[i]['href'])
                while len(DICT_OF_LAST['bbc']) > 5:
                    DICT_OF_LAST['bbc'] = DICT_OF_LAST['bbc'][1:]
        return news

    def get_gazeta(self):
        url = self.gazeta
        headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' +
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll('div', self.class_gazeta)
        href_of_news = soup.findAll('a', 'b_ear-image')
        news = []
        for i in range(4, -1, -1):
            if href_of_news[i]['href'] not in DICT_OF_LAST['gazeta']:
                href = self.gazeta.split('/news/')[0] + href_of_news[i]['href']
                txt = texts[i].text
                news.append((txt, href))
                DICT_OF_LAST['gazeta'].append(href_of_news[i]['href'])
                while len(DICT_OF_LAST['gazeta']) > 5:
                    DICT_OF_LAST['gazeta'] = DICT_OF_LAST['gazeta'][1:]
        return news

    def get_economics(self):
        url = self.economics
        headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' +
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll('a', 'titles')
        news = []
        for i in range(4, -1, -1):
            if texts[i]['href'] not in DICT_OF_LAST['economics']:
                href = 'https://lenta.ru' + texts[i]['href']
                txt = texts[i].text
                news.append((txt, href))
                DICT_OF_LAST['economics'].append(texts[i]['href'])
                while len(DICT_OF_LAST['economics']) > 5:
                    DICT_OF_LAST['economics'] = DICT_OF_LAST['economics'][1:]
        return news

    def get_internet(self):
        url = self.internet
        headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' +
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll('a', 'titles')
        news = []
        for i in range(4, -1, -1):
            if texts[i]['href'] not in DICT_OF_LAST['internet']:
                href = 'https://lenta.ru' + texts[i]['href']
                txt = texts[i].text
                news.append((txt, href))
                DICT_OF_LAST['internet'].append(texts[i]['href'])
                while len(DICT_OF_LAST['internet']) > 5:
                    DICT_OF_LAST['internet'] = DICT_OF_LAST['internet'][1:]
        return news

    def get_sport(self):
        url = self.sport
        headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' +
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll('a', 'titles')
        news = []
        for i in range(4, -1, -1):
            if texts[i]['href'] not in DICT_OF_LAST['sport']:
                href = 'https://lenta.ru' + texts[i]['href']
                txt = texts[i].text
                news.append((txt, href))
                DICT_OF_LAST['sport'].append(texts[i]['href'])
                while len(DICT_OF_LAST['sport']) > 5:
                    DICT_OF_LAST['sport'] = DICT_OF_LAST['sport'][1:]
        return news

    def get_science(self):
        url = self.science
        headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' +
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll('a', 'titles')
        news = []
        for i in range(4, -1, -1):
            if texts[i]['href'] not in DICT_OF_LAST['science']:
                href = 'https://lenta.ru' + texts[i]['href']
                txt = texts[i].text
                news.append((txt, href))
                DICT_OF_LAST['science'].append(texts[i]['href'])
                while len(DICT_OF_LAST['science']) > 5:
                    DICT_OF_LAST['science'] = DICT_OF_LAST['science'][1:]
        return news

    def get_culture(self):
        url = self.culture
        headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' +
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll('a', 'titles')
        news = []
        for i in range(4, -1, -1):
            if texts[i]['href'] not in DICT_OF_LAST['culture']:
                href = 'https://lenta.ru' + texts[i]['href']
                txt = texts[i].text
                news.append((txt, href))
                DICT_OF_LAST['culture'].append(texts[i]['href'])
                while len(DICT_OF_LAST['culture']) > 5:
                    DICT_OF_LAST['culture'] = DICT_OF_LAST['culture'][1:]
        return news


worker = SourceValues()


while True:
    table = sqlite3.connect('Users_db.sqlite')
    cur = table.cursor()
    users_and_sources = cur.execute(f"""SELECT chat_id, choice FROM Sources WHERE mode='resources'""").fetchall()
    users_and_categories = cur.execute(f"""SELECT chat_id, choice FROM Sources WHERE mode='categories'""").fetchall()
    sources = {}
    categories = {}
    for pack in users_and_sources:
        name1, sources1 = pack
        sources1 = sources1.split(', ')
        sources[name1] = sources1
    for pack in users_and_categories:
        name2, categories2 = pack
        categories2 = categories2.split(', ')
        categories[name2] = categories2
    table.close()
    news_ria = worker.get_ria()
    news_rambler = worker.get_rambler()
    news_rbc = worker.get_rbc()
    news_bbc = worker.get_bbc()
    news_gazeta = worker.get_gazeta()
    news_economics = worker.get_economics()
    news_internet = worker.get_internet()
    news_sport = worker.get_sport()
    news_science = worker.get_science()
    news_culture = worker.get_culture()
    with open('last_news.txt', 'w') as f:
        for name in DICT_OF_LAST:
            f.write(name + ' ' + ' '.join(DICT_OF_LAST[name]) + '\n')
    for name in sources:
        websites = sources[name]
        for site in websites:
            if site == 'ria':
                for new in news_ria:
                    text, link = new
                    BOT.send_message(name, '<a href="{}">{}</a>'.format(link, text), parse_mode='html')
            elif site == 'rambler':
                for new in news_rambler:
                    text, link = new
                    BOT.send_message(name, '<a href="{}">{}</a>'.format(link, text), parse_mode='html')
            elif site == 'rbc':
                for new in news_rbc:
                    text, link = new
                    BOT.send_message(name, '<a href="{}">{}</a>'.format(link, text), parse_mode='html')
            elif site == 'bbc':
                for new in news_bbc:
                    text, link = new
                    BOT.send_message(name, '<a href="{}">{}</a>'.format(link, text), parse_mode='html')
            elif site == 'gazeta':
                for new in news_gazeta:
                    text, link = new
                    BOT.send_message(name, '<a href="{}">{}</a>'.format(link, text), parse_mode='html')
    for name in categories:
        websites = categories[name]
        for category in websites:
            if category == 'economics':
                for new in news_economics:
                    text, link = new
                    BOT.send_message(name, '{}\n<a href="{}">{}</a>'.format('Экономика', link, text), parse_mode='html')
            elif category == 'internet':
                for new in news_internet:
                    text, link = new
                    BOT.send_message(name, '{}\n<a href="{}">{}</a>'.format('Интернет и СМИ', link, text),
                                     parse_mode='html')
            elif category == 'sport':
                for new in news_sport:
                    text, link = new
                    BOT.send_message(name, '{}\n<a href="{}">{}</a>'.format('Спорт', link, text), parse_mode='html')
            elif category == 'science':
                for new in news_science:
                    text, link = new
                    BOT.send_message(name, '{}\n<a href="{}">{}</a>'.format('Наука', link, text), parse_mode='html')
            elif category == 'culture':
                for new in news_culture:
                    text, link = new
                    BOT.send_message(name, '{}\n<a href="{}">{}</a>'.format('Культура', link, text), parse_mode='html')
                BOT.send_message(name, 'Здесь могла быть ваша реклама!')
    time.sleep(1800)
