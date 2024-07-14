# vk_test
Тестовое профильное задание для VK на позицию ML-инженер<br>
Для работы самого модуля достаточно:<br>
1) установить 2 библиотеки:<br>
   pip install requirements.txt<br>
   запустить web-server.py<br>
   python.exe web-server.py<br>
2) Иммитация всего процесса, включая генерацию документов и запись в очередь<br>
   pip install requirements.txt<br>
   pyhon.exe web-server.py<br>
   Запустить ноутбук "Запуск кода"<br>
Все подробности о работе, о том как и что работает в ноутбуке "Описание и логика работы"<br>
В бд vk.db сохранена таблица с результатами, её можно дропнуть для проверки с нуля<br>

connection = sqlite3.connect('vk.db')<br>
cursor = connection.cursor()<br>
z = f"DELETE FROM T_Documents'"<br>
cursor.execute(z)<br>
connection.commit()<br>
connection.close()
<br>
Я не ML, я только учусь<br>
   
