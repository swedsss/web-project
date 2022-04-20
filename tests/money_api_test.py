from constants import *
from requests import get, post, delete, put
from pprint import pprint

app_address = f"http://{APP_HOST}:{APP_PORT}"

# Получение списка всех сумм
print()
print('Получение списка всех сумм:')
pprint(get(app_address + '/api/money').json())

# Ошибочный запрос на получение одного суммы — неверный id мероприятия
print()
print('Ошибочный запрос на получение одного суммы - неверный id мероприятия:')
pprint(get(app_address + '/api/money/999/1').json())

# Ошибочный запрос на получение одного суммы — неверный id пользователя
print()
print('Ошибочный запрос на получение одного суммы - неверный id пользователя:')
pprint(get(app_address + '/api/money/1/999').json())

# Ошибочный запрос на получение одного суммы — строка
print()
print('Ошибочный запрос на получение одного суммы - строка:')
pprint(get(app_address + '/api/money/abc/def').json())

# Корректный запрос на добавление суммы:
print()
print('Корректный запрос на добавление суммы:')
print(post(app_address + '/api/money',
           json={
               'event_id': 1,
               'user_id': 1,
               'cost': 456.12,
           }).json())

# Получение списка всех сумм
print()
print('Получение списка всех сумм:')
pprint(get(app_address + '/api/money').json())

# Некорректный запрос на добавление суммы - повторное добавление:
print()
print('Некорректный запрос на добавление суммы - повторное добавление:')
print(post(app_address + '/api/money',
           json={
               'event_id': 1,
               'user_id': 1,
               'cost': 789.01
           }).json())

# Некорректный запрос на добавление суммы - параметр json не указан:
print()
print('Некорректный запрос на добавление суммы - параметр json не указан:')
print(post(app_address + '/api/money').json())

# Некорректный запрос на добавление суммы - отсутствуют необходимые параметры:
print()
print('Некорректный запрос на добавление суммы - отсутствуют необходимые параметры:')
print(post(app_address + '/api/money',
           json={
               'event_id': 4,
           }).json())

# Корректное получение одного суммы:
print()
print('Корректное получение одного суммы:')
pprint(get(app_address + f'/api/money/1/1').json())

# Корректный запрос на изменение суммы:
print()
print('Корректный запрос на изменение суммы:')
print(put(app_address + '/api/money/1/1',
          json={
              'cost': 1234.56,
          }).json())

# Корректное получение одного суммы:
print()
print('Корректное получение одного суммы:')
pprint(get(app_address + f'/api/money/1/1').json())

# Корректный запрос на удаление суммы:
print()
print('Корректный запрос на удаление суммы:')
print(delete(app_address + f'/api/money/1/1').json())

# Получение всех сумм
print()
print('Получение всех сумм:')
pprint(get(app_address + '/api/money').json())

# Некорректный запрос на удаление суммы - повторное удаление:
print()
print('# Некорректный запрос на удаление суммы - повторное удаление:')
print(delete(app_address + f'/api/money/1/1').json())

# Некорректный запрос на удаление суммы - пользователь с таким id не существует:
print()
print('Некорректный запрос на удаление суммы - пользователь с таким id не существует:')
print(delete(app_address + '/api/money/1/999').json())

# Некорректный запрос на удаление суммы - мероприятие с таким id не существует:
print()
print('Некорректный запрос на удаление суммы - мероприятие с таким id не существует:')
print(delete(app_address + '/api/money/999/1').json())

# Некорректный запрос на удаление суммы - строка вмеcто id:
print()
print('Некорректный запрос на удаление суммы - строка вмеcто id:')
pprint(get(app_address + '/api/money/abc/вуа').json())
