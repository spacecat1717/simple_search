RU

Запуск сервиса
1. Установить Posrtgesql и Elasticsearch (при необходимости)
2. Создать базу данных Postgre
3. Клонировать репозиторий
4. В файле .env прописать данные для подключения к БД и абсолютный путь к файлу csv, из которого необходимо импортировать данные
5. Запустить скрипт preparing.sh
6. После корректного выполнения скрипта, запустить скрипт start.sh



Запросы к сервису

Сервис по умолчанию работает на localhost:8000.
При необходимости конфигурацию можно изменить в файле ./main.py
Запрос на поиск: GET http://localhost:8000/search?q='ваш_запрос'
Запрос на удаление: GET http://localhost:8000/deleteh?rec_id='id_записи_для_удаления'


EN

Run the service
1. Install Postgresql and Elasticsearch (if necessary)
2. Create Postgresql DB
3. Clone this repo
4. In .env file write down variables for DB connection and abspath to file with data import to
5. Run preparing.sh script
6. After correct finishing the script, run start.sh script

Requests to the service

The service works on localhost:8000 by default
If necessary, you can change it on ./main.py file

Request for search: GET http://localhost:8000/search?q='ваш_запрос'
Request for delete: GET http://localhost:8000/deleteh?rec_id='id_записи_для_удаления'
