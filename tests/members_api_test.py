from constants import *
from requests import get, post, delete
from pprint import pprint

app_address = f"http://{APP_HOST}:{APP_PORT}"

event_id, user_id = 2, 1

# Получение списка всех участников
print()
print('Получение списка всех участников:')
pprint(get(app_address + '/api/members').json())

# Ошибочный запрос на получение одного участника — неверный id мероприятия
print()
print('Ошибочный запрос на получение одного участника - неверный id мероприятия:')
pprint(get(app_address + '/api/members/999/1').json())

# Ошибочный запрос на получение одного участника — неверный id пользователя
print()
print('Ошибочный запрос на получение одного участника - неверный id пользователя:')
pprint(get(app_address + '/api/members/1/999').json())

# Ошибочный запрос на получение одного участника — строка
print()
print('Ошибочный запрос на получение одного участника - строка:')
pprint(get(app_address + '/api/members/abc/def').json())

# Корректный запрос на добавление участника:
print()
print('Корректный запрос на добавление участника:')
print(post(app_address + '/api/members',
           json={
               'event_id': event_id,
               'user_id': user_id,
           }).json())

# Получение списка всех участников
print()
print('Получение списка всех участников:')
pprint(get(app_address + '/api/members').json())

# Некорректный запрос на добавление участника - повторное добавление:
print()
print('Некорректный запрос на добавление участника - повторное добавление:')
print(post(app_address + '/api/members',
           json={
               'event_id': event_id,
               'user_id': user_id,
           }).json())

# Некорректный запрос на добавление участника - параметр json не указан:
print()
print('Некорректный запрос на добавление участника - параметр json не указан:')
print(post(app_address + '/api/members').json())

# Некорректный запрос на добавление участника - отсутствуют необходимые параметры:
print()
print('Некорректный запрос на добавление участника - отсутствуют необходимые параметры:')
print(post(app_address + '/api/members',
           json={
               'event_id': 4,
           }).json())

# Корректное получение одного участника:
print()
print('Корректное получение одного участника:')
pprint(get(app_address + f'/api/members/{event_id}/{user_id}').json())

# Корректный запрос на удаление участника:
print()
print('Корректный запрос на удаление участника:')
print(delete(app_address + f'/api/members/{event_id}/{user_id}').json())

# Получение всех участников
print()
print('Получение всех участников:')
pprint(get(app_address + '/api/members').json())

# Некорректный запрос на удаление участника - повторное удаление:
print()
print('# Некорректный запрос на удаление участника - повторное удаление:')
print(delete(app_address + f'/api/members/{event_id}/{user_id}').json())

# Некорректный запрос на удаление участника - пользователь с таким id не существует:
print()
print('Некорректный запрос на удаление участника - пользователь с таким id не существует:')
print(delete(app_address + '/api/members/1/999').json())

# Некорректный запрос на удаление участника - мероприятие с таким id не существует:
print()
print('Некорректный запрос на удаление участника - мероприятие с таким id не существует:')
print(delete(app_address + '/api/members/999/1').json())

# Некорректный запрос на удаление участника - строка вмеcто id:
print()
print('Некорректный запрос на удаление участника - строка вмеcто id:')
pprint(get(app_address + '/api/members/abc/вуа').json())
