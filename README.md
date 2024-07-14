# vk_test
Тестовое профильное задание для VK на позицию ML-инженер
Для работы самого модуля достаточно:
1) установить 2 библиотеки:
   pip install requirements.txt
   запустить web-server.py
   python.exe web-server.py
2) Иммитация всего процесса, включая генерацию документов и запись в очередь
   pip install requirements.txt
   pyhon.exe web-server.py
   Запустить ноутбук "Запуск кода"
Все подробности о работе, о том как и что работает в ноутбуке "Описание и логика работы"
В бд vk.db сохранена таблица с результатами, её можно дропнуть для проверки с нуля

connection = sqlite3.connect('vk.db')
cursor = connection.cursor()
z = f"DELETE FROM T_Documents'"
cursor.execute(z)
connection.commit()

Я не ML, я только учусь
   
