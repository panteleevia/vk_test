from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import sqlite3

#настройки Flask
app = Flask(__name__)
#список, который будет хранить Url прошедших "модерацию" постов
@app.route('/listener', methods=['POST'])
def listener():
    #отлавливаем ошибку, когда пришёл не json
    try:
        response_data = request.get_json()
        return jsonify(checker(response_data))
    except:
        return 'nil'

def checker(new_document:dict):
    # отлавливаем ошибку, когда пришёл битый словарь без какого-либо ключа
    try:
        Url = new_document['Url']
        FetchTime = new_document['FetchTime']
        Text = new_document['Text']
    except:
        return 'nil'

    # проверяем валидность даты
    try:
        if int(FetchTime) >= 0:
            pass
        else:
            return 'nil'
    except:
        return 'nil'

    # Проверяем, чтобы дата обновления была логичной (появилась позже даты появления интернета в России и раньше, чем текущий момент)
    if FetchTime > datetime(1990, 1, 1).timestamp() and FetchTime < datetime.now().timestamp():
        pass
    else:
        return 'nil'

    try:
        # достаём все url, которые прошли модерацию
        connection = sqlite3.connect('vk.db')
        cursor = connection.cursor()
        cursor.execute("SELECT tod.Url FROM T_Documents tod")
        bd = pd.DataFrame(cursor.fetchall(), columns=[description[0] for description in cursor.description])
        url_list = bd['Url'].to_list()
        connection.close()
        if Url not in url_list:
            if len(Url) == 12:
                connection = sqlite3.connect('vk.db')
                cursor = connection.cursor()
                cursor.execute(
                    'INSERT INTO T_documents (Url, FetchTime, PubDate, Text, FirstFetchTime) VALUES (?, ?, ?, ?, ?)', \
                    (Url, FetchTime, FetchTime, Text, FetchTime))
                connection.commit()
                connection.close()
                return {'Url': Url, 'FetchTime': FetchTime, 'PubDate': FetchTime, 'Text': Text,
                        'FirstFetchTime': FetchTime}
            else:
                return 'nil'

        else:
            connection = sqlite3.connect('vk.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT tod.Url, tod.FetchTime, tod.PubDate, tod.Text, tod.FirstFetchTime \
                        FROM T_Documents tod WHERE tod.Url = '{Url}'")
            bd = pd.DataFrame(cursor.fetchall(), columns=[description[0] for description in cursor.description])
            current_fetch = bd['FirstFetchTime'][0]
            if current_fetch > FetchTime:
                connection = sqlite3.connect('vk.db')
                cursor = connection.cursor()
                z = f"UPDATE T_Documents SET FetchTime='{FetchTime}', PubDate='{FetchTime}', Text='{Text}', \
                        FirstFetchTime='{FetchTime}' WHERE Url='{Url}'"
                cursor.execute(z)
                connection.commit()
                return {'Url': Url, 'FetchTime': FetchTime, 'PubDate': FetchTime, 'Text': Text,
                        'FirstFetchTime': FetchTime}
            else:
                connection = sqlite3.connect('vk.db')
                cursor = connection.cursor()
                z = f"UPDATE T_Documents SET FetchTime='{FetchTime}', PubDate='{bd['PubDate'][0]}', Text='{Text}', \
                        FirstFetchTime='{bd['FirstFetchTime'][0]}' WHERE Url='{Url}'"
                cursor.execute(z)
                connection.commit()
                return {'Url': Url, 'FetchTime': FetchTime, 'PubDate': FetchTime, 'Text': Text,
                        'FirstFetchTime': FetchTime}
            connection.close()
    except:
        return 'nil'
if __name__ == '__main__':

    app.run(debug=True)

