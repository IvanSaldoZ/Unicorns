# Получаем области, в которых больше всего запускается единорогов
# https://www.cbinsights.com/research-unicorn-companies
import bs4 as bs
import requests
import re
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

def get_top_unicorns()-> dict:
    '''Get list of top unicorns'''
    response = requests.get('https://www.cbinsights.com/research-unicorn-companies')
    soup = bs.BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', {'class': 'sortable-theme-bootstrap'})
    unicorn_names = []
    unicorn_values = []
    unicorn_countries = []
    unicorn_fields = []
    unicorn_investors = []
    for row in table.findAll('tr')[1:]:
        row_content = row.findAll('td')
        if row_content:
            unicorn_name = clean_str(row_content[0].string.strip())
            unicorn_value = clean_str(row_content[1].string.strip())
            unicorn_country = clean_str(row_content[3].string.strip())
            unicorn_field = clean_str(row_content[4].string.strip())
            unicorn_investor = clean_str(row_content[5].string.strip())
            unicorn_names.append(unicorn_name)
            unicorn_values.append(unicorn_value)
            unicorn_countries.append(unicorn_country)
            unicorn_fields.append(unicorn_field)
            unicorn_investors.append(unicorn_investor)
    result = {'Names': unicorn_names,
              'Values': unicorn_values,
              'Countries': unicorn_countries,
              'Fields': unicorn_fields,
              'Investors': unicorn_investors,
              }
    return result

def analizing_data(unicorn_data: dict)-> None:
    '''Анализируем количество единорогов по странам, отраслям и инвесторам'''
    countries_data = unicorn_data['Countries']
    fields_data = unicorn_data['Fields']
    investors_data = unicorn_data['Investors']

    # разделяем каждого инвестора отдельно
    investors_data_separate = []
    for investor_name_old in investors_data:
        sepateted_invesotrs = investor_name_old.split(',')
        investors_data_separate.extend(sepateted_invesotrs)

    # Получаем распределение единорогов по странам
    countries_stat = get_stat(countries_data)
    visualize_stat(stat=countries_stat, file_name='countries_stat')
    save_stat(stat=countries_stat, filename='countries_stat')

    # Получаем распределение единорогов по областям
    fields_stat = get_stat(fields_data)
    visualize_stat(fields_stat, file_name='fields_stat')
    save_stat(stat=fields_stat, filename='fields_stat')

    # Получаем распределение единорогов по инвесторам
    investors_stat = get_stat(investors_data_separate)
    save_stat(stat=investors_stat, filename='investors_stat')

    return None

def get_stat(data: list)-> dict:
    '''Получаем статистику распределения по странам/инвесторам/областям на основе
    общих табличных данных'''
    def sort_stat(dictionary: dict)-> dict:
        '''Вспомогательная функция для сортировки по значениям'''
        return {k: v for k,v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}
    stat = defaultdict(int)  # Создаём словарь, содержащий будущую статистику,
    # и значение по умолчанию int (ноль)
    for item in data:
        stat[item] += 1 # если есть, то просто прибавляем единицу
    stat = sort_stat(stat)  # сортируем по убыванию
    return stat

def visualize_stat(stat: dict, file_name: str)-> None:
    '''Визуализируем статистику'''
    data_frame = pd.Series(stat)
    data_frame.plot(kind='bar')
    plt.savefig(file_name+'.png')
    plt.show()
    return None

def save_stat(stat: dict, filename: str)-> None:
    '''Сохраняем в файл статистику'''
    data_frame = pd.Series(stat)
    data_frame.to_excel(filename+'.xls')
    print(data_frame)
    return None

def clean_str(input_str: str) -> str:
    '''При парсинге почему-то могут оставаться рудементы
    вроде \n\t у названий компании'''
    input_str = re.sub("^\s+|\n|\r|\s+$", '', input_str)
    input_str = re.sub("^\s+|\n|\t|\s+$", '', input_str)
    return input_str

unicorn_data = get_top_unicorns()  # Получаем данные из Интернета по единорогам
analizing_data(unicorn_data)       # Превращаем полученные данные в статистику, таблицы и графики