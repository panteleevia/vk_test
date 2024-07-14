import pandas as pd
import random
import string
import requests
import time
from datetime import datetime, timedelta
import sqlite3

class Generator():
    def __init__(self):
        #api fish-text.ru
        self.__url = 'https://fish-text.ru/get'
        # Параметры запроса
        self.__params = {
            'format': 'html',
            'type': 'paragraph',
        }
        self.__result = {}
        self.__connection = sqlite3.connect('vk.db')
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute('SELECT tod.Url, tod.Text FROM T_Documents tod')
        self.__current_bd = pd.DataFrame(self.__cursor.fetchall(), columns=[description[0] for description in self.__cursor.description])


    #Генератор случайных URL
    def __generate_random_string(self, length: int) -> str:
        rand = random.randint(0, 1)
        #выдаёт случайное новое значение или случайное значение из имеющихся
        try:
            if rand == 1:
                letters = string.ascii_letters + string.digits
                return ''.join(random.choice(letters) for i in range(length))
            else:
                url = self.__current_bd['Url'][random.randint(0, len(self.__current_bd)-1)]
                return url
        except:
            return ''
        
    #Генератор постов
    def __generate_new_text(self) -> str:
        #выдаёт случаное новое значение из api или берёт случайный текст из уже имеющихся
        rand = random.choices([0, 1], [0.4, 0.6], k=1)[0]
        try:
            if rand == 1:
                try:
                    response = requests.get(self.__url, params=self.__params)
                    fish_text = response.text.replace('<p>', '').split('</p>')[0]

                    # чтобы не получить блокировку за превышение количества запросов
                    time.sleep(0.1)
                except:
                    fish_text = ''

                return fish_text
            else:
                fish_text = self.__current_bd['Text'][random.randint(0, len(self.__current_bd)-1)]
                return fish_text
        except:
            return ''

    #функция для генерации случайной даты в заданном диапазоне
    def __generate_random_date(self, start_date: datetime, end_date: datetime):
        rand = random.choices([0, 1], [0.2, 0.8], k=1)[0]
        if rand == 1:
            delta = end_date - start_date
            random_days = random.randrange(abs(delta.days))
            dt = start_date + timedelta(days=random_days)
            try:
                return int(dt.timestamp())
            except:
                return ''
        else:
            return 'Error date'

    def __update_bd(self):
        self.__cursor.execute('SELECT tod.Url, tod.Text FROM T_Documents tod')
        self.__current_bd = pd.DataFrame(self.__cursor.fetchall(),
                                         columns=[description[0] for description in self.__cursor.description])

    #функция генерация документов
    def generate_document(self):
        #примерно раз в 10 секунд, будет выгружать то, что уже находится в очереди и подставлять в значения
        #тем самым иммитируя то, что документ обновился
        if datetime.now().second % 10 == 0:
            self.__update_bd()


        start_date = [datetime(2001, 1, 1, hour=random.randint(0, 23), minute=random.randint(0, 59)), \
                      datetime(1001, 1, 1, hour=random.randint(0, 23), minute=random.randint(0, 59)), \
                      datetime(2011, 1, 1, hour=random.randint(0, 23), minute=random.randint(0, 59)), \
                      datetime(21, 1, 1, hour=random.randint(0, 23), minute=random.randint(0, 59)), \
                      datetime(2031, 1, 1, hour=random.randint(0, 23), minute=random.randint(0, 59))]
        end_date = [datetime(2000, 1, 1, hour=random.randint(0, 23), minute=random.randint(0, 59)), \
                    datetime(1000, 1, 1, hour=random.randint(0, 23), minute=random.randint(0, 59)), \
                    datetime(2030, 1, 1, hour=random.randint(0, 23), minute=random.randint(0, 59)), \
                    datetime(20, 1, 1, hour=random.randint(0, 23), minute=random.randint(0, 59)), \
                    datetime(2030, 1, 1, hour=random.randint(0, 23), minute=random.randint(0, 59))]
        prob = [0.3, 0.2, 0.1, 0.25, 0.15]
        #получаем случайные url. Только вариант из 12 символов для нас будет корректным
        self.__result['Url'] = self.__generate_random_string(random.choices([12, 103, 0, 3, 17], prob, k=1)[0])
        self.__result['PubDate'] = ''
        self.__result['Text'] = self.__generate_new_text()
        self.__result['FetchTime'] = self.__generate_random_date(random.choices(start_date, prob, k=1)[0], random.choices(end_date, prob, k=1)[0])
        self.__result['FirstFetchTime'] = ''

        return self.__result

    def __del__(self):
        self.__connection.close()
