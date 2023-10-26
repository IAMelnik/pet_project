***Скрипт для парсинга производственного календаря с сайта Консультант+***

Устанавливаем библиотеки для парсинга страниц

!pip install requests
!pip install beautifulsoup4

Импортируем библиотеки


from bs4 import BeautifulSoup as bs
import csv
import requests
import json
import pandas as pd
import re
from datetime import datetime


Выполняем парсинг страницы с производственным календарем Консультант+ и выгружаем данные в csv файл

# Отправляем GET-запрос к указанной странице
url = 'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/2023/'
response = requests.get(url)

# Проверяем успешность запроса
if response.status_code == 200:
    # Создаем объект BeautifulSoup для парсинга HTML
    soup = bs(response.content, 'html.parser')

with open('output.csv', mode='w', newline='', encoding='windows-1251') as file:
    writer = csv.writer(file)

    writer.writerow(['Год','Месяц', 'Дата', 'Тип дня', 'День недели'])

    # Находим все таблицы на странице
    tables = soup.find_all('table', {'class': 'cal'})
    year = ''.join(re.findall(r'\d+', soup.title.text))
    for table in tables:
        # Находим заголовок месяца для текущей таблицы
        month_header = table.find('th', class_='month').text.strip()

        rows = table.find_all('tr')[1:]

        # Получаем строку с днями недели
        days_of_week_row = rows[0].find_all('th')

        for row in rows:
            cells = row.find_all('td')
            for cell, day_of_week_cell in zip(cells, days_of_week_row):
                date = cell.text.strip('*')
                day_type = ''
                #day_of_week = ''
                # Получаем тип дня, игнорируя 'inactively'
                if not cell.get('class'):
                    day_type = 'Рабочий'
                elif 'holiday' in cell.get('class'):
                    day_type = 'Праздник'
                elif 'weekend' in cell.get('class'):
                    day_type = 'Выходной'
                elif 'preholiday' in cell.get('class'):
                    day_type = 'Предпраздничный'
                elif 'inactively' in cell.get('class'):
                  continue

                #day_of_week_cell = table.find_all('tr')[1:][0].find_all('th')[cells.index(cell)]
                #day_of_week = day_of_week_cell.text.strip()
                day_of_week = day_of_week_cell.text.strip()
                writer.writerow([year,month_header, date, day_type, day_of_week])

print('Данные успешно выгружены в output.csv.')
