from constants import *
from requests import get, post, put, delete
from pprint import pprint

app_address = f"http://{APP_HOST}:{APP_PORT}"

# Получение всех пользователей
print()
print('Получение всех пользователей:')
pprint(get(app_address + '/api/users').json())

# Ошибочный запрос на получение одного пользователя — неверный id
print()
print('Ошибочный запрос на получение одного пользователя - неверный id:')
pprint(get(app_address + '/api/users/999').json())

# Ошибочный запрос на получение одного пользователя — строка
print()
print('Ошибочный запрос на получение одного пользователя - строка:')
pprint(get(app_address + '/api/users/abc').json())

# Корректный запрос на добавление пользователя:
print()
print('Корректный запрос на добавление пользователя:')
print(post(app_address + '/api/users',
           json={
               'email': 'pupkin@mail.org',
               'password': 'pupkin',
               'surname': 'Пупкин',
               'name': 'Вася',
           }).json())

# Получение всех пользователей
print()
print('Получение всех пользователей:')
req_dict = get(app_address + '/api/users').json()
pprint(req_dict)

new_user_id = len(req_dict['users'])

# Некорректный запрос на добавление пользователя - параметр json не указан:
print()
print('Некорректный запрос на добавление пользователя - параметр json не указан:')
print(post(app_address + '/api/users').json())

# Некорректный запрос на добавление пользователя - отсутствуют необходимые параметры:
print()
print('Некорректный запрос на добавление пользователя - отсутствуют необходимые параметры:')
print(post(app_address + '/api/users',
           json={
               'email': 'pupkin@mail.org',
               'password': 'pupkin',
               'name': 'Вася',
           }).json())

# Корректный запрос на изменение данных пользователя
print()
print('Корректный запрос на изменение данных пользователя:')
print(put(app_address + f'/api/users/{new_user_id}',
          json={
              'email': 'pupkin@mail.org',
              'password': 'pupkin',
              'surname': 'Пупкин',
              'name': 'Василий',
          }).json())

# Корректное получение одного пользователя
print()
print('Корректное получение одного пользователя:')
pprint(get(app_address + f'/api/users/{new_user_id}').json())

# Корректный запрос на изменение данных пользователя
print()
print('Некорректный запрос на изменение данных пользователя - отсутствуют необходимые параметры:')
print(put(app_address + f'/api/users/{new_user_id}',
          json={
              'email': 'pupkin@mail.org',
              'surname': 'Пупкин',
              'name': 'Василий',
          }).json())

# Корректный запрос на удаление пользователя:
print()
print('Корректный запрос на удаление пользователя:')
print(delete(app_address + f'/api/users/{new_user_id}').json())

# Получение всех пользователей
print()
print('Получение всех пользователей:')
pprint(get(app_address + '/api/users').json())

# Некорректный запрос на удаление пользователя - пользователь с таким id не существует:
print()
print('Некорректный запрос на удаление пользователя - пользователь с таким id не существует:')
print(delete(app_address + '/api/users/999').json())

# Некорректный запрос на удаление пользователя - строка вмеcто id:
print()
print('Некорректный запрос на удаление пользователя - строка вмеcто id:')
pprint(get(app_address + '/api/users/abc').json())
